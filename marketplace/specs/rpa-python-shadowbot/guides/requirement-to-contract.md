# Requirement to Contract

## 原则

新业务的第一份交付物是可确认的输入输出契约，不是代码。除非用户已经给出完整且明确的既有契约，否则 Agent 应先起草并等待明确确认后再实现。

## 第一步：理解业务目标

先确认：

- 业务最终要得到什么结果。
- 影刀当前已经完成哪些页面、登录、下载、上传或调度动作。
- Python 将收到哪些文件和参数。
- 哪些判断需要人工确认。
- 成功、跳过、可重试、待修复分别意味着什么。

不要在需求不清时通过猜测字段直接编码。

## 第二步：划分职责

- 需要页面状态、登录、验证码、下载上传或人工交互：影刀。
- 可由结构化输入稳定复现、需要测试和复用：Python。
- 需求确认、上线决策和业务验收：用户。
- 契约、Python 实现、测试、文档和故障证据整理：Agent。

详细判断见 [ShadowBot Boundary](./shadowbot-boundary.md)。

## 第三步：起草契约

使用以下结构：

```markdown
## 业务契约草案

### 业务目标
- 最终结果：
- 成功标准：

### 影刀需要提供
- input_file: input_{run_id}.json
- business files:
- context fields:

### Python 任务路由
- tasks[].type:
- handler location:

### payload 字段
| 字段 | 必填 | 类型 | 示例 | 默认值/空值语义 | 说明 |
| --- | --- | --- | --- | --- | --- |

### 输出
- business output:
- runner output:
- status expectation:

### 异常语义
- BusinessException:
- SystemException:
- retryable:
- boundary/fix target:

### 验收
- sample input:
- expected output:
- tests:
- ShadowBot manual check:
```

## 第四步：确认契约

在以下内容未明确前，不进入 handler 实现：

- `tasks[].type`
- payload 必填字段和示例
- 输入、输出路径
- 空数据和错误数据处理
- runner status 预期
- 影刀接下来如何消费结果
- 最小验收样例

用户可用“契约确认，开始实现”等明确表达进入实现阶段。

## 第五步：实现与同步

确认后：

1. 实现 route 和 handler。
2. 添加脱敏示例输入。
3. 添加正常、warning 和系统边界测试。
4. 更新项目文档中的 payload 和输出说明。
5. 运行测试和 runner 样例。
6. 报告影刀侧仍需完成的接入步骤。

## 变更中的契约

联调发现契约需要调整时，先把变化写回契约和示例，再修改代码。不要让聊天中的临时决定成为唯一事实来源。

