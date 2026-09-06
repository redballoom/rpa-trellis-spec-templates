# Collaboration Entry

本指南定义正式工程 Task 的唯一入口顺序。它组合 Trellis 与 Project Gate Controller，但不修改 Trellis CLI，也不创建第二套 Task 或 Gate 状态。

## 三次主要确认

正常交付只向用户发起三个主要确认包；每个包必须展示结论、证据、风险和将执行的写入：

| 次数 | 用户确认包 | 内部事件 |
| --- | --- | --- |
| 1 | 目标、成功结果、范围与明确不做事项 | 分别保存 G0 与 G1 close 事件；正式 Task 可在目标与验收方向明确后创建为 `planning` |
| 2 | 输入输出契约、验收基线、交付要求、实施计划与实施授权 | 保存 G2 close 或 amendment/revalidation；active-task preflight 通过后 `task.py start` |
| 3 | 技术、目标环境、业务结果、剩余风险与发布/归档授权 | 按适用路线分别保存 G3/G4/G5 close 或 revalidation；archive preflight 通过后归档 Task |

一个确认包可以授权多个已清楚列出的内部事件，但不得合并、覆盖或伪造 G0-G5 历史。若证据尚未齐全，只记录已经满足的事件，未满足部分继续等待。

以下情况可增加必要确认：范围或契约变化、失败后的策略选择、高风险或不可逆操作、凭据/生产数据处理、发布/合并/rebase/删除，以及用户判断不可替代的业务例外。普通工具调用、测试重跑、记录既有事实和确认范围内的可逆实现不增加主要确认。

## 正式 Task start

不要直接把 `task.py start` 当作入口。按以下顺序执行并读回结果：

1. 运行 Project Gate Controller `status`，读取项目 Gate、选中 Task、警告和 accepted baseline。
2. 运行 `python .trellis/scripts/task.py current` 与 `list`。若另一业务 Task 已是 `in_progress`，停止并处理暂停/切换授权；`00-bootstrap-guidelines` 不算业务 Task。
3. 确认 Task 仍为 `planning`，目标、AC、交付要求、可选 delivery route、工作分支和第二次主要确认均已记录。
4. 执行 `python .trellis/scripts/task.py start <task-dir>`，随后再次运行 `current` 和 Controller `status`。

`status` 是只读 active-task preflight，不可由聊天记忆、Base 或 Task 内复制的 `current_gate` 替代。

## PR 与 G3 时序

当 `meta.delivery_requirements.require_pr=true`：

1. 在请求 G3 技术接受之前创建 PR，并把可访问的 `pr_url` 写入 Task evidence。
2. 从 Git 平台读取 PR 当前状态，不以“准备创建”“已有分支”或本地 diff 代替 PR。
3. 至少记录一项实际 review 结论和一项已通过的 check/CI 结论；各自保留可返回来源的 URL、check 名称或审查记录引用。
4. 将上述事实写入 `meta.archive_evidence.technical_checks`，并在 G3 close/revalidation 的 evidence 中引用它们。
5. review 未通过、checks 缺失/运行中/失败，或只有 `pr_url` 时，G3 不得标记完成。

最小示例：

```json
{
  "meta": {
    "delivery_requirements": {
      "require_pr": true,
      "require_runner": true,
      "require_user_acceptance": true
    },
    "archive_evidence": {
      "technical_checks": [
        {"name": "pull request review", "result": "passed", "evidence_refs": ["https://git.example/pulls/12#review-44"]},
        {"name": "unit-tests", "result": "passed", "evidence_refs": ["https://git.example/pulls/12/checks#unit-tests"]}
      ],
      "commit": "<exact-commit>",
      "pr_url": "https://git.example/pulls/12",
      "runner_refs": ["evidence/runs/<run-id>.summary.json"],
      "final_summary": "技术、目标环境和剩余风险摘要"
    }
  }
}
```

## 正式 Task archive

归档前按以下顺序执行：

1. 运行 Controller `status`；若有 `unaccepted_delivery_drift`、`history_diverged`、多 active Task 或非法 route，停止归档。
2. 若要求 runner，先运行 `evidence-check --summary evidence/runs/{run_id}.summary.json`，并要求 `valid=true`、`delivery_ready=true`。
   `valid` 只表示历史摘要有效；`delivery_ready` 还要求当前交付代码兼容。Schema 2 保留运行时精确 commit 和原始工作树状态，新增交付代码清洁度。只保存摘要或 Gate/Task/journal 记录的后续提交不要求重跑；代码、Spec、配置、依赖、契约、Skill 指令或未知文件变更必须重验。读取 Controller `version_check`，不要把摘要 commit 改写为当前 HEAD。
3. 运行 `delivery-route-check`（Task 配置 route 时）与 `archive-check`；要求 `ready=true`。`require_pr=true` 时另行核对 PR review/check 的真实平台状态，因为 URL 本身不是验收。
4. 完成第三次主要确认及其适用的 Gate close/revalidation，并读回 Project Gate Controller。
5. 用户已授权归档后，运行 `python .trellis/scripts/task.py archive <task-name> --no-commit`；再次读取 Task 列表与 Controller `status`。
6. Git commit、push、PR merge、Issue close 和发布都是独立动作，只按用户授权执行。

原生 Trellis start/archive 仍可被直接调用，因此 Agent 必须把以上 preflight 当作正式入口；不能宣称 Trellis CLI 自身已经强制这些规则。

## 引用而不复制

- Project Gate accepted baseline：引用 `.project-gates/project.json` 或 `commit:<sha>`。
- amendment/revalidation：引用 `.project-gates/gate-history.md#<event-id>`。
- portable run evidence：引用 `evidence/runs/{run_id}.summary.json`。
- PR review/check：引用 Git 平台的具体 review/check URL 或稳定标识。

Task 保存指针和工程结论，不复制 Gate 快照、完整 evidence summary、runner 原文、日志、payload、客户数据或凭据。
