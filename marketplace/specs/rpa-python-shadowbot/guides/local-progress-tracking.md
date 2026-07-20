# Local Progress Tracking

Use this guide whenever an RPA project needs durable progress tracking across AI sessions, including projects that do not use Feishu Base.

The local record must answer five questions without reading chat history:

1. Which Gate is currently waiting to close?
2. What is the Agent working on now?
3. What was the latest verified checkpoint?
4. What happens next, and who owns that action?
5. Is the project blocked, and what evidence supports the current state?

## Authority

```text
Trellis task.json             = current task lifecycle and local progress snapshot
Trellis task progress.md      = append-only checkpoint history
PRD / design / implement      = requirement, contract, and plan
Git                           = code and document evidence
runner / logs                 = execution evidence
Feishu Base, when configured  = optional management projection
```

Do not create another lifecycle file such as `.rpa_ai/handoff/current.json` for new harness-independent projects. Do not make `run.bat`, `runner.py`, or handlers read Trellis progress files.

## Canonical Gates

Use exactly one human-facing project progress route:

```text
G0 需求对齐
G1 PRD/Plan确认
G2 契约确认
G3 开发实现
G4 联调验证
G5 业务验收归档
```

`current_gate` means the Gate currently waiting to close, not the last accepted Gate. After the user accepts G2, record the G2 decision and advance `current_gate` to G3.

Blocking is orthogonal to Gate progress. Keep `current_gate` unchanged and set `blocked=true` with a reason and owner. Do not replace the current Gate with a generic blocked Gate.

The Gate route is a canonical trunk, not a blind conveyor belt. Before writing progress, inspect local facts first: Trellis task lifecycle, `task.json.meta.progress`, `progress.md`, Git evidence, runner outputs, and user acceptance. The default accepted-Gate path advances sequentially, but stale or contradictory records should be handled with an explicit `recovery` calibration, and reopened work should be recorded as a new checkpoint with a clear reason instead of overwriting history.

Recommended command discipline when the `rpa-delivery-close` skill scripts are available:

```powershell
trellis init --registry gh:redballoom/rpa-trellis-spec-templates/marketplace --template rpa-python-shadowbot --codex
python <skill-dir>\scripts\rpa_collab.py --project-root <project-root> bootstrap --project-name "<name>"
python <skill-dir>\scripts\rpa_collab.py --project-root <project-root> status
python <skill-dir>\scripts\rpa_collab.py --project-root <project-root> suggest
```

Use `bootstrap` only to attach a newly initialized code project to local collaboration tracking. The normal path requires a full Trellis workspace with `.trellis/spec`; do not create a task-only `.trellis` directory for formal projects. The bootstrap step should create or recognize the delivery task and write an initial G0/G1 snapshot when missing. If progress already exists, preserve it and read back status instead of overwriting. Only after the read-only status check should the Agent propose `checkpoint`, `gate-close`, `recovery`, or `finish`.

## Snapshot Schema

Store the current local snapshot under `task.json.meta.progress`. Preserve all other Trellis fields and existing `meta` content.

```json
{
  "meta": {
    "progress": {
      "schema_version": 1,
      "current_gate": "G3",
      "current_work": "实现业务 handler 和字段校验",
      "latest_checkpoint": "核心实现完成，相关测试通过",
      "next_action": "执行 runner dry-run",
      "next_owner": "agent",
      "blocked": false,
      "block_reason": "",
      "updated_at": "2026-07-15T14:30:00+08:00",
      "checkpoint_id": "checkpoint-g3-implementation-v1",
      "evidence_refs": [
        "tests/test_business_handler.py",
        "commit:abc1234"
      ]
    }
  }
}
```

Allowed `next_owner` values are `agent`, `user`, `external`, and `none`. Use `none` only after final closure.

Do not store secrets, tokens, full payloads, customer rows, or complete logs in progress metadata. Store only concise conclusions and evidence references.

## Checkpoint History

Keep an append-only `progress.md` beside `task.json`. The snapshot is overwritten; the history is appended.

Each entry should contain:

- timestamp and stable checkpoint id
- checkpoint kind: `checkpoint`, `gate_close`, or `recovery`
- current Gate
- accepted Gate, when a Gate was closed
- current work and latest verified result
- next action and owner
- blocker information
- evidence references

Use `recovery` when correcting stale state after the fact. Do not fabricate missing historical checkpoints; state clearly that the entry is a recovery calibration.

## Update Triggers

Update the local snapshot at these points:

1. A Trellis task is created and the initial Gate route is known.
2. A meaningful implementation or verification checkpoint completes.
3. Work becomes blocked or the next owner changes.
4. The Agent is about to end a session with unfinished work.
5. The user accepts or rejects a Gate.
6. Stage H calibration completes before archive.

Do not write a checkpoint for every tool call or small file edit.

## Gate Close Transaction

For a Gate that requires user judgment:

1. Report the result, evidence, risk, and proposed next Gate.
2. Ask: `当前 Gate 是否验收通过，并记录到 Trellis？`
3. If Base is configured, also ask whether to sync the management projection.
4. After acceptance, append one `gate_close` checkpoint.
5. Advance `current_gate`, update the next action and owner, and read back the saved snapshot.
6. If rejected, keep the current Gate and record the smallest corrective next action.

Do not claim the Gate is locally closed until the snapshot and checkpoint history have been written and read back successfully.

## Session Recovery

On a new session, read in this order:

1. `rpa_collab.py status` / `suggest`, when the guard CLI is available.
2. `task.py current --source`, when an active pointer exists.
3. Current or explicitly named task `task.json`.
4. `task.json.meta.progress`.
5. The latest entry in task `progress.md`.
6. PRD, design, and implementation artifacts.
7. Recent Git commits and relevant runner evidence.

The Trellis workspace journal remains useful for developer-wide session history, but it does not replace task-local progress because a journal entry may cover several tasks or may not have been written yet.

If task lifecycle and progress disagree, such as a completed or archived task whose progress still assigns work to a user or Agent, do not continue as if the latest chat message were authoritative. Report the drift, explain the evidence, and write one recovery checkpoint after user awareness.

## Optional Base Projection

Base may project the current Gate, next action, blocker, and accepted milestone summary. A missing or unavailable Base must not prevent local progress recording, production execution, or task recovery.

When Base is configured, derive its summary from the saved local checkpoint. Do not maintain a second independent interpretation of project progress.
