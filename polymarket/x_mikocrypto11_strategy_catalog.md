# @Mikocrypto11 — Strategy Catalog (Draft)

Source: https://x.com/Mikocrypto11

Purpose: a fast, scannable catalog of strategy patterns extracted/abstracted from the feed.
Each item has:
- **One-liner**: what it is
- **Trigger**: what to detect
- **Filters**: reduce false positives
- **Risks**: common failure modes

> This is not financial advice.

---

## A) Arbitrage / Structural opportunities

### S01 — Complement arb (YES + NO < 1)
- **One-liner**: Buy both sides in a binary market when total cost < 1.
- **Trigger**: bestAsk(YES) + bestAsk(NO) < 1 - buffer
- **Filters**: depth >= minSize both sides; fees included; market active
- **Risks**: partial fills; using mid/last creates false positives

### S02 — Cross-market logical constraint arb
- **One-liner**: Trade violations across mutually exclusive / subset / time-sliced markets.
- **Trigger**: constraint graph violations after converting prices → implied probs
- **Filters**: same resolution source; align wording/time windows
- **Risks**: definition mismatch; low liquidity to leg hedges

### S03 — “Already happened” mispricing
- **One-liner**: Markets lag reality; buy the side that’s already objectively true.
- **Trigger**: external data indicates event occurred; market prob still far from 0/1
- **Filters**: machine-checkable sources; rule text unambiguous
- **Risks**: rule/definition risk dominates

### S04 — Near-0 / Near-1 zone plays
- **One-liner**: Edges exist near extremes, but it’s mostly rule risk.
- **Trigger**: best price >0.99 or <0.01 while external evidence strong
- **Filters**: only very clear resolution criteria; cap size
- **Risks**: fat-tail loss from unexpected resolution

### S05 — Attention lag (“market asleep”)
- **One-liner**: Price moves when attention/liquidity arrives, not just facts.
- **Trigger**: rising volume/liquidity + price still lagging prior info
- **Filters**: avoid ambiguous markets; require trend confirmation
- **Risks**: narrative reversals; hard to quantify

### S06 — Leaderboard / new wallet anomaly
- **One-liner**: New steep PnL curves can reveal a repeatable mechanism.
- **Trigger**: new entrant with PnL > X in Y days; low drawdown
- **Filters**: min trade count; exclude one-off lucky hits
- **Risks**: survivorship bias; cherry-picked screenshots

### S07 — Whale / size spike signal
- **One-liner**: Large size often precedes repricing or creates pressure.
- **Trigger**: sudden volume/liquidity spike; large prints (if accessible)
- **Filters**: time-to-resolution context; ignore churn-like activity
- **Risks**: whales hedge and can be wrong

---

## B) Data-driven verticals (Weather)

### S08 — Weather model edge (ensemble vs market)
- **One-liner**: Treat weather markets as data trading.
- **Trigger**: |P_model - P_market| > threshold
- **Filters**: parse city/date/threshold; only high-confidence forecasts
- **Risks**: forecast flips; thin liquidity

### S09 — Weather two-mode sizing (70–90c grind + 1–10c pounce)
- **One-liner**: Separate budgets for high-prob and deep-tail mispricing.
- **Trigger**: Mode A high P_model with discounted price; Mode B tail too cheap
- **Filters**: independent risk budgets; liquidity checks
- **Risks**: deep tails can wipe many small wins if oversized

### S10 — Repeating weather templates
- **One-liner**: Same city/threshold/time window repeats; systematize.
- **Trigger**: pattern match on question metadata
- **Filters**: exclude low-liquidity duplicates
- **Risks**: regime change (forecast model shifts), seasonality

---

## C) Short-horizon / microstructure (esp. crypto 15-min)

### S11 — 15-min up/down microstructure trading
- **One-liner**: Trade short-dated up/down markets like micro products.
- **Trigger**: spread/vol/volume regimes favorable; repeated edges
- **Filters**: only liquid markets; fee budget
- **Risks**: adverse selection; competition

### S12 — Spot–market lag
- **One-liner**: Underlying spot moves first; market reprices later.
- **Trigger**: spot return exceeds threshold; market price hasn’t updated
- **Filters**: stable spot feed; latency checks
- **Risks**: false signals in choppy conditions

