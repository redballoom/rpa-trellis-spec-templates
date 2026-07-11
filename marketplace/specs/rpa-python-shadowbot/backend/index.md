# Python Backend Guidelines

本目录定义影刀调用 Python Code 项目时的稳定工程规范。

## 开发前检查

- [ ] 已读取当前项目 `README.md`、`AGENTS.md` 和相关 `docs/`
- [ ] 已核对 `schemas/input.schema.json` 和现有 handler
- [ ] 已确认影刀提供什么、Python 输出什么
- [ ] 已定义 `tasks[].type`、`payload`、业务输出和异常语义
- [ ] 用户已明确确认业务契约，或当前任务只是分析/起草契约

## 规范索引

| 规范 | 适用场景 |
| --- | --- |
| [Runner Contract](./runner-contract.md) | 修改入口、输入结构、状态或标准输出 |
| [Handler Patterns](./handler-patterns.md) | 新增或修改业务任务类型 |
| [Error Handling](./error-handling.md) | 设计 warning、重试、待修复和致命错误 |
| [Logging and Output](./logging-and-output.md) | 业务输出、日志、快照和运行产物 |
| [Testing and Delivery](./testing-and-delivery.md) | 测试、验收、Git 记录和交付报告 |

## 质量检查

- [ ] 未修改稳定 runner 协议，或已获得明确确认并同步测试、文档和影刀分支
- [ ] 新增 `tasks[].type` 已有 handler、示例输入和测试
- [ ] 相对路径以项目 `repo_path` 为基准解析
- [ ] 业务输出默认写入 `data/output/`
- [ ] 未提交运行产物、密钥、账号、Cookie 或个人绝对路径
- [ ] 已执行相关测试；无法执行时已说明原因和风险

