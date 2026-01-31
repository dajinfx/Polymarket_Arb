"""Polymarket simple arbitrage scanner.

What it does
- Pulls *all* active, non-archived, non-closed markets from Polymarket Gamma API
- Filters to standard binary markets with outcomes {Yes, No}
- Fetches each market's latest outcome prices
- Flags risk-free (theoretical) arbitrage when buy(Yes)+buy(No) < 1.0

Notes
- This is a *pricing* scanner, not an execution bot.
- Real profitability depends on fees, liquidity, slippage, spread, and fill risk.

Run:
  python arb_scan.py
  python arb_scan.py --min-edge 0.005 --limit 500
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import aiohttp

API_BASE = "https://gamma-api.polymarket.com"


def _to_float(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None


def is_candidate_market(m: dict) -> bool:
    """Structural filter: active + not archived + has Yes/No outcomes."""
    if not isinstance(m, dict):
        return False
    if not m.get("active", False):
        return False
    if m.get("archived", False):
        return False
    if m.get("closed", False):
        return False

    outcomes = m.get("outcomes", [])
    names = {o.get("name") for o in outcomes if isinstance(o, dict)}
    return {"Yes", "No"}.issubset(names)


async def fetch_json(session: aiohttp.ClientSession, url: str, *, params: dict | None = None) -> Any:
    async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
        resp.raise_for_status()
        return await resp.json()


async def load_all_markets(
    session: aiohttp.ClientSession,
    *,
    page_size: int = 200,
    max_markets: Optional[int] = None,
) -> List[dict]:
    """Load markets via pagination.

    Gamma API commonly supports limit + offset.

    If max_markets is set, stops early once that many markets are collected.
    """
    markets: List[dict] = []
    offset = 0

    while True:
        params = {
            "active": "true",
            "archived": "false",
            "closed": "false",
            "limit": page_size,
            "offset": offset,
        }
        data = await fetch_json(session, f"{API_BASE}/markets", params=params)

        if isinstance(data, list):
            page = data
        elif isinstance(data, dict):
            page = data.get("markets", []) or []
        else:
            page = []

        if not page:
            break

        markets.extend(page)
        offset += len(page)

        if max_markets is not None and len(markets) >= max_markets:
            return markets[:max_markets]

        # Normal end: last page shorter than requested size
        if len(page) < page_size:
            break

    return markets


async def fetch_market_prices(session: aiohttp.ClientSession, market_id: str) -> Optional[Tuple[float, float]]:
    data = await fetch_json(session, f"{API_BASE}/markets/{market_id}")

    prices: Dict[str, float] = {}
    for o in data.get("outcomes", []) or []:
        if not isinstance(o, dict):
            continue
        name = o.get("name")
        price = _to_float(o.get("price"))
        if name and price is not None:
            prices[name] = price

    if "Yes" not in prices or "No" not in prices:
        return None

    return prices["Yes"], prices["No"]


@dataclass
class ArbHit:
    market_id: str
    slug: str
    question: str
    yes: float
    no: float
    s: float
    edge: float

    @property
    def url(self) -> str:
        return f"https://polymarket.com/market/{self.slug}"


async def scan(session: aiohttp.ClientSession, *, min_edge: float, limit: Optional[int], concurrency: int) -> List[ArbHit]:
    # If limit is set, we can stop pagination early for faster iteration.
    all_markets = await load_all_markets(session, max_markets=limit)
    candidates = [m for m in all_markets if is_candidate_market(m)]

    if limit is not None:
        candidates = candidates[:limit]

    sem = asyncio.Semaphore(concurrency)

    async def one(m: dict) -> Optional[ArbHit]:
        market_id = str(m.get("id"))
        slug = str(m.get("slug") or "")
        question = str(m.get("question") or "UNKNOWN")

        if not market_id or not slug:
            return None

        async with sem:
            try:
                res = await fetch_market_prices(session, market_id)
            except Exception:
                return None

        if not res:
            return None

        yes, no = res
        s = yes + no

        # Simple risk-free buy-both arb: pay s now, receive 1 at settlement.
        # Profit (ignoring fees) = 1 - s.
        edge = 1.0 - s
        if edge >= min_edge:
            return ArbHit(
                market_id=market_id,
                slug=slug,
                question=question,
                yes=yes,
                no=no,
                s=s,
                edge=edge,
            )

        return None

    hits = await asyncio.gather(*(one(m) for m in candidates))
    out = [h for h in hits if h is not None]
    out.sort(key=lambda x: x.edge, reverse=True)
    return out


def render(hits: List[ArbHit], *, top: int) -> None:
    if not hits:
        print("No arbitrage hits found.")
        return

    print(f"Found {len(hits)} hits. Showing top {min(top, len(hits))} by edge:\n")

    for i, h in enumerate(hits[:top], 1):
        print("=" * 90)
        print(f"{i:02d}. {h.question}")
        print(f"    id={h.market_id}  YES={h.yes:.4f}  NO={h.no:.4f}  SUM={h.s:.4f}  EDGE={h.edge:.4f}")
        print(f"    {h.url}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-edge", type=float, default=0.002, help="Minimum edge (1 - (yes+no)) to report.")
    ap.add_argument("--limit", type=int, default=None, help="Optional cap on number of markets to scan.")
    ap.add_argument("--concurrency", type=int, default=30, help="Concurrent market detail requests.")
    ap.add_argument("--top", type=int, default=30, help="How many hits to print.")
    args = ap.parse_args()

    async def runner():
        async with aiohttp.ClientSession() as session:
            hits = await scan(
                session,
                min_edge=float(args.min_edge),
                limit=args.limit,
                concurrency=int(args.concurrency),
            )
            render(hits, top=int(args.top))

    asyncio.run(runner())


if __name__ == "__main__":
    main()
