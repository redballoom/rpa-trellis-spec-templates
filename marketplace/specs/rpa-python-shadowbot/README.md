# RPA Python + ShadowBot Spec

本 Spec 面向从 `rpa-dev-template` 初始化的项目，帮助 Agent 在新需求、实现、联调和故障修复时保持一致的工程边界。

## 权威顺序

规则发生冲突时，按以下顺序判断：

1. 当前项目可执行代码和自动化测试
2. 当前项目 `schemas/input.schema.json`
3. 当前项目 `README.md`、`AGENTS.md` 和 `docs/`
4. 当前安装的项目级 `.trellis/spec/`
5. 本公共模板的原始内容

本 Spec 是开发指导，不得覆盖实际运行契约。发现漂移时，应先核对代码和测试，再更新项目级 Spec。

## 开发前最小阅读路径

- 新业务：`guides/requirement-to-contract.md` -> `backend/runner-contract.md` -> `backend/handler-patterns.md`
- Trellis Task / Hermes Gate 恢复：`guides/local-progress-tracking.md`
- 飞书 Base 只读组合展示：`guides/gate-progress-base.md`
- 影刀和 Python 分工不清：`guides/shadowbot-boundary.md`
- 异常或状态设计：`backend/error-handling.md`
- 输出、日志和验收：`backend/logging-and-output.md`、`backend/testing-and-delivery.md`
- 运行失败：`guides/fix-loop.md`

## 核心原则

- 先确认契约，再实现 handler。
- 影刀负责 UI 和调度，Python 负责可复现、可测试的业务处理。
- `tasks[].type` 是路由键，`task["payload"]` 是业务参数入口。
- 影刀只根据标准 runner 结果分支，不解析 Python traceback。
- 不把 Trellis、Base、Git 平台或外部工单系统变成 Python 运行依赖。
- 没有测试或运行证据时，不宣称交付完成。
- Trellis 只管理工程 Task；项目 G0-G5 经用户确认后只记录到 Hermes。Base 如启用，只组合展示权威来源。

