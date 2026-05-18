# 发布到 GitHub Pages

本目录的 `workflows/pages.yml` 提供完整的构建 + 部署流水线。绑定 GitHub remote 后按以下步骤启用。

## 一次性配置

1. **创建仓库**：在 GitHub 创建 `hust-eic-microwave-review`（或自选名）。
2. **绑 remote**：

   ```bash
   git remote add origin git@github.com:<USER>/hust-eic-microwave-review.git
   git push -u origin main
   ```

3. **打开 Pages**：仓库 Settings → Pages → Source 选择 **GitHub Actions**（不要选 "Deploy from a branch"）。
4. **触发首次部署**：再次 push 任意提交，Actions 会自动跑 `pages.yml`。

## 工作流做了什么

- `build` job：装 Python 3.11 + `markdown` 包 → 跑 `python build.py` → 跑链接校验脚本（与本地一致，0 缺失才放行）→ 上传 `site/` 为 Pages artifact。
- `deploy` job：把 artifact 部署到 Pages 环境，URL 写到 deployment summary。

## 本地预览

工作流和本地构建逻辑完全一致：

```bash
python build.py
python -m http.server -d site 8000
# 浏览器打开 http://localhost:8000
```

## 链接校验失败时

CI 会打印前 20 个缺失链接。本地用同样的脚本反查：

```bash
python3 scripts/tools/check_cross_refs.py
```

或者直接在本地跑工作流里的内联脚本（复制粘贴运行）。

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
