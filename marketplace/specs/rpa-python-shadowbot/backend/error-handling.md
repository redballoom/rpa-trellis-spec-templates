# Error Handling

## 目标

异常分类的目的，是让影刀知道下一步该继续、重试、停止还是交给 Agent 修复，而不是隐藏失败。

## 业务异常

使用项目的 `BusinessException` 表达可接受、可解释、通常可跳过的业务情况，例如：

- 输入数据为空
- 单条记录格式不合法
- 业务规则阻断
- 订单或目标记录不存在
- 重复记录需要跳过

业务异常通常进入 `warnings`，对应任务标记为 skipped，整体通常为 `warning`。

```python
raise BusinessException(
    "payload.source_files is empty",
    project=project,
    context={"payload": payload},
    code="DATA_EMPTY",
    suggested_action="请由影刀提供至少一个输入文件",
)
```

不要用业务异常掩盖代码缺陷、依赖失败或契约未实现。

## 系统异常

使用项目的 `SystemException` 表达代码、规则、环境、依赖和第三方问题，例如：

- `RULE_MISSING`：路由或业务规则缺失
- `DEPENDENCY_FAILURE`：网络或外部依赖临时故障
- `ENVIRONMENT_ISSUE`：依赖、权限、磁盘或运行环境问题
- `LOGIC_DEFECT`：代码逻辑缺陷
- `DATA_QUALITY`：输入虽符合外形但无法满足系统处理要求
- `THIRD_PARTY_LIMIT`：第三方限流、配额或限制

```python
raise SystemException(
    message="外部接口超时",
    project=project,
    payload=payload,
    action="调用外部接口",
    expected="在超时时间内返回成功响应",
    actual="请求超时",
    code="NETWORK_TIMEOUT",
    exc_category="DEPENDENCY_FAILURE",
    retryable=True,
    run_context=context,
)
```

## Retryable 判断

只有满足以下条件时设置 `retryable=True`：

- 失败由临时资源状态导致。
- 原输入重复执行是安全的，或业务已有幂等保护。
- 重试有合理成功概率。
- 影刀有明确的重试次数、间隔和失败出口。

数据永久缺失、规则未实现、代码缺陷和参数错误不应标记为可重试。

## Fatal 与 Failed

- 输入文件缺失、JSON 非法、基础配置致命错误通常由 runner 返回 `fatal`。
- runner 自身未能完成标准业务执行时可能返回 `failed` 或 `fatal`，以当前实现为准。
- handler 不应随意制造入口级状态；它应抛出项目定义的业务或系统异常。

## Fix Target

如果当前项目输出 `fix_target`，优先使用：

| fix_target | 处理方向 |
| --- | --- |
| `python` | 修改 Python 代码、测试或项目文档 |
| `rpa` | 调整影刀输入、页面流程或调度动作 |
| `upstream` | 处理外部系统、权限、网络或数据源 |

若项目尚未实现 `fix_target`，Agent 应根据证据判断边界并说明置信度，不得虚构字段。

## 可选外部集成

通知、AI 分析、飞书 Base 或工单创建失败，不应自动改变核心异常语义。外部集成必须能够优雅降级，runner 状态仍由实际业务执行结果决定。

## 禁止事项

- `except Exception: return success`。
- 把不可重试的系统异常降级成 warning。
- 让影刀解析 traceback。
- 未验证幂等性就自动重试。
- 为了适配某个 Harness，在异常类中写入任务状态机逻辑。

