# Testing and Delivery

## 测试范围

每个新增或修改的业务任务类型至少考虑：

- 正常成功路径
- payload 缺失、空值或类型错误
- 可接受的业务 warning
- 不可重试系统异常或未实现 route
- 路径解析和输出文件内容
- runner 输入输出集成，若变更触及入口或标准结果
- `fail_fast`、`continue_on_error` 或并发行为，若本次需求涉及

测试断言应验证真实结果、输出文件和状态，不要只验证“函数被调用”。

## 推荐验证顺序

1. 运行与改动最接近的单元测试。
2. 运行项目测试集：

```powershell
python -m pytest tests/ -v
```

3. 涉及模板完整性、迁移、Schema 或版本时运行：

```powershell
python tools/doctor.py
```

4. 涉及影刀调用契约时，用脱敏样例执行一次 runner，检查标准结果和业务输出。

命令应以当前项目 README 和工具实际支持为准。

## 契约变更检查

修改以下任一内容时，必须检查所有消费者：

- `tasks[].type`
- payload 字段、默认值或路径
- 业务输出结构或文件名
- runner status、顶层字段或 data 字段
- `run.bat` 参数

至少搜索代码、测试、示例、文档和影刀侧约定。不能只改生产代码。

## Git 工作记录

提交应描述可复查的工程事实，例如：

- 新增了哪个任务类型
- 修改了什么业务契约或异常语义
- 补充了哪些测试
- 修复了哪个可复现问题

不要提交运行产物和敏感数据。是否 commit、push、merge 或发布，由用户明确决定；Agent 不因 Trellis 任务完成而自动执行这些外部动作。

## 完成交付的最低证据

- 契约已确认，或变更严格遵循既有已确认契约。
- 代码、示例、测试和项目文档保持一致。
- 已执行测试并记录结果。
- 如可行，已用 runner 样例验证标准结果和业务输出。
- 影刀侧仍需人工完成的接入或验收项已明确列出。
- 剩余风险和未验证项已说明。

## Stage H 最终校准

业务验收通过后，不要只在聊天里说“完成”。Agent 应执行 Stage H 校准，确认以下证据一致：

| 证据组 | 检查内容 |
| --- | --- |
| Git | 关键代码和文档变化有可追溯 commit；运行产物、日志、真实输入和密钥未提交 |
| 测试 | 相关测试已执行，或说明无法执行的原因 |
| runner | 有可定位的 `run_id` 和 `runner_{run_id}.json`；状态为 `success` 或用户接受的 `warning` |
| 影刀 / 业务 | 影刀真实调用路径清楚，用户已核对业务输出或接受剩余限制 |
| Trellis Task | PRD、设计、计划、Task 状态、证据引用、delivery state、可选 delivery route 和 Final Summary 与实际一致 |
| Project Gate | `.project-gates/project.json` 与 Gate 历史符合用户已接受的项目阶段事实 |
| Base（可选） | 配置了管理 Base 时，其摘要可追溯到 Project Gate Controller、Trellis 和证据系统 |

Stage H 结论只能是：

- `ready`：证据齐全，可按用户授权归档或提交。
- `needs_user_review`：证据存在，但仍需用户确认验收、写入授权、提交、归档或 Base 更新。
- `blocked`：缺少关键证据或运行失败，应说明最小下一步。

不要用测试通过替代业务验收；不要用 Git commit 替代 runner 证据；不要用 Trellis archive 替代 Project Gate；不要用 Base 摘要替代任何权威来源。

## Gate 与 Task 分层记录

项目不必等到最终交付才记录事实，但 Task 和 Gate 必须写入各自的权威来源：

- Trellis Task 记录工程计划、重要发现、阻塞、下一工程动作和证据引用。
- Trellis Task 可记录当前 Issue 的可选 G2-G5 delivery route，但不得复制项目 current_gate；旧 Task 无 route 时仍兼容。
- Project Gate Controller 记录项目 `current_gate`、Gate close 和 G5 后的 revalidation。
- Git/PR 记录代码变化与技术接纳。
- runner 记录目标环境执行结果。
- Base 如启用，只在这些事实保存并回读成功后组合展示。

所有记录只保存必要的脱敏结论和证据指针，不复制完整聊天、payload、日志、客户数据或 Trellis 任务树。

每次 Gate 完成报告必须显式询问：

```text
当前 Gate 是否验收通过，并记录到 Project Gate Controller？
```

配置了 Base 时，用户可另行要求刷新管理展示。Base 缺失或写入失败不能影响 Project Gate、Trellis Task、runner 或业务交付。

## 最终报告

Agent 应简明说明：

- 新增或修改的 `tasks[].type`
- 输入和 payload 变化
- 业务输出路径
- 预期 runner status
- 修改文件和 Git 事实
- 测试命令及结果
- 影刀侧人工检查项
- Trellis Task 状态、证据、下一工程动作和 Final Summary 是否已记录
- Project Gate Controller 当前 Gate 和必要的 close/revalidation 事件是否已记录
- 配置了 Base 时，其展示是否可追溯到权威来源
- 当前是否已完成、待联调或待验收

