# @Mikocrypto11 — Strategy Catalog (Explained)

This document explains the **principle / underlying logic** for each strategy in:
- `x_mikocrypto11_strategy_catalog.md`

Order preserved: **S01 → S27**.

> Not financial advice. Many “edges” disappear after fees, slippage, and definition risk.

---

## S01 — Complement arb (YES + NO < 1)
**Principle**: In a binary market, exactly one outcome pays out 1 at resolution. Holding **YES + NO** (one share each) is therefore a **synthetic risk-free 1** at settlement. If you can acquire both for **< 1**, you lock in profit (before fees).

Why it exists: stale quotes, fragmented liquidity, taker/maker imbalance, or a side not updating.

---

## S02 — Cross-market logical constraint arb
**Principle**: Some markets are logically related: mutually exclusive outcomes must sum to ≤ 1, subsets must price ≤ supersets, and earlier deadlines must price ≥ later deadlines for “by date” events. Violations imply at least one market is mispriced relative to the others.

Why it exists: different trader pools, wording confusion, liquidity differences, and slow capital moving between markets.

---

## S03 — “Already happened” mispricing
**Principle**: If an event is already objectively true/false (by a reliable source) but the market hasn’t updated, the market price is temporarily disconnected from reality. The trade is less about “forecasting” and more about **information latency / attention**.

The core risk isn’t probability—it’s whether the **resolution rules** match your “objective truth”.

---

## S04 — Near-0 / Near-1 zone plays
**Principle**: When a market trades at 0.99 or 0.01, the remaining “edge” is small but may be repeatable if the market systematically underprices certainty or overprices unlikely tails.

In practice this becomes a **rule-risk trade**: tiny expected return, potentially large downside if definition/resolution surprises.

---

## S05 — Attention lag (“market asleep”)
**Principle**: Prices are moved by orders, and orders are moved by attention. Many markets reprice not when facts change, but when **more participants notice**, increasing liquidity and shifting the equilibrium.

This is a reflexive mechanism: attention → liquidity → price movement → more attention.

---

## S06 — Leaderboard / new wallet anomaly
**Principle**: A sudden outlier in PnL may indicate a new repeatable mechanism (arb, incentives, model edge, or execution). The “trade” here is not copying them; it’s using anomaly detection to discover *which market types* are being exploited.

This is essentially “alpha discovery” rather than alpha itself.

---

## S07 — Whale / size spike signal
**Principle**: Large size can be (a) informed, (b) a hedge, or (c) a liquidity event that forces other participants to reprice. Even when uninformed, big flows can create **temporary dislocations** (spread widening, depth depletion).

Signal value comes from context: timing, market type, and whether the size is one-sided.

---

## S08 — Weather model edge (ensemble vs market)
**Principle**: Weather is one of the few verticals where probability is often estimable from physical models. If you can map market conditions (city/date/threshold) to an ensemble forecast distribution, you can compare **P_model** vs **P_market** and trade the spread.

Edge comes from better modeling, faster updates, or focusing on markets with high forecast confidence.

---

## S09 — Weather two-mode sizing (70–90c grind + 1–10c pounce)
**Principle**: Two different return profiles:
- High-prob trades (70–90c) aim for small, frequent wins with lower variance.
- Deep-tail trades (1–10c) can have asymmetric payoff if the tail is systematically underpriced.

Separating risk budgets prevents one tail loss from erasing months of small-edge gains.

---

## S10 — Repeating weather templates
**Principle**: Markets recur with similar structure (same city/metric thresholds). Once you build parsing + modeling for a template, marginal cost to evaluate the next market is near zero.

This is a *scaling* principle: automation turns niche expertise into repeatable throughput.

---

## S11 — 15-min up/down microstructure trading
**Principle**: Very short horizon markets behave like micro-derivatives: order book dynamics, latency, and slippage dominate. The “edge” is often execution quality (spreads, queue position) rather than long-term forecasting.

These markets reward fast detection and disciplined fee control.

---

## S12 — Spot–market lag
**Principle**: If the market references a spot price (or price movement), and the prediction market reprices slower than the underlying spot venue, you can trade the lag. This is classic cross-venue latency/price-discovery arb.

