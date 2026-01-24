import asyncio
import aiohttp
import nest_asyncio
from datetime import datetime, timezone

# ====== 运行环境（Spyder / Jupyter 需要） ======
nest_asyncio.apply()

# ====== API & 参数 ======
API_BASE = "https://gamma-api.polymarket.com"

THRESHOLD_LOW = 0.98
THRESHOLD_HIGH = 1.02

MAX_MARKETS = 100
INTERVAL = 2  # 秒


# =========================================================
# 1️⃣ 判断：这是不是一个「合法的 Yes/No 市场」
# （注意：这里只做“结构判断”，不做“交易判断”）
# =========================================================
def is_candidate_market(m: dict) -> bool:
    if not isinstance(m, dict):
        return False

    # API 还存在
    if not m.get("active", False):
        return False

    # 被系统彻底归档的，不要
    if m.get("archived", False):
        return False

    # 必须有 Yes / No outcomes
    outcomes = m.get("outcomes", [])
    names = {o.get("name") for o in outcomes if isinstance(o, dict)}
    if not {"Yes", "No"}.issubset(names):
        return False

    return True


# =========================================================
# 2️⃣ HTTP 工具
# =========================================================
async def fetch_json(session, url):
    async with session.get(url, timeout=10) as resp:
        resp.raise_for_status()
        return await resp.json()


# =========================================================
# 3️⃣ 加载市场列表（只做“候选市场”筛选）
# =========================================================
async def load_markets(session):
    params = {
        "active": "true",
        "archived": "false",
        "closed": "false",
        "limit": 200,
    }

    async with session.get(f"{API_BASE}/markets", params=params, timeout=10) as resp:
        resp.raise_for_status()
        data = await resp.json()

    if isinstance(data, list):
        markets = data
    elif isinstance(data, dict):
        markets = data.get("markets", [])
    else:
        markets = []

    return markets


# =========================================================
# 4️⃣ 单市场监控逻辑
# （真正的“交易意义判断”在这里）
# =========================================================
async def monitor_market(session, market):
    market_id = market["id"]
    title = market.get("question", "UNKNOWN")

    url = f"{API_BASE}/markets/{market_id}"

    last_seen_sum = None  # 用来判断价格是否变化

    while True:
        try:
            data = await fetch_json(session, url)

            # 直接判断：如果市场已经 closed 且价格不再变化，跳过
            if data.get("archived", False):
                await asyncio.sleep(INTERVAL)
                continue

            # 提取价格
            prices = {
                o["name"]: o["price"]
                for o in data.get("outcomes", [])
                if isinstance(o, dict) and "name" in o and "price" in o
            }

            if "Yes" not in prices or "No" not in prices:
                await asyncio.sleep(INTERVAL)
                continue

            yes = prices["Yes"]
            no = prices["No"]
            s = yes + no

            # 如果价格长期不变，认为是“死市场”
            if last_seen_sum is not None and abs(s - last_seen_sum) < 1e-6:
                await asyncio.sleep(INTERVAL)
                continue

            last_seen_sum = s

            # 错配报警
            if s < THRESHOLD_LOW or s > THRESHOLD_HIGH:
                print("=" * 60)
                print(f"[ALERT] {title}")
                print(f"YES={yes:.3f}  NO={no:.3f}  SUM={s:.3f}")
                print("=" * 60)

        except Exception as e:
            print(f"[ERROR] {title}: {e}")

        await asyncio.sleep(INTERVAL)


# =========================================================
# 5️⃣ 主入口
# =========================================================
async def main():
    async with aiohttp.ClientSession() as session:
        markets = await load_markets(session)

        print("=" * 80)
        print(f"Loaded {len(markets)} candidate markets")
        print("Monitoring the following markets:")
        print("-" * 80)

        for i, m in enumerate(markets[:MAX_MARKETS], 1):
            print(
                f"{i:02d}. {m.get('question')} "
                f"(id={m.get('id')}, slug={m.get('slug')})"
            )
            web_url = f"https://polymarket.com/market/{m.get('slug')}"
            print(f"    👉 {web_url}")

        print("=" * 80)

        tasks = [
            monitor_market(session, m)
            for m in markets[:MAX_MARKETS]
        ]

        await asyncio.gather(*tasks)



# =========================================================
# 6️⃣ 启动
# =========================================================
if __name__ == "__main__":
    asyncio.run(main())
