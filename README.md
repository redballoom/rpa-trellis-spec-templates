# RPA Python + ShadowBot Trellis Spec Templates

这是一个独立、可选的 Trellis Spec 模板仓库，用于约束 Agent 在 `rpa-dev-template` 项目中的开发行为。

它不提供运行代码，不替代 `rpa-dev-template`，也不替代 `rpa-dev-template-skills`。项目仍可在不安装 Trellis 的情况下运行。

## 职责边界

```text
rpa-dev-template        = Python 运行底座和影刀调用契约
rpa-dev-template-skills = 初始化、业务契约、故障修复、进度与交付收尾等专业动作
本仓库                  = Agent 写代码和检查代码时参考的工程规范
Trellis                 = 可选的任务、记忆和 Spec 编排工具
```

## 安装

仓库发布后，可通过自定义 registry 初始化：

```bash
trellis init --registry git@github.com:redballoom/rpa-trellis-spec-templates.git --template rpa-python-shadowbot --codex
```

Trellis 会读取 registry index，并将所选模板目录内容安装到项目的 `.trellis/spec/`。
当前仓库同时保留两个入口：

- `index.json`：兼容 Trellis CLI 的 registry 根入口
- `marketplace/index.json`：保留 marketplace 目录结构，便于后续扩展 workflow 等模板类型

说明：公开 HTTPS 地址也可以作为 registry，但 Trellis 0.6.6 的 giget 下载路径会启用离线缓存。开发和验证阶段优先使用 SSH registry，可直接走 git 后端并避免旧模板缓存。

## 使用原则

1. 先使用 `rpa-dev-template` 初始化可运行项目。
2. 按需安装本 Spec，不把 Trellis加入 Python 运行依赖。
3. Agent 开发前阅读相关 `index.md` 和任务涉及的具体规范。
4. 以当前项目代码、Schema、测试和文档为最终事实；若与本 Spec 不一致，先确认实际契约，再更新项目 Spec。
5. 项目私有字段、客户规则、账号和密钥只留在项目内，不回写公共模板。

## 当前模板

| ID | 用途 |
| --- | --- |
| `rpa-python-shadowbot` | 影刀调用 Python Code 项目的契约优先开发规范 |

第一版的提炼依据和版本边界见 [SOURCES.md](./SOURCES.md)。

## 维护边界

本仓库只沉淀跨项目稳定规则，不包含：

- `run.bat`、`runner.py` 或业务 handler 实现
- Codex、Claude、Cursor 等特定 Agent 主机配置
- Trellis 任务状态机或会话数据
- 飞书 Base 表结构和同步逻辑
- 项目私有 Gate 路线图和 Base 记录内容
- 生产密钥、账号、Cookie、客户数据

本仓库可以定义跨项目稳定的本地进度字段与检查点规则，但实际 `task.json`、`progress.md` 和 Base 记录始终保存在具体项目或目标系统中。
