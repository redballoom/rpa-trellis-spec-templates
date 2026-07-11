# Runner Contract

## 适用范围

新增业务、调整影刀调用参数、修改输入文件、状态码或 `runner_{run_id}.json` 时使用。

## 启动契约

推荐由影刀调用：

```bat
run.bat {run_id} {work_dir} {input_file}
```

等价 Python 参数以当前项目 `runner.py --help` 和 `run.bat` 为准。稳定参数通常包括：

- `run_id`：由影刀或 BAT 通过命令行传入，是本次运行的唯一关联键。
- `repo_path`：项目根目录。
- `work_dir`：影刀本次运行的工作目录，可选。
- `input_file`：本次运行的结构化输入文件，可选。

不要依赖输入 JSON 顶层的 `run_id` 覆盖命令行参数。

## 输入契约

推荐每次运行生成独立文件 `input_{run_id}.json`。固定 `input.json` 只允许单实例串行兼容场景使用。

```json
{
  "project": "文件汇总项目",
  "tasks": [
    {
      "id": "task-001",
      "name": "合并文件",
      "type": "merge_excel",
      "payload": {
        "source_files": ["data/input/a.xlsx"],
        "output_file": "data/output/summary.xlsx"
      }
    }
  ],
  "context": {
    "operator": "yingdao",
    "env": "test",
    "source": "shadowbot",
    "app_name": "文件汇总项目",
    "fail_fast": true
  }
}
```

稳定规则：

- `project` 和 `tasks` 按当前 Schema 要求提供。
- 使用 `tasks[].type` 路由，不按 `name` 路由。
- 业务参数只放入 `tasks[].payload`。
- `context.env` 应明确区分测试与生产。
- 有依赖关系的任务保持 `fail_fast=true`。
- 只有彼此独立、重复执行无副作用的批任务，才考虑 `fail_fast=false` 或 `continue_on_error=true`。

## 并发契约

- 输入、runner 结果、日志和快照都应按 `run_id` 隔离。
- `.runner.lock` 只保护 Python 执行阶段，不能保护影刀写固定 `input.json` 的阶段。
- 影刀遇到 `locked` 应等待后重试，不先修改 Python 业务代码。

## 标准输出

Python 默认写出项目根目录的 `runner_{run_id}.json`：

```json
{
  "status": "success",
  "message": "处理完成",
  "data": {
    "run_id": "rpa_001",
    "results": [],
    "warnings": [],
    "errors": [],
    "retryable": false,
    "crash_snapshot_dir": "",
    "log_path": "logs/run_rpa_001.log"
  }
}
```

影刀可消费 `status`、`message` 和 `data` 中的结构化字段，但不应解析 Python traceback。

## 状态语义

| status | 含义 | 默认影刀动作 |
| --- | --- | --- |
| `success` | 所有任务成功 | 继续后续流程 |
| `warning` | 有可接受的业务跳过或非阻断问题 | 记录后继续，必要时人工检查 |
| `retryable_error` | 临时系统异常，可重试 | 延迟后按策略重试 |
| `pending_fix` | 不可重试的系统问题，需要修复 | 停止并进入修复闭环 |
| `failed` | runner 级不可恢复失败 | 停止并通知人工 |
| `locked` | 同项目并发锁冲突 | 等待后重试 |
| `fatal` | 入口参数、输入、配置或启动级错误 | 停止并通知维护人员 |

## 禁止事项

- 未经明确约定修改 `run.bat` 参数顺序或 runner 顶层字段。
- 让影刀从控制台文本或 traceback 判断业务分支。
- 多个并发流程共同覆盖固定 `input.json`。
- 把 Base、Trellis、Git 平台或外部工单成功与否作为 runner 成功的必要条件。

## 事实来源

安装到具体项目后，核对：`run.bat`、`runner.py`、`schemas/input.schema.json`、`docs/SHADOWBOT_INPUT_CONTRACT.md` 和 runner 相关测试。

