# Logging and Output

## 运行产物

每次运行应通过 `run_id` 关联以下证据：

| 产物 | 默认位置 | 用途 |
| --- | --- | --- |
| 标准结果 | `runner_{run_id}.json` | 影刀分支和运行摘要 |
| 日志 | `logs/run_{run_id}.log` | 执行过程和任务定位 |
| 异常快照 | `crash_snapshots/crash_{run_id}.json` | 系统异常诊断 |
| 业务输出 | `data/output/` | 供影刀或业务方继续使用 |

具体路径以当前项目实现为准，但不得让多个并发 run 相互覆盖关键证据。

## 日志规则

- 日志至少能关联 `run_id`、项目和任务。
- 记录任务开始、结束、状态和必要摘要，不重复写入完整大文件内容。
- 错误日志提供定位信息，但用户可见消息应保持可行动、可理解。
- 不记录密钥、Cookie、Authorization、完整账号信息或敏感客户数据。
- 日志不是影刀的控制协议；影刀控制分支只读 runner JSON。

## 业务输出规则

- 默认写入 `data/output/`。
- 文件名应稳定且可由 payload 明确指定，避免依赖当前时间等隐式规则，除非契约已定义。
- 先完成写入，再在 handler 摘要中返回输出路径。
- 对关键输出考虑原子写入或临时文件替换，避免半写文件被影刀读取。
- 输出格式变化属于契约变化，必须同步示例、测试和影刀消费逻辑。

## Runner 结果规则

- 保持顶层 `status`、`message`、`data` 稳定。
- 业务详情放入对应 `results[].data`，warnings 和 errors 保持结构化。
- `message` 是摘要，不承载完整诊断。
- traceback 和详细环境信息保留在日志或快照，不暴露给影刀分支。
- 输出必须可被标准 JSON 解析，避免 NaN、二进制或自定义对象。

## 异常快照规则

快照用于让 Agent 复现和定位问题，适合包含：

- `run_id`、环境、输入文件和任务上下文
- 错误类型、异常分类、action、expected、actual
- 代码位置和 traceback
- 必要且已脱敏的 payload 摘要

截图路径、页面信息等只在当前项目确实由上游提供时记录，不强迫 Python 直接控制页面。

## Git 忽略与清理

运行产物通常不得提交：

- 根目录 `input*.json`
- `runner_*.json`
- `logs/`
- `crash_snapshots/`
- `data/` 中的运行数据
- `.runner.lock`

可提交的是脱敏、稳定、专门用于测试或文档的 fixture 和示例文件。

