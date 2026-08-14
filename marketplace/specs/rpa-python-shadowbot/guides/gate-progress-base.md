# Gate Progress And Optional Base Projection

Use this guide only when a project explicitly configures a Feishu Base management view.

Base is not required for project recovery, Task execution, runner operation, Gate acceptance, or release. It has no authority to create or update Trellis Task state or Hermes Gate state.

Read `local-progress-tracking.md` first. It defines the authoritative sources and recovery order.

## Ownership

```text
Hermes                    = project current Gate and accepted Gate events
Trellis                   = engineering Task, plan, notes, references, and archive
Git / PR                  = code version and technical acceptance
runner / logs             = target-environment execution evidence
Gitea Issue               = original requirement and discussion
Base                      = optional read-only management projection
user                      = business acceptance and irreversible authorization
```

Base can combine summaries from these sources. It must not become a second writer, fallback authority, or required runtime dependency.

## Projection Inputs

Before preparing a Base update, read the authoritative sources directly:

1. Hermes current Gate and latest Gate event.
2. Trellis Task ID, title, native status, delivery state, blocker, and next engineering action.
3. Linked Issue, PR, commit, test, and runner references.
4. The accepted conclusion that is safe to expose in a management view.

Do not derive a projection from chat memory, an older Base record, legacy `.rpa_ai/handoff`, `task.json.meta.progress.current_gate`, or Task-local Gate checkpoints.

## Recommended Projection

A management record may show:

| Field | Source |
| --- | --- |
| `当前Gate` | Hermes `.hermes/project.json` |
| `最近Gate事件` | latest accepted Hermes Gate history event |
| `当前工程Task` | Trellis Task |
| `Task状态` | Trellis native status plus schema-governed delivery state |
| `下一步建议` | Task-owned next action or Hermes next acceptance action, clearly labelled |
| `是否阻塞` / `阻塞说明` | Trellis Task blocker |
| `证据引用` | Git, PR, tests, runner, and approved document references |

The projection must retain source identifiers so a reader can return to the authority. Do not copy full PRD, Task tree, payload, logs, customer rows, secrets, tokens, or chat transcripts.

## Update Discipline

When the user requests a Base update:

1. Read Hermes, Trellis, Git/PR, and runner facts.
2. Detect and report conflicts before projecting.
3. Prepare a concise, desensitized summary with source references.
4. Ask for the target Base record only when it is not already configured.
5. Write the Base view after the authoritative state is saved and read back.
6. If Base write fails, report the projection failure without changing or rolling back Hermes, Trellis, Git, or runner facts.

Base updates never close a Gate, archive a Task, close an Issue, merge a PR, or publish a release.

## Idempotency

Use a stable projection key such as:

```text
<project_id>/<source_kind>/<source_id>/<event_type>/v<version>
```

Repeated delivery of the same source event must update or no-op the same projection record rather than create duplicate milestones.

## Anti-Patterns

- Do not use Base as the only copy of project Gate or Task status.
- Do not write Base state back into Hermes or Trellis.
- Do not let Base availability block `run.bat`, `runner.py`, handler execution, Task recovery, or Gate acceptance.
- Do not create one Base record for every tool call or small code edit.
- Do not project unaccepted Gate conclusions as completed.
- Do not ask for a Base link when the project has not requested a management projection.
- Do not keep legacy Task Gate fields synchronized for compatibility.
