# @Mikocrypto11 — Top 10 Distinct Strategy Patterns (Executable Draft)

Source feed: https://x.com/Mikocrypto11 (curated extraction)

> Goal: 10 *distinct* strategy archetypes that can be implemented as (A) opportunity alerts (watchers) and later (B) execution modules.
> Not financial advice. Real edge depends on fees, liquidity, slippage, and rule risk.

---

## 1) Complement Arbitrage (YES + NO < 1)
**Core idea**: For a binary market, buy YES and NO if total cost < 1. Profit locks at settlement.

- **Signal / trigger**: bestAsk(YES) + bestAsk(NO) < 1 - buffer
- **Filters**:
  - depth at best asks >= minSize on both sides
  - market not restricted/archived; adequate liquidity
- **Risks**:
  - false positives if using mid/last prices
  - partial fills / legging risk
  - fees
- **Watcher**: scan binary markets and compute depth-aware edge
- **Execution**: simultaneous (or fast sequential) buy on both sides; cancel/rollback logic

---

## 2) “Already happened” / Deterministic Mispricing (stale event markets)
**Core idea**: Markets sometimes lag reality (e.g., an event already occurred) and still price low probability.

- **Signal**: market condition is objectively true/false by reliable data; market price still far from 0/1.
- **Filters**:
  - only for events with machine-checkable sources (price levels already crossed; scheduled results posted)
- **Risks**:
  - rule-definition mismatch (how Polymarket resolves)
  - data source delays
- **Watcher**: detect “should be near 1.0 but isn’t” by cross-checking external feeds (later)
- **Execution**: buy near-1 side with capped exposure; treat as rule-risk trade

---

## 3) Weather Forecast Model Edge (ensemble vs market)
**Core idea**: Weather markets can be “data trading”. Use multi-model ensemble distribution to estimate probability.

- **Signal**: |P_model(event) - P_market| > threshold
- **Filters**:
  - parse market params: city/date/threshold
  - only trade when forecast confidence high (tight distribution)
- **Risks**:
  - last-minute model flips
  - thin liquidity
- **Watcher**: weather market parser + probability estimator + mispricing alert
- **Execution**: size by confidence; avoid illiquid hours; tighten/close as forecast converges

---

## 4) Attention / Narrative Lag (“market asleep”) trades
**Core idea**: Enter before attention arrives; price can move as attention/liquidity arrives.

- **Signal**: increasing mentions/traffic (proxy) + market price still low / spread wide
- **Filters**:
  - avoid ambiguous resolution
  - require improving liquidity trend
- **Risks**:
  - pure narrative can reverse
  - hard to quantify without social data
- **Watcher**: detect unusual volume/liquidity change + price drift in low-activity markets
- **Execution**: small initial position, scale with confirmation; predefined exit rules

---

## 5) Short-horizon Crypto Up/Down (15-min) microstructure
**Core idea**: Trade short-dated BTC/ETH/SOL up/down markets like microstructure products.

- **Signal**:
  - lag vs spot move (spot moved, market hasn’t repriced)
  - abnormal spread/volume spikes
- **Filters**:
  - only liquid markets; avoid high-fee churn
- **Risks**:
  - extremely competitive; adverse selection
- **Watcher**: new short-horizon market discovery + spread/vol/volume monitor
- **Execution**: strict fee+slippage budget; stop quoting during volatility bursts

---

## 6) Whale / Size Spike Signal
**Core idea**: Very large orders/positions can predict a repricing or create self-fulfilling liquidity pressure.

- **Signal**: sudden jump in volume/liquidity or large prints (if available)
- **Filters**:
  - near event time window
  - ignore if purely wash/market-making churn
- **Risks**:
  - whales can be wrong; can also be hedges
- **Watcher**: per-market volume spike alert + time-to-resolution context
- **Execution**: optional small follow; or liquidity-provision with widened spreads

---

## 7) Leaderboard / New Entrant Anomaly Detection
**Core idea**: New wallets with steep equity curves may indicate a new repeatable edge.

- **Signal**: new wallet appears with PnL > X in Y days or unusually low drawdown
- **Filters**:
  - require enough trades (avoid one lucky hit)
- **Risks**:
  - survivorship bias; cherry-picked screenshots
- **Watcher**: if leaderboard data accessible, alert on anomalies
- **Execution**: not copy-trade; use it to discover market types they focus on

---

## 8) Vertical Specialist Wallet Tracking (topic concentration)
**Core idea**: Some accounts specialize (weather-only, crypto-only). Their entries can be a signal.

- **Signal**: wallet opens position in a market within its specialty
- **Filters**:
  - confirm specialty via historical concentration score
- **Risks**:
  - may be market-making rather than alpha
- **Watcher**: maintain specialist watchlists + entry alerts
- **Execution**: follow only when independent signal also agrees (e.g., model mispricing)

---

## 9) High-Probability Grinding + Occasional Deep-Tail Pounce (two-mode sizing)
**Core idea**: Most trades in 70–90c zone for consistent small wins, plus rare 1–10c “obvious mispricing”.

- **Signal**:
  - Mode A: model probability very high but price still discounted
  - Mode B: extreme tail priced too cheap vs model
- **Filters**:
  - enforce max loss per day; avoid correlated clusters
- **Risks**:
  - tail events happen; can wipe gains if mis-sized
- **Watcher**: classify opportunities into Mode A vs Mode B
- **Execution**: separate risk budgets per mode

---

## 10) Near-0 / Near-1 Price Zone Plays (rule-risk aware)
**Core idea**: Edges may exist near 0.99/0.01 when markets lag, but risk is mostly definition/rules.

- **Signal**: best price near 0/1 but external reality strongly supports that side AND rule text is clear
- **Filters**:
  - only markets with unambiguous resolution criteria
- **Risks**:
  - definition risk dominates; fat-tail loss
- **Watcher**: flag markets with prices beyond thresholds (e.g., >0.99 or <0.01) and show resolution source
- **Execution**: tiny size, diversify, hard cap per market

---

# Next implementation steps (in this repo)
1) Add watcher scripts per strategy (alerts only)
2) Add a shared config + routing to Discord
3) After you provide execution credentials/specs: build paper execution layer + risk limits
