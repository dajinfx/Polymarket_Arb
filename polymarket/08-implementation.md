# 08 — Implementation（工程架构）

## 1) 数据层
- 市场元数据（Gamma）
- 盘口/成交（WS）
- 账户：订单/成交/持仓

## 2) OMS（订单管理系统）最低要求
- 幂等下单/撤单
- 状态对账循环（open orders / fills / positions）
- 限速 + backoff
- kill switch + cancel-all 快路径

## 3) Backtest 注意
- 仅用 trade print 很难还原 queue
- 激励机制变化会改变最优策略

## 4) 交付计划
- watchers（提示）优先
- execution（paper）其次
- live（你提供资料后）最后
