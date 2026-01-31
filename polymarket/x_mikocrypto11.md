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

## 2026-01-30 — Weather markets: probability is often "already determined" (model edge)
Tweet: https://x.com/Mikocrypto11/status/2017183003965886765

**Theme / claim**
- Argues Polymarket isn’t “just gambling” because some markets (esp. weather) have strong signal: probability can be estimated tightly using ensembles of weather models.

**Actionable idea**
- Treat some verticals as *data/forecast trading* rather than opinion:
  - build a pipeline to map a market’s condition (city/date/threshold) → external forecast distribution
  - trade when Polymarket price deviates from model-implied probability beyond a buffer.

**Risks / unknowns**
- Need reliable parsing of market parameters (location, date, threshold).
- Model error + last-minute forecast updates; liquidity may be thin.

**Watcher implementation**
- Extend `yn_watch.py` (weather) with parameter extraction + “mispricing vs model” alert.

---

## 2026-01-30 — Repeated weather-focused wallet (London) — rationale expansion
Tweet: https://x.com/Mikocrypto11/status/2017168410401190301

**Theme / claim**
- Reinforces the idea that a weather-specialist can generate strong returns with low drawdown.

**Actionable idea**
- Build "vertical specialist" watchlists:
  - detect wallets with high concentration in a topic
  - when they open positions in new markets, alert.

**Watcher implementation**
- Wallet/topic clustering + alerts for new entries.

---

## 2026-01-30 — $2.7M long-term stable trader (discipline/repetition)
Tweet: https://x.com/Mikocrypto11/status/2017157838217630206

**Theme / claim**
- Highlights a large, stable PnL achieved by repeatedly executing one disciplined play (not one-off bets).

**Actionable idea**
- In strategy research, prioritize repeatable templates:
  - same market type
  - similar holding horizon
  - consistent sizing rules

**Watcher implementation**
- Template detection over market metadata (question patterns, time windows) + performance tracking.

---

## 2026-01-30 — Short-horizon crypto Up/Down markets (15-min) with big PnL
Tweet: https://x.com/Mikocrypto11/status/2017143493727248827

**Theme / claim**
- A trader focuses on BTC/ETH/SOL 15-min Up/Down markets; more like microstructure trading than event prediction.

**Actionable idea**
- Treat these as *short-dated event markets* with continuous updates:
  - potential edges: latency to underlying spot moves, spread capture, mean reversion around strikes.

**Risks / unknowns**
- Highly competitive; adverse selection severe; fees dominate if not careful.

**Watcher implementation**
- Watch for new short-dated crypto markets + abnormal spread/volume spikes.

---

## 2026-01-30 — 6 dollars → millions: "script writer" (automation edge)
Tweet: https://x.com/Mikocrypto11/status/2017129218195481074

**Theme / claim**
- Claims extreme growth driven by automation/structure rather than “inside info”.

**Actionable idea**
- Automation advantages:
  - scanning many markets
  - instant execution when edge appears
  - consistent risk sizing

**Watcher implementation**
- Reinforces building robust scanners + fast alerting/exec framework (paper-first).

---

## 2026-01-29 — Political event trade: US shutdown bet with large floating PnL
Tweet: https://x.com/Mikocrypto11/status/2016879001311047882

**Theme / claim**
- Example of large-size event trade; suggests some profits come from managing price swings before resolution.

**Actionable idea**
- Add “resolution proximity + volatility” monitoring:
  - track markets near key decision times
  - alert on large size entering + sudden price jumps.

**Watcher implementation**
- Size/volume spike watcher for event markets.

---

## 2026-01-29 — “98% winrate” trader focuses on one market type
Tweet: https://x.com/Mikocrypto11/status/2016750668690968883

**Theme / claim**
- A trader shows extremely high win-rate and tiny historical losses, allegedly because they *only participate in a single class of markets* (not because they predict better).

**Actionable idea**
- Identify “structural edge” market types:
  - markets where outcome probability is near-certain (e.g., already-known info, near-resolution, deterministic rule triggers)
  - or where there is persistent micro-edge (spread/incentives).

**Risks / unknowns**
- Need to verify winrate and losses from real trade history (avoid storytelling bias).

**Watcher implementation**
- Market classifier for “near-deterministic” setups + alert when new such markets appear.

---

## 2026-01-29 — New wallet: crypto markets, 8,700+ trades, monthly +$400k (15-min focus)
Tweet: https://x.com/Mikocrypto11/status/2016772995512226275

**Theme / claim**
- Reinforces high-frequency short-horizon crypto trading on Polymarket.

**Actionable idea**
- For short-dated up/down markets:
  - watch underlying spot movement + Polymarket price response
  - detect delayed repricing / stale quotes.

**Watcher implementation**
- “Spot vs market” lag watcher (needs spot feed later) + spread/volume spike alerts.

---

## 2026-01-29 — “$100/day possible?” example: BTC/ETH focus to ~$690k
Tweet: https://x.com/Mikocrypto11/status/2016800986883408175

**Theme / claim**
- Suggests consistent small daily gains via narrow focus and repetition.

**Actionable idea**
- Emphasize repeatable templates + strict sizing rather than hero bets.

**Watcher implementation**
- Template + cadence analytics for wallet behavior (open/close timing, hold duration, avg edge).

---

