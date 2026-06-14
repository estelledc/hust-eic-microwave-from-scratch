# Agent 入口

本文件遵循 [agents.md](https://agents.md/) 开放格式。详细说明见 **[docs/AGENTS.md](docs/AGENTS.md)**。

## 快速命令

```bash
python -m pip install -r requirements.txt
python build.py
python scripts/tools/check_cross_refs.py
```

## 必读

- [docs/AGENTS.md](docs/AGENTS.md) — 目录、playbook、禁止事项
- [docs/PR_CHECKLIST.md](docs/PR_CHECKLIST.md) — 提交 PR 前逐步检查
- [docs/good-first-issues.md](docs/good-first-issues.md) — 入门任务 + Agent prompt
- [CONTRIBUTING.md](CONTRIBUTING.md) — 人类贡献者流程

默认分支：`main`。不要 force push `main`，不要提交 `site/`。
