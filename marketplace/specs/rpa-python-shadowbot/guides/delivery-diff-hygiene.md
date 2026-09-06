# Delivery Diff Hygiene

业务代码和治理记录回答不同问题：前者说明系统行为怎样变化，后者说明谁在何时接受了什么。把两者混成一次生成式大提交，会降低 PR review 的可见性。

## 路径分区

```text
业务实现：src/、core/、handlers/、schemas/、tests/、run.bat、runner.py、耐久业务文档
治理记录：.project-gates/、.trellis/tasks/、.trellis/workspace/、生成式 Agent 资产
运行产物：runner_*.json、input*.json、logs/、crash_snapshots/、data/temp/、私有 payload
```

- 业务实现、契约、测试和必要文档形成聚焦的业务提交。
- 运行产物永不提交。
- 保持 `session_auto_commit: false`。Gate、Task archive、journal 写入并读回一致后，如用户授权 Git 记录，将治理路径合成最多一个后置提交。
- 同一 PR 必须分区列出业务和治理路径；大量生成文件应折叠、单独 review，或按项目策略留在本地。
- 归档、journal 或 Gate 文件存在不能替代业务 diff 的 review/check。

commit、push、PR、merge、Issue close 和发布仍是相互独立的授权；提交边界不扩大权限。
