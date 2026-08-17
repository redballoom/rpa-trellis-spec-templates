# RPA Development Guides

这些指南帮助 Agent 在编码前先判断契约、职责边界和故障归属。

## 指南索引

| 指南 | 何时使用 |
| --- | --- |
| [Requirement to Contract](./requirement-to-contract.md) | 业务方提出新需求或改变输入输出时 |
| [ShadowBot Boundary](./shadowbot-boundary.md) | 不确定逻辑应放在影刀还是 Python 时 |
| [Fix Loop](./fix-loop.md) | runner 失败、重复重试或输出不符合预期时 |
| [Local Progress Tracking](./local-progress-tracking.md) | 需要跨会话组合恢复 Project Gate、Trellis Task 和证据时 |
| [Gate Progress And Optional Base Projection](./gate-progress-base.md) | 项目明确配置 Base，只读展示权威状态时 |

## 快速判断

```text
新需求
  -> 先拆影刀 / Python / 人的职责
  -> 定义 input、type、payload、output、status、acceptance
  -> 在 Trellis Task 中形成 PRD、设计和计划
  -> 在 Project Gate Controller 中确认项目 Gate 与验收基线
  -> 用户确认契约
  -> Agent 实现并测试
  -> 用户完成影刀接入和业务验收
  -> 每个 Gate 验收后只写入 Project Gate 历史
  -> 配置了 Base 时再组合展示 Project Gate Controller、Trellis 和证据

运行失败
  -> 收集 input + runner + log + snapshot + 样例
  -> 判断 rpa / input / python / environment / upstream
  -> 修复最小正确范围
  -> 测试 + runner 回归
  -> 再交回影刀联调
  -> 在 Trellis Task 记录修复证据，必要时由 Project Gate Controller 记录 Gate 复核
```

## 更新原则

当真实项目在实现或排障中形成新的跨项目稳定规则，可更新项目 `.trellis/spec/`。只有经过多个项目验证、且不包含私有业务字段的规则，才适合回收进公共模板。

