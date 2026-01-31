"""Polymarket Y/N new-market watcher.

Goal
- Scan active markets and find *binary* Yes/No markets created within the last N days
- Classify into categories (weather / tech / culture / economy) via keyword rules
- Print a short, human-checkable list (title + link + createdAt)

Notes
- Gamma API returns some fields (outcomes/outcomePrices) as JSON strings.
- Category is heuristic (keyword-based) because `category/tags` are often null.

Usage
  python yn_watch.py --days 2 --count 10
  python yn_watch.py --days 2 --count 10 --offset-start 15000 --offset-end 40000

Tip
- Use `--show-stats` to print how many markets/pages were scanned.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests

API_BASE = "https://gamma-api.polymarket.com"


KEYWORDS: Dict[str, List[str]] = {
    "weather": [
        "weather",
        "rain",
        "snow",
        "temperature",
        "hurricane",
        "typhoon",
        "storm",
        "forecast",
        "wind",
        "heat",
        "cold",
    ],
    "tech": [
        "ai",
        "openai",
        "chatgpt",
        "nvidia",
        "tesla",
        "apple",
        "microsoft",
        "google",
        "meta",
        "amazon",
        "gpu",
        "chip",
        "bitcoin",
        "ethereum",
        "crypto",
        "spacex",
    ],
    "culture": [
        "oscars",
        "grammys",
        "emmys",
        "taylor",
        "beyonce",
        "movie",
        "film",
        "album",
        "song",
        "celebrity",
        "twitch",
        "netflix",
        "super bowl",
        "world cup",
        "nba",
        "nfl",
    ],
    "economy": [
        "cpi",
        "inflation",
        "gdp",
        "fed",
        "fomc",
        "rate cut",
        "rate hike",
        "unemployment",
        "recession",
        "stocks",
        "s&p",
        "nasdaq",
        "dow",
        "tariff",
        "yield",
    ],
}


def parse_json_maybe(x: Any) -> Any:
    """Gamma often returns arrays as JSON strings."""
    if x is None:
        return None
    if isinstance(x, (list, dict)):
        return x
    if isinstance(x, str):
        x = x.strip()
        if not x:
            return None
        try:
            return json.loads(x)
        except Exception:
            return None
    return None


def is_yesno_market(m: dict) -> bool:
    outs = parse_json_maybe(m.get("outcomes"))
    if not isinstance(outs, list) or len(outs) != 2:
        return False
    return set(outs) == {"Yes", "No"}


def iso_to_dt(s: str) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def classify(question: str) -> Optional[str]:
    """Heuristic classifier.

    Uses substring matching for long keywords, but applies word-boundary matching
    for very short tokens (e.g. "ai") to avoid false positives like "mAInz".
    """
    import re

    t = (question or "").lower()

    # Prefer longer keywords first (more specific).
    for cat, keys in KEYWORDS.items():
        keys_sorted = sorted(keys, key=len, reverse=True)
        for k in keys_sorted:
            k = k.lower()
            if len(k) <= 2:
                if re.search(rf"\b{re.escape(k)}\b", t):
                    return cat
            else:
                if k in t:
                    return cat
    return None


@dataclass
class MarketHit:
    created_at: datetime
    category: str
    market_id: str
    slug: str
    question: str

    @property
    def url(self) -> str:
        return f"https://polymarket.com/market/{self.slug}"


def fetch_markets_page(offset: int, limit: int) -> List[dict]:
    r = requests.get(
        f"{API_BASE}/markets",
        params={
            "active": "true",
            "archived": "false",
            "closed": "false",
            "limit": limit,
            "offset": offset,
        },
        timeout=40,
    )
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("markets", []) or []
    return []


def scan_recent_yesno(
    *,
    days: float,
    count: int,
    offset_start: int,
    offset_end: int,
    step: int,
    max_per_category: int,
    show_stats: bool,
) -> List[MarketHit]:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)

    hits: List[MarketHit] = []
    scanned = 0
    pages = 0

    for off in range(offset_start, offset_end, step):
        page = fetch_markets_page(off, step)
        if not page:
            break
        pages += 1
        scanned += len(page)

        for m in page:
            if not isinstance(m, dict):
                continue

            ca = iso_to_dt(m.get("createdAt") or "")
            if not ca or ca < cutoff:
                continue

            if not is_yesno_market(m):
                continue

            q = str(m.get("question") or "")
            cat = classify(q)
            if cat not in KEYWORDS:
                continue

            slug = str(m.get("slug") or "")
            mid = str(m.get("id") or "")
            if not slug or not mid:
                continue

            hits.append(
                MarketHit(
                    created_at=ca,
                    category=cat,
                    market_id=mid,
                    slug=slug,
                    question=q,
                )
            )

    hits.sort(key=lambda x: x.created_at, reverse=True)

    # Pick up to `count`, with per-category caps.
    picked: List[MarketHit] = []
    per_cat: Dict[str, int] = {k: 0 for k in KEYWORDS}

    for h in hits:
        if len(picked) >= count:
            break
        if per_cat[h.category] >= max_per_category:
            continue
        picked.append(h)
        per_cat[h.category] += 1

    if show_stats:
        print(f"cutoff_utc={cutoff.isoformat()}")
        print(f"pages_scanned={pages} markets_scanned={scanned} recent_yesno_hits={len(hits)}")
        print(f"picked={len(picked)} per_category={per_cat}")

    return picked


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=2.0, help="Lookback window in days.")
    ap.add_argument("--count", type=int, default=10, help="How many markets to print.")
    ap.add_argument("--offset-start", type=int, default=15000, help="Start offset for scanning (newer markets tend to be higher offsets).")
    ap.add_argument("--offset-end", type=int, default=40000, help="End offset (exclusive).")
    ap.add_argument("--step", type=int, default=200, help="Page size / offset step.")
    ap.add_argument("--max-per-category", type=int, default=3, help="Cap per category when selecting.")
    ap.add_argument("--show-stats", action="store_true", help="Print scan stats.")
    args = ap.parse_args()

    picked = scan_recent_yesno(
        days=float(args.days),
        count=int(args.count),
        offset_start=int(args.offset_start),
        offset_end=int(args.offset_end),
        step=int(args.step),
        max_per_category=int(args.max_per_category),
        show_stats=bool(args.show_stats),
    )

    if not picked:
        print("No matching recent Yes/No markets found for the chosen window/categories.")
        return

    for h in picked:
        print(f"[{h.category}] {h.question}")
        print(f"  createdAt={h.created_at.isoformat()}")
        print(f"  {h.url}")


if __name__ == "__main__":
    main()