## 2026-01-29 — Weather trader: cumulative +$64k; extreme ROI examples are structure/model-driven
Tweet: https://x.com/Mikocrypto11/status/2016818603098853612

**Theme / claim**
- Weather markets can produce large returns with small stakes when probability is mispriced.

**Actionable idea**
- Build weather-model mispricing signals (same as earlier), add liquidity/market-quality filters.

**Watcher implementation**
- Weather market parameter extraction + mispricing alert.

---

## 2026-01-29 — Another London-weather wallet: 1,400+ predictions, concentrated markets
Tweet: https://x.com/Mikocrypto11/status/2016787363922661405

**Theme / claim**
- Concentration + repetition in weather vertical.

**Actionable idea**
- “Vertical specialist” detection (topic concentration) + follow alerts.

**Watcher implementation**
- Wallet clustering by market text + alert on entries.

---

## 2026-01-28 — Large whale event trade: $2,000,000 NO at 99.9¢ (shutdown market)
Tweet: https://x.com/Mikocrypto11/status/2016458732142830035

**Theme / claim**
- Very large size enters near-certain price region (99.9¢), implying either near-deterministic belief or structural play.

**Actionable idea**
- “Near-1.0 price” markets:
  - if liquidity allows, small edge strategies exist but tail risk (rule risk) dominates.

**Watcher implementation**
- Alerts for markets where best prices are >0.99 or <0.01 + sudden size spikes.

---

## 2026-01-27 — Weather-only trader “HondaCivic” (high-prob + occasional deep mispricing)
Tweet: https://x.com/Mikocrypto11/status/2016131575881335101

**Theme / claim**
- A weather-only trader allegedly earns by mostly buying 70–90c high-prob events, occasionally buying 1–10c “obvious undervalued” lines.

**Actionable idea**
- Two-mode playbook for weather markets:
  1) **High-prob grind**: enter when model probability is very high and price still below model (after fees buffer).
  2) **Deep mispricing pounce**: look for extreme tails priced too cheap vs model.

**Risks / unknowns**
- Without model + liquidity checks this becomes pure gambling.

**Watcher implementation**
- Weather watcher with:
  - parameter extraction
  - model probability estimate (future)
  - thresholds for “high-prob” and “deep tail” alerts

---

## 2026-01-27 — “3–5% near risk-free” structural arb claim (needs specifics)
Tweet: https://x.com/Mikocrypto11/status/2016120251847766184

**Theme / claim**
- Claims a repeatable 3–5% per-trade “near risk-free” strategy; emphasizes not direction betting, but structural arb.

**Actionable idea**
- Treat as hypothesis bucket until details are extracted from the thread:
  - likely candidates: complement arb, cross-market constraints, ladder/range inconsistencies, or incentive farming.

**Watcher implementation**
- Keep a “to-verify” list: once the thread reveals mechanics, we implement the corresponding watcher.

---

## 2026-01-27 — New leaderboard name “Maze8” (rapid +$557k)
Tweet: https://x.com/Mikocrypto11/status/2016106662218850415

**Theme / claim**
- New wallet appears and quickly outperforms long-term top wallets.

**Actionable idea**
- Leaderboard anomaly detection:
  - detect new accounts with unusually steep equity curve

**Watcher implementation**
- If we can access leaderboard data: alert on “new entrant with >X PnL in Y days”.

---

## 2026-01-27 — Dominant account “beachboy4” (top 8 monthly PnL slots)
Tweet: https://x.com/Mikocrypto11/status/2016092569701171259

**Theme / claim**
- Extreme repeated gains; suggests it may be mechanism/incentive/structure driven.

**Actionable idea**
- Identify whether returns come from:
  - incentive farming
  - structured arb
  - microstructure edge

**Watcher implementation**
- Add “whale wallet watchlist” module: when these wallets open positions, alert with market links.

---

## 2026-01-27 — “Polymarket bot case study” & “swisstony” (automation)
Tweets:
- https://x.com/Mikocrypto11/status/2016078648785481872
- https://x.com/Mikocrypto11/status/2016076344707395845

**Theme / claim**
- Emphasizes that profitable bots are already running; highlights a trader allegedly turning $5 into $3.7M.

**Actionable idea**
- The durable edge is usually *system design*:
  - scanning coverage
  - execution speed
  - risk control
  - avoiding stale quotes

**Watcher implementation**
- Reinforces our roadmap: watchers → paper exec → live with kill switches.

---

## 2026-01-26 — BTC-only progression & “safer than CEX” claim
Tweet: https://x.com/Mikocrypto11/status/2015794355991421438

**Theme / claim**
- Argues trading BTC on Polymarket (as prediction markets) can be “safer” than leveraged CEX trading (less liquidation mechanics), and shows an example of grinding up.

**Actionable idea**
- If true, these markets may support lower-vol execution strategies:
  - small edges, controlled downside, no leverage liquidation

**Watcher implementation**
- Crypto-market watcher: identify new BTC markets and track spreads/volatility regimes.

---

## 2026-01-26 — “Betting on yourself” / probability loophole (needs thread)
Tweet: https://x.com/Mikocrypto11/status/2015781771065884791

**Theme / claim**
- Mentions a probability-theory “loophole” and a strategy described as “betting on yourself”.

**Actionable idea**
- Mark for deep extraction: likely involves multi-outcome or self-hedging via correlated markets.

**Watcher implementation**
- Add to “to-verify” list; implement once mechanics are clarified.

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
