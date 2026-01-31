# 02 — Order Book Dynamics（订单簿微观结构）

## 1) Spread / Depth / Queue
- spread 变窄时，优势从“价差”转向“激励 + 更新 + 库存控制”。
- queue（通常是价格-时间优先）：同价位越早越靠前；频繁撤挂会丢队列。
- depth：二元市场常在 0.4/0.5/0.6 等整数概率附近堆量。

## 2) 预测市场的逆向选择（adverse selection）
- 新闻事件导致跳变：maker 容易被“打掉”。
- 规则解释/数据源变化也会引发跳变。

## 3) 你会遇到的对手盘 bot 模式
- tick-sniping（1 tick 抢最优）
- refresh-walling（展示后快速撤）
- latency-arb（外部信息更快）

## 4) 对应工程要求
- 断线/延迟检测 → 立即 cancel-all
- 更新频率与队列损失的权衡
