# Handler Patterns

## 适用范围

新增 `tasks[].type`、修改 payload 或拆分业务模块时使用。

## 路由规则

- 路由键必须来自 `task.get("type")`。
- `task.name` 只用于显示和日志，不参与业务分支。
- 未实现的非空 type 必须返回系统异常，不能假成功。
- `template_demo` 等模板演示路由不得作为真实业务路由。

简单业务可在现有入口增加小型 handler；中大型业务应放入项目已有的 `core/handlers/`、`core/services/` 或同类模块，再由入口路由。

```python
def process_example(task, context):
    payload = task.get("payload") or {}
    repo_path = context.get("repo_path") or "."
    project = context.get("project", "RPA")

    # 1. 校验 payload
    # 2. 读取业务输入
    # 3. 执行确定性处理
    # 4. 写出业务结果
    # 5. 返回结果摘要
```

## Payload 规则

- handler 的业务参数只从 `task["payload"]` 读取。
- 每个字段要定义：名称、类型、必填性、默认值、示例、路径规则和空值语义。
- 不从 `task.name`、临时环境变量或个人目录推断业务参数。
- 业务变化优先扩展 payload，不轻易改变 runner 顶层协议。
- 敏感信息使用项目认可的安全配置方式，不进入输入样例或 Git。

## 路径规则

- 相对路径以 `context["repo_path"]` 为基准解析。
- 业务输入默认位于 `data/input/`，输出默认位于 `data/output/`，临时文件位于 `data/temp/`。
- 输出目录不存在时由 Python 创建。
- 不硬编码影刀临时目录或开发者个人绝对路径。
- 返回给影刀或结果 JSON 的路径应保持项目可理解的相对路径，除非契约明确要求绝对路径。

## 返回规则

handler 返回可序列化的摘要，由 runner 放入对应 `results[].data`。大文件或完整业务数据写入业务输出文件，摘要只保留：

- 输出文件路径
- 记录数、成功数、跳过数等统计
- 后续影刀确实需要的少量结构化字段

不要把大量业务数据、二进制内容或 traceback 塞进 runner 结果。

## 拆分判断

满足任一条件时优先拆出独立模块：

- handler 已包含多个可独立测试的处理阶段。
- 相同转换或校验被多个 type 复用。
- 文件读取、领域规则和输出组装混在一起，测试困难。
- 单个入口文件开始承载多个无关业务。

不要为一个短小、单用途转换过早创建复杂抽象。

## 每个新任务类型的完整产物

- handler 路由和实现
- `input_{run_id}.json` 示例
- payload 字段说明
- 正常路径测试
- 关键业务 warning 测试
- 系统异常或边界测试
- 预期业务输出和 runner status

## 禁止事项

- 只更新文档但不实现 route。
- 捕获所有异常后返回 success。
- 在 Python handler 内执行应由影刀负责的页面点击、验证码或人工确认。
- 为了绕过契约问题，直接读取影刀内部变量或未声明的固定文件。

## 事实来源

安装到具体项目后，搜索 `tasks[].type` 的路由实现、现有 handler、示例输入和对应测试，以实际模式为准。

