# Sources and Maintenance Boundary

## 第一版提炼基线

记录日期：2026-07-11

| 资产 | 基线 |
| --- | --- |
| `rpa-dev-template` 独立化分支 | `codex/harness-independent-template` |
| `rpa-dev-template` 基线提交 | `da4927e` |
| `rpa-dev-template-skills` 独立化分支 | `codex/harness-independent-skills` |
| `rpa-dev-template-skills` 基线提交 | `b05fb88` |

主要事实来源：

- `README.md`
- `AGENTS.md`
- `run.bat`、`runner.py`
- `core/entry.py`、`core/exceptions.py`
- `schemas/input.schema.json`
- `docs/SHADOWBOT_INPUT_CONTRACT.md`
- `docs/RPA_PYTHON_BOUNDARY.md`
- `docs/OPERATION_GUIDE.md`
- `docs/ISSUE_FIX_WORKFLOW.md`
- `docs/ACCEPTANCE_CHECKLIST.md`
- `rpa-contract-business/SKILL.md`
- `rpa-fix-loop/SKILL.md`
- `rpa-project-bootstrap/SKILL.md`

## 维护规则

1. 运行行为变化先在 `rpa-dev-template` 中通过代码、测试和文档完成，再更新本 Spec。
2. Skill 工作顺序变化先在 `rpa-dev-template-skills` 中确认，再更新本 Spec 的相关指南。
3. 本 Spec 不反向要求模板依赖 Trellis，也不拥有 runner 状态机。
4. 外部通知、Base、工单和 Agent 平台都按可选集成描述。
5. 从单个业务项目回收规则前，确认它可跨项目复用且不包含私有字段或数据。
6. `index.json` 与 `marketplace/index.json` 应保持一致，前者用于 Trellis CLI registry 发现，后者用于 marketplace 结构表达。

## 漂移检查

模板或 skills 发布新版本后，至少核对：

- `run.bat` 参数是否变化
- `schemas/input.schema.json` 是否变化
- runner 顶层字段和状态码是否变化
- handler 路由和路径解析方式是否变化
- 异常类、错误分类和重试语义是否变化
- 测试与验收命令是否变化
- skills 是否改变“先契约、后实现”和故障证据读取顺序

只有确认变化属于跨项目稳定规则后，才更新公共 Spec。
