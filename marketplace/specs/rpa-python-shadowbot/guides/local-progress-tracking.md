# Local Progress Tracking

Use this guide when an RPA project must recover its project Gate and engineering work across Agent sessions.

The recovery view must answer these questions without relying on chat history:

1. Which project Gate is current, and what Gate events were accepted?
2. Which Trellis Task is active, planned, blocked, or awaiting review?
3. What was the latest verified engineering result?
4. What happens next, and who owns that action?
5. Which Git, PR, test, runner, or business evidence supports the state?

## Authority

```text
Project Gate Controller .project-gates/project.json       = project current Gate
Project Gate Controller .project-gates/gate-history.md    = accepted Gate close and revalidation events
Trellis .trellis/tasks/           = engineering Task lifecycle and artifacts
Trellis .trellis/workspace/       = cross-session engineering journal
Git / PR                          = code version and technical acceptance
runner / logs                     = target-environment execution evidence
Gitea Issue                       = original requirement and discussion
```

One fact has one writer. Do not copy `current_gate` into `task.json`, Task metadata, Task notes, workspace journals, Base, or `.rpa_ai/handoff`.

Trellis Task metadata may contain Task-owned delivery fields such as `delivery_state`, Issue/PR references, runner references, blocker detail, and next engineering action. It must not contain a second project Gate snapshot or Gate history.

## Project Gates

Project Gate Controller owns exactly one project route:

```text
G0 目标与边界
G1 交付规格
G2 契约与验收基线
G3 实现与技术验证
G4 目标环境验证
G5 业务验收与发布
```

The project Gate advances only forward. Each Gate is formally closed once. After G5, later major changes keep the project at G5 and append a `gate-revalidation` event; they do not rewind `current_gate` or rewrite prior history.

Blocking is orthogonal to the project Gate. Keep the Project Gate unchanged and record the Task-owned blocker in Trellis. A blocked Task does not create a new Gate.

## Trellis Task Progress

Trellis is the only engineering Task authority. Store these facts in the Task artifacts or supported `task.json.meta` fields:

- confirmed goal, context, scope, and Acceptance Criteria;
- PRD, design, and implementation plan as required by complexity;
- important implementation findings, blockers, and recovery point;
- Issue, PR, commit, test, runner, and decision references;
- `delivery_state` such as `paused`, `blocked`, or `in_review` when the Project Gate Controller adapter defines it;
- final engineering summary before archive.

Do not create a parallel Task checkpoint system. Agent-native Todo remains free for current-session steps; only cross-session facts belong in Trellis.

Trellis may create a system Task such as `00-bootstrap-guidelines`. Never treat it as the business delivery Task or use it to infer the project Gate.

## Recovery Order

On a new session, read in this order:

1. Project Gate Controller `status`, or `.project-gates/project.json` and the latest Gate history event.
2. Trellis current Task and all `planning` / `in_progress` Tasks.
3. The selected Task's PRD, design, implementation plan, notes, metadata, and final summary.
4. The linked Gitea Issue and PR.
5. Git branch, working tree, and recent commits.
6. Relevant tests, runner result, logs, and target-environment evidence.
7. Long-term project decisions and constraints.

If Project Gate Controller and Trellis disagree, do not choose the newest chat statement. Report the exact conflict and preserve both sources until the responsible writer is corrected.

If `.project-gates/` is missing, report that project Gate tracking has not been bootstrapped. Do not infer or write a Gate into Trellis as a fallback.

## Gate Close Discipline

For a Gate that requires user judgment:

1. Read the current Project Gate and relevant Trellis Task.
2. Report the result, evidence, remaining risk, and proposed next Gate.
3. Ask: `当前 Gate 是否验收通过，并记录到 Project Gate Controller？`
4. After explicit acceptance, call the Project Gate command or update its schema-governed files.
5. Read back the new Project Gate Controller state.
6. Update only Task-owned facts in Trellis, such as evidence references or `delivery_state`.

Task archive, Issue close, PR merge, Gate close, and release are separate events. Never let a Trellis archive operation close or advance a Gate implicitly.

## Archive Guard

Trellis archive is a technical operation and does not enforce the delivery evidence required by this workflow. Before archive, the Project Gate Controller delivery adapter must verify the evidence required for that Task, including as applicable:

- Acceptance Criteria and technical checks;
- commit and PR state;
- test and runner evidence;
- target-environment result;
- required user acceptance;
- final summary and remaining risks.

Keep `session_auto_commit: false` in `.trellis/config.yaml` so archive and journal operations do not commit without user authorization.

## Migration From The Previous Model

Older projects may contain project Gate files under `.hermes/`, or `task.json.meta.progress.current_gate` / Task-local `progress.md` used as project Gate state.

Migration rules:

1. Treat those files and fields as legacy input, not current authority.
2. If `.hermes/project.json` exists, stop bootstrap and Gate writes until an explicitly confirmed storage migration moves only the two Gate files to `.project-gates/`.
3. Preserve `.hermes/plugins/` and every other Hermes Agent file.
4. Compare Task-local Gate facts with Git, runner, Issue, PR, and explicit user acceptance.
5. Create or verify `.project-gates/project.json` and append an explicit migration/recovery event after user awareness.
6. Remove the legacy Gate fields from active Task metadata after migration.
7. Preserve historical files through Git history; do not keep them synchronized.

Do not maintain a compatibility writer after migration.
