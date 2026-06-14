# PR 提交前检查清单

Agent 或人类贡献者在 `git push` / `gh pr create` 之前逐步勾选。借鉴 [executablebooks CONTRIBUTING](https://github.com/executablebooks/.github/blob/master/CONTRIBUTING.md) 的 review checklist，并针对本仓库 Markdown + Python build 定制。

## 1. 范围与分支

- [ ] 当前分支 **不是** `main`
- [ ] 分支名符合规范（`content/` · `docs/` · `fix/` · `feat/` · `chore/`）
- [ ] `git status` 中无无关文件（尤其 `scripts/plots/` 的行尾符噪音）
- [ ] 只 stage 本次任务相关路径（优先 `git add <具体文件>`）

## 2. 内容质量（若改 `content/`）

- [ ] 符合 [MANUAL_CONTENT_STANDARD.md](MANUAL_CONTENT_STANDARD.md)
- [ ] 符号与课程口径一致（$Z_c$、$\Gamma$、Smith 圆图、TE/TM）
- [ ] 新页面已在阶段 README 或 guide 索引中链接
- [ ] 题解数值有来源或手算说明（不凭空改答案）

## 3. 导航与资源

- [ ] 新增/重命名文件时检查 `nav.json`
- [ ] 图片在 `assets/images/` 或 `assets/illustrations/`，Markdown 相对路径可访问
- [ ] 未引用 `sources/` 下本地-only 路径

## 4. 构建与校验（必须执行并保留输出）

```bash
python build.py
python scripts/tools/check_cross_refs.py
```

- [ ] `build.py` 成功（当前基线约 **169 pages**）
- [ ] 交叉引用：knowledge / solutions / experiments 缺失均为 **0**
- [ ] 若改考前复习相关：`python scripts/tools/check_exam_integration.py`
- [ ] 若改 Python：`python -m py_compile build.py scripts/plots/*.py scripts/tools/*.py`

## 5. 预览（content 改动建议做）

```bash
python -m http.server -d site 8000
```

- [ ] 打开改动页，公式渲染正常
- [ ] 侧栏标题合理（`nav.json`）
- [ ] 内外链可点击

## 6. Git 与 PR 元数据

- [ ] Commit message：`<type>(<scope>): <描述>`
- [ ] PR title 与 commit 风格一致
- [ ] 填写 `.github/PULL_REQUEST_TEMPLATE.md` 全部必填项
- [ ] 关联 Issue：`Closes #N` 或 `Related to #N`
- [ ] 未包含 `site/` 构建产物

## 7. 禁止项（任一命中则不要提交）

- [ ] 未对 `main` 做 force push
- [ ] 未删除他人 content 正文
- [ ] 未批量提交未校验的 AI 题解

## 8. CI 预期

PR 触发 `.github/workflows/pr-check.yml`：

- build + cross_refs + exam_integration + internal_links

全部通过后再请求 review。
