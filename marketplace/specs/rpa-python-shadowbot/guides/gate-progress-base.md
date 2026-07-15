# Gate Progress And Optional Base Projection

Use this guide after requirement alignment and before implementation, and again whenever a Gate or high-value milestone is ready for user confirmation.

The goal is to project accepted local Trellis progress into Feishu Base without making Base a prerequisite for project recovery or delivery.

Read `local-progress-tracking.md` first. It defines the canonical Gate route, local snapshot, checkpoint history, and Gate close transaction. This guide only defines the optional Base projection.

## Ownership

```text
Trellis / active Harness = canonical local progress, PRD, plan, evidence, archive
Base project record      = optional human-readable projection of current progress
Base milestone records   = accepted progress events and evidence pointers
Git                      = code and document change evidence
runner / logs            = execution evidence
user                     = business acceptance and authorization
```

Base is an optional cockpit. It should answer where the project is, what was accepted, and what happens next. It must not become another Trellis workspace or the only copy of progress.

## When To Create The Gate Route

After the user agrees that a requirement should enter planning:

1. Create or update the Trellis planning task.
2. Write PRD, design, and implementation plan as needed.
3. Derive a Gate route from the plan.
4. Ask the user to confirm the Gate route before implementation.
5. Save the confirmed route in the Trellis task local progress record.
6. When a project Base is configured, project the route into its long text summary.

Do not start business handler implementation before the contract Gate is confirmed.

## Recommended Gate Route

Adjust names to the project, but keep the number of Gates small. Most RPA projects should use five to seven Gates.

```text
G0 需求对齐
目标：确认业务目标、输入、输出、范围外事项、风险和成功标准。
完成条件：用户确认值得进入规划。

G1 PRD/Plan确认
目标：Trellis 形成 PRD、计划、待确认事项和 Gate 路线图。
完成条件：用户确认计划范围和 Gate。

G2 契约确认
目标：确认 tasks[].type、payload、输出、异常语义、影刀/Python边界和验收样例。
完成条件：用户明确说“需求和契约确认，允许开始实现”。

G3 开发实现
目标：实现 Python handler/service，补测试、示例和必要文档。
完成条件：测试、doctor 或 runner dry-run 通过，并形成可追溯 Git 里程碑。

G4 联调验证
目标：影刀真实调用 run.bat 或 runner.py，生成 run_id 和业务输出。
完成条件：runner 状态可接受，用户核对业务输出或问题边界明确。

G5 业务验收归档
目标：用户确认业务结果，Trellis/Git/runner 完成本地最终校准。
完成条件：验收通过，任务归档；配置了 Base 时同步业务验收结果。
```

Do not use `阻塞/待外部处理` as a replacement Gate in new projects. Preserve the current Gate and project a separate blocker flag or blocker text when the next action belongs to ShadowBot, source data, permissions, upstream systems, or business decision makers. Existing Base records may retain the legacy option until migrated.

## Base Project Record

The project table should have these lightweight fields, or local equivalents:

| Field | Purpose |
| --- | --- |
| `项目全流程Gate备注` | Long text route map with Gates, goals, completion conditions, status, and evidence hints |
| `当前Gate` | Current visible Gate such as `G3 开发实现` |
| `下一步建议` | One short actionable next step and owner |
| `是否阻塞` | Optional independent blocker flag; do not erase the current Gate |
| `阻塞说明` | Optional reason, owner, and unblock condition |

The route text may include status markers, but it is not the detailed development source of truth. Keep detailed PRD, implementation notes, and task history in Trellis or the active Harness.

## Base Milestone Records

Only project high-value local checkpoints. Existing Bases may keep their current event labels while the local Gate remains canonical:

| Event | When to write |
| --- | --- |
| `PRD待确认` | G1 planning evidence is ready for review; after acceptance advance local progress to G2 |
| `允许开发` | User confirms contract and allows implementation |
| `关键Git提交` | A reviewable implementation or fix milestone exists |
| `联调结论` | Real ShadowBot/runner integration succeeds or a problem boundary is accepted |
| `业务验收结果` | User accepts or rejects final business result |

Each event should include:

- linked project
- project id
- Trellis task id, when available
- Gate or stage
- concise desensitized summary
- timestamp or date
- next decision or blocker
- commit hash, when relevant
- run_id, when relevant
- artifact references
- acceptance result
- idempotency key

Do not sync secrets, tokens, full payloads, complete logs, customer-sensitive rows, chat transcripts, or the complete Trellis task tree.

## Confirmation Discipline

For each Gate:

1. Agent reports the completed work and evidence.
2. User accepts, rejects, or requests changes.
3. After acceptance, Agent first updates and reads back local Trellis progress.
4. If Base is configured, Agent projects the accepted checkpoint to Base.
5. If evidence is incomplete, keep the Gate open and record the blocker instead of advancing it.

This keeps Base progress aligned with human acceptance, not just Agent optimism.

## Required Gate Close Prompt

Every Gate completion report should end with an explicit local decision question:

```text
当前 Gate 是否验收通过，并记录到 Trellis？
```

When Base is configured, add:

```text
是否同时同步到飞书 Base？
```

Local recording is required even if the user did not mention Base. Base synchronization is optional and must not be invented when no target record is configured.

If the user requests Base sync but the project record is missing, ask for it:

```text
我可以准备本次 Base 摘要，但还缺项目管理 Base 的项目记录链接或 record_id。
```

After the user confirms, first update:

- local `task.json.meta.progress`
- local task `progress.md`

Then, when Base is configured, update:

- project `当前Gate`
- project `下一步建议`
- one Base milestone event for the accepted Gate

Do not continue to the next Gate as if the previous one is closed when the local confirmation and write-back have not happened.

## Idempotency

Use stable keys so repeated sync attempts do not create duplicate records:

```text
<project_id>/<trellis_task_id>/<event_type>/v<version>
```

When the Gate route changes materially, update the project route text and either increment the relevant event version or record a new accepted milestone.

## Anti-Patterns

- Do not create one Base record for every small code edit.
- Do not use Base as the only copy of PRD or implementation details.
- Do not let Base failure block `run.bat`, `runner.py`, or business handlers.
- Do not mark a Gate complete before user acceptance when the Gate requires business judgment.
- Do not omit local Trellis recording just because implementation or tests passed.
- Do not require a Base link when the project is intentionally local-only.
- Do not treat a legacy `.rpa_ai/handoff` file as the authority for harness-independent projects.