### S13 — Spread/depth anomaly
- **One-liner**: Temporary dislocations visible in order book.
- **Trigger**: spread widens; depth collapses; microprice shifts
- **Filters**: exclude illiquid markets; require persistence > N seconds
- **Risks**: often precursor to news jump

### S14 — Event-time volatility regimes
- **One-liner**: Scheduled catalysts change best quoting/trading behavior.
- **Trigger**: time-to-resolution / scheduled event windows
- **Filters**: calendar mapping; avoid quoting through jumps
- **Risks**: missed opportunity vs reduced blow-ups

---

## D) Wallet behavior (use to discover mechanisms)

### S15 — Vertical specialist wallet tracking
- **One-liner**: Specialists repeat in one vertical (weather-only, crypto-only).
- **Trigger**: concentration score high; new entry in that vertical
- **Filters**: confirm via history; require independent signal alignment
- **Risks**: may be market-making, not alpha

### S16 — Consistency scoring (small frequent wins)
- **One-liner**: Identify accounts with low variance / steady gains.
- **Trigger**: rolling win-rate + low drawdown metrics
- **Filters**: enough trades; normalize for incentives
- **Risks**: PnL attribution hard without full data

### S17 — “Dominates leaderboard” single-actor decomposition
- **One-liner**: If one account owns top slots, reverse-engineer market types.
- **Trigger**: leaderboard concentration by wallet
- **Filters**: verify data source; exclude duplicated identities
- **Risks**: might be subsidy farming

### S18 — New account, few trades, very “clean” entries
- **One-liner**: Low trade count but high PnL suggests a template.
- **Trigger**: small N trades; high hit rate
- **Filters**: ignore early noise; look for repeated market type
- **Risks**: could be luck; need follow-up confirmation

### S19 — “High win-rate” explained by market selection
- **One-liner**: Win-rate can be high if only trading near-deterministic setups.
- **Trigger**: wallet focuses on near-0/near-1 or already-known markets
- **Filters**: verify via per-trade entry price distribution
- **Risks**: rare tail events + rule risk

---

## E) Risk management patterns (strategy-critical)

### S20 — Exposure caps by market / cluster / theme
- **One-liner**: Prevent correlated blow-ups.
- **Trigger**: risk accounting per bucket
- **Filters**: define clusters (election slate, crypto basket, etc.)
- **Risks**: under-utilization if too tight

### S21 — Kill switch (disconnect / jump)
- **One-liner**: Auto cancel-all on disconnects or large jumps.
- **Trigger**: WS disconnect; price jump > threshold
- **Filters**: debounce to avoid thrash
- **Risks**: cancellation delays; missed fills

### S22 — Separate risk budgets (Mode A vs Mode B)
- **One-liner**: High-prob grind vs tail pounce must not share risk limits.
- **Trigger**: classify opportunities into modes
- **Filters**: separate caps, stop-loss rules
- **Risks**: hidden correlation between modes

### S23 — De-risk near resolution
- **One-liner**: As resolution approaches, definition risk can dominate.
- **Trigger**: time-to-resolution thresholds
- **Filters**: only if rule ambiguity present
- **Risks**: early exit leaves money on table

---

## F) Automation / execution advantages (enablers)

### S24 — Coverage advantage (scan many markets)
- **One-liner**: Edge appears briefly; you need breadth.
- **Trigger**: multi-market scanning + alerting
- **Filters**: rate limits; prioritization
- **Risks**: operational complexity

### S25 — Trade on executable prices (best ask + depth)
- **One-liner**: Never decide on mid/last; compute fillable price for size.
- **Trigger**: compute depth-weighted executable prices
- **Filters**: min depth, slippage buffer
- **Risks**: stale book; partial fills

### S26 — OMS reconciliation / idempotency
- **One-liner**: Keep orders/positions in sync; avoid phantom states.
- **Trigger**: reconcile loop (open orders, fills, positions)
- **Filters**: backoff; rate-limit safe
- **Risks**: complexity; bugs create losses

### S27 — Execution speed / latency discipline
- **One-liner**: Many edges are timing-based.
- **Trigger**: measure end-to-end latency; prioritize hot paths
- **Filters**: avoid over-cancel (queue loss)
- **Risks**: competition; overfitting to short regimes

---

# Next
- Convert selected items into watchers (Discord alerts) first.
- Paper execution later once credentials + rules are provided.
