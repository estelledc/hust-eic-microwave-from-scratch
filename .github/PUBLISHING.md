# 发布到 GitHub Pages

本目录的 `workflows/pages.yml` 提供完整的构建 + 部署流水线。当前仓库 remote 为 `estelledc/hust-eic-microwave-from-scratch`。

## 一次性配置

1. **仓库**：已创建并绑定 remote（见上）。
2. **打开 Pages**：仓库 Settings → Pages → Source 选择 **GitHub Actions**（不要选 "Deploy from a branch"）。
3. **触发部署**：push 到 `main` 或手动 `workflow_dispatch`，Actions 会跑 `pages.yml`。

若在新 fork 上复现：

```bash
git remote add origin git@github.com:<USER>/hust-eic-microwave-from-scratch.git
git push -u origin main
```

## 工作流做了什么

- `build` job：Python 3.11 + `requirements.txt` → `python build.py` → 内链校验（0 缺失才放行）→ 上传 `site/` 为 Pages artifact。
- `deploy` job：部署到 Pages 环境。

**注意**：仓库内 `site/` 被 `.gitignore` 忽略（仅保留 `site/.gitkeep`）。本地必须先 `python build.py` 再预览；线上完全由 CI 构建。

## 本地预览

工作流和本地构建逻辑完全一致：

```bash
python3 -m pip install -r requirements.txt   # 首次
python build.py
python -m http.server -d site 8000
# 浏览器打开 http://localhost:8000
```

## 链接校验失败时

CI 会打印前 20 个缺失链接。本地：

```bash
python3 scripts/tools/check_cross_refs.py
python build.py
# 再跑 pages.yml 中的内联链接脚本，或 push 触发 CI
```

## 缓存优化（可选）

加 `actions/cache@v4` 缓存 pip：

```yaml
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}
```

放在 "Set up Python" 之后、"Install dependencies" 之前即可。

## 自定义域名（可选）

在仓库 Settings → Pages → Custom domain 填域名，仓库根加 `CNAME` 文件。Workflow 不需要改。
