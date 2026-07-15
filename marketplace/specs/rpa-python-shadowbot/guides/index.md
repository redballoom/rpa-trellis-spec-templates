# RPA Development Guides

这些指南帮助 Agent 在编码前先判断契约、职责边界和故障归属。

## 指南索引

| 指南 | 何时使用 |
| --- | --- |
| [Requirement to Contract](./requirement-to-contract.md) | 业务方提出新需求或改变输入输出时 |
| [ShadowBot Boundary](./shadowbot-boundary.md) | 不确定逻辑应放在影刀还是 Python 时 |
| [Fix Loop](./fix-loop.md) | runner 失败、重复重试或输出不符合预期时 |
| [Local Progress Tracking](./local-progress-tracking.md) | 需要跨会话恢复、记录当前 Gate、检查点、下一步或阻塞时 |
| [Gate Progress And Optional Base Projection](./gate-progress-base.md) | 已有本地检查点，需要将已接受进度投影到 Base 时 |

## 快速判断

```text
新需求
  -> 先拆影刀 / Python / 人的职责
  -> 定义 input、type、payload、output、status、acceptance
  -> 生成 Gate 路线图并写入 Trellis 本地进度
  -> 用户确认契约
  -> Agent 实现并测试
  -> 用户完成影刀接入和业务验收
  -> 每个 Gate 验收后记录本地检查点
  -> 配置了 Base 时再同步管理里程碑

运行失败
  -> 收集 input + runner + log + snapshot + 样例
  -> 判断 rpa / input / python / environment / upstream
  -> 修复最小正确范围
  -> 测试 + runner 回归
  -> 再交回影刀联调
  -> 修复 Gate 验收后同步问题边界或关键提交摘要
```

## 更新原则

当真实项目在实现或排障中形成新的跨项目稳定规则，可更新项目 `.trellis/spec/`。只有经过多个项目验证、且不包含私有业务字段的规则，才适合回收进公共模板。

