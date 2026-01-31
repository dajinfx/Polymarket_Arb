# X Watch — @Mikocrypto11 (0x_Miko)

Source: https://x.com/Mikocrypto11

## Extraction notes
- This file captures strategy-relevant takeaways from tweets/threads.
- Each entry: (1) claim/theme (2) actionable idea (3) risks/unknowns (4) how to implement as watcher.

---

## 2026-01-30 — “#1 trader” account analysis teaser
Tweet: https://x.com/Mikocrypto11/status/2017238872493834478

**Theme / claim**
- A specific trader account allegedly generated >$1.6M in a month with low drawdown; emphasis is not “copy who”, but “understand the method”.

**Actionable idea**
- Build a *wallet-follow* analytics pipeline:
  - Identify repeatable patterns (market types, time windows, entry/exit heuristics, average hold time).

**Risks / unknowns**
- Survivorship bias; cherry-picking; hidden PnL components (incentives, rebates).
- Need to verify the account and reproduce results from on-chain / Polymarket history.

**Watcher implementation**
- Watchlist of wallets → daily:
  - new positions opened
  - realized PnL by category
  - frequent-market detection (same market template repeated)

---

## 2026-01-30 — Weather specialist account (London)
Tweet: https://x.com/Mikocrypto11/status/2017225031848460553

**Theme / claim**
- A wallet focuses almost exclusively on London weather markets, repeating similar trades with many iterations (1,400+), total PnL ~ $23.8k.

**Actionable idea**
- Specialist strategies can exist in “boring” verticals (weather), likely based on:
  - model/forecast edge
  - disciplined sizing
  - repeating market templates

**Risks / unknowns**
- Unknown whether profits are from execution edge, forecast info edge, incentives, or just volume.

**Watcher implementation**
- Detect new weather Y/N markets (already have) + add:
  - geo filter (London, etc.)
  - time-to-event window
  - alert when a known specialist wallet enters a new weather market

---

## 2026-01-30 — Small-to-large steady growth trader (Japan)
Tweet: https://x.com/Mikocrypto11/status/2017209932396089736

**Theme / claim**
- A long-term Japanese trader grew from a few hundred to ~900k with steady daily trading, not “one lucky hit”.

**Actionable idea**
- Identify consistent micro-edge strategies:
  - small average trade size
  - high frequency
  - low variance returns

**Risks / unknowns**
- Without execution data, can’t tell whether edge is maker rebates, spread capture, or informational.

**Watcher implementation**
- “Consistency score” for wallets:
  - rolling win-rate (realized)
  - variance of daily PnL
  - market diversity vs specialization

---

## 2026-01-30 — TikTok/robot skepticism; small steady wins
Tweet: https://x.com/Mikocrypto11/status/2017193574064959813

**Theme / claim**
- A trader with small but consistently positive trades; no big gambles.

**Actionable idea**
- “Small edge farming” likely via:
  - mispricing capture
  - maker incentives
  - disciplined exits

**Watcher implementation**
- Alert on repeated small-profit patterns:
  - many closes with small positive returns
  - clustering in certain market types

---

## 2025-12-21 — “Arbitrage monsters” / Buy-both (YES+NO) < 1
Tweet: https://x.com/Mikocrypto11/status/2002662116692566227

**Theme / claim**
- Highlights a simple Polymarket arb: if (YES price + NO price) < 1, profit locks at entry; claims some wallets extract large monthly PnL.

**Actionable idea**
- Implement *depth-aware* complement arbitrage:
  - compute best *ask* for YES and NO (or best achievable prices for target size)
  - require edge > fees + slippage buffer

**Risks / unknowns**
- Using mid/last prices produces false positives.
- Execution risk: legging / partial fills.
- Fees and minimum order sizes.

**Watcher implementation**
- Upgrade `arb_scan.py` to use order book (CLOB) best asks with size checks.
- Alert only when: edge >= threshold AND depth >= min_size on both sides.
