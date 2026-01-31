# 07 — Risk Management（风控）

## 1) 仓位限制
- 单市场：max YES/max NO/max net
- 单事件簇：例如同一选举/同一赛事日程
- 单主题：politics/sports/crypto 等

## 2) 尾部风险
- news-jump kill switch（自动撤单）
- 波动 regime 切换（扩大价差、减 size）
- 临近结算缩仓（若定义风险升高）

## 3) PnL 拆解
- spread capture
- inventory MTM
- 激励收入
- 手续费/滑点

## 4) 运维风险
- 断线/不同步 → 主动 reconcile
- 限速/失败重试
- 密钥安全
