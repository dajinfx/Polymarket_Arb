# Polymarket_Arb

Tools for Polymarket market discovery and (eventually) automated strategies.

## What’s here

- `yn_watch.py` — Daily discovery: new Yes/No markets (< N days) by category (weather/tech/culture/economy)
- `arb_scan.py` — Simple theoretical scan: YES+NO < 1 (buy-both candidate)
- `polymarket/` — Strategy knowledge base (markdown)

## Quick start

```bat
cd /d D:\Git\Polymarket_Arb
python yn_watch.py --days 2 --count 10
python arb_scan.py --limit 1000 --top 20
```

## Strategy knowledge base
See `polymarket/`.

## Safety
Automation (execution) will be built **paper-first** with strict risk limits.