It only works if you measure latency and the market’s reference mechanism is consistent.

---

## S13 — Spread/depth anomaly
**Principle**: Sudden spread widening or depth collapse indicates temporary uncertainty or a liquidity vacuum. This can create opportunities for:
- conservative liquidity provision (wide quotes)
- selective taking of stale levels

But it can also signal impending news/jump risk.

---

## S14 — Event-time volatility regimes
**Principle**: Volatility and adverse selection are not stationary. Near scheduled events or resolution windows, informed flow increases and market makers get picked off more often. A profitable strategy adapts: widen spreads, reduce size, or disable quoting.

This is “regime switching” based on time and event calendars.

---

## S15 — Vertical specialist wallet tracking
**Principle**: Specialists concentrate where they have structural advantage (data edge, execution edge, incentives). Watching their entries is a way to discover which markets currently offer exploitable structure.

Treat wallet tracking as a *lead generator*, not a buy signal.

---

## S16 — Consistency scoring (small frequent wins)
**Principle**: Many profitable systems look boring: small edge, high repetition, low variance. Scoring accounts by stability can filter out “one lucky bet” narratives and highlight process-driven strategies.

The goal is to identify repeatability and robustness.

---

## S17 — “Dominates leaderboard” single-actor decomposition
**Principle**: When one actor dominates, it often indicates one of:
- a systematic arb
- incentive farming
- a microstructure edge

Decomposing their activity (market types, timing, sizing) reveals which mechanism is likely.

---

## S18 — New account, few trades, very “clean” entries
**Principle**: “Clean” entries (high selectivity, minimal noise trades) suggest a rule-based filter or a narrow template being exploited. This can indicate a discoverable condition (e.g., specific market type/expiration window).

Needs time to distinguish from luck.

---

## S19 — “High win-rate” explained by market selection
**Principle**: Win-rate is often a selection artifact: if you only trade near-deterministic setups, you can achieve very high win-rate even with modest edge. The real metric becomes tail-risk and definition risk.

The key is understanding *what types* produce that win-rate.

---

## S20 — Exposure caps by market / cluster / theme
**Principle**: Many prediction markets are correlated (same news cycle, same asset, same event). Without caps, you can unknowingly build a concentrated bet that blows up together.

Capping by cluster is a structural defense against correlation and tail events.

---

## S21 — Kill switch (disconnect / jump)
**Principle**: In CLOB markets, stale quotes are a liability. If you lose data feed or the world changes quickly, your existing orders become “free options” for others to hit.

A kill switch prevents being picked off during outages or jumps.

---

## S22 — Separate risk budgets (Mode A vs Mode B)
**Principle**: Different strategies have different loss distributions. Mixing them under one risk limit hides the true risk: a tail strategy can erase the steady strategy’s profits. Separate budgets keep the portfolio stable.

This is portfolio construction, not just trade selection.

---

## S23 — De-risk near resolution
**Principle**: As resolution nears, probability uncertainty may fall, but **definition risk** can rise (rule interpretations, data source quirks). Many “unexpected losses” happen at settlement due to rules, not probability.

Reducing size near resolution is a rule-risk hedge.

---

## S24 — Coverage advantage (scan many markets)
**Principle**: Many opportunities are short-lived. Breadth increases the chance you are looking at the right place at the right time. Automation converts breadth into consistent capture.

This is a throughput advantage.

---

## S25 — Trade on executable prices (best ask + depth)
**Principle**: “A price” is not actionable unless it’s fillable for your size. Using mid/last creates false edges. You must compute the depth-weighted price you can actually execute.

This turns theoretical signals into real, tradable signals.

---

## S26 — OMS reconciliation / idempotency
**Principle**: Automated trading fails more often from state desync than from bad signals. Reconciliation (orders/fills/positions) and idempotent actions prevent phantom orders, double cancels, or missed fills.

It’s the plumbing that allows safe automation.

---

## S27 — Execution speed / latency discipline
**Principle**: If edge decays quickly (especially in short-horizon markets), the winner is often the one who can observe → decide → execute faster, without breaking risk controls.

Speed only matters if your signal is real and your execution doesn’t churn away edge via fees.
