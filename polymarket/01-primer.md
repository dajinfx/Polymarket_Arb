# 01 — Primer: Polymarket (CLOB / Gamma) — 基础概念

> 目的：把 Polymarket 当作一个“订单簿交易所”来理解，而不是 AMM。

## 1) 产品与结算
- 二元市场（Yes/No share）价格近似“隐含概率”。
- 结算时：某一边 payout=1，另一边=0（按规则/时间/数据源）。
- 预测市场的典型风险：信息跳变（news jump）+ 规则解释风险（definition risk）。

## 2) CLOB vs AMM
- **CLOB**：通过挂单提供流动性，竞争点是 **价差、队列位置、更新速度、库存管理**。
- **AMM**：靠曲线交易；旧 AMM 策略在 CLOB 下常需要重写成“订单簿版本”。

## 3) 数据与接口（待你提供交易资料后完善）
- 市场列表/详情（Gamma API）
- 订单簿/成交（WebSocket/REST）
- 下单/撤单/查持仓（CLOB client / API）

## 4) 本仓库当前关注
- 新市场发现（Yes/No、新建 < N 天、按类目）
- 简单一致性扫描（Yes+No < 1 的理论套利候选）
