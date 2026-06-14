# 历史审计文档

更新时间：2026-06-14

本目录存放 **2026-05 至 2026-06** 内容反查、课件融入与站点调研的闭环记录，供维护者考古与数值追溯。**日常贡献不必阅读**；新任务见 [../good-first-issues.md](../good-first-issues.md)。

原始课件在本地 `sources/`（`.gitignore`），不发布。面向读者的 `content/` 不得引用 `sources/` 文件名或 BLQ 页码。

## 文档一览

| 文件 | 用途 | 状态 |
|------|------|------|
| [KNOWLEDGE_AUDIT.md](KNOWLEDGE_AUDIT.md) | 53 个知识讲义逐节反查清单 | 2026-06-03 全量闭环 |
| [QUESTION_AUDIT.md](QUESTION_AUDIT.md) | 70 道题逐题校验状态 | 全部「已校验」 |
| [AUDIT_NOTES.md](AUDIT_NOTES.md) | 手算数值核对与十轮优化留痕 | 与上两项互引 |
| [SOURCE_EXTRACTION_AUDIT.md](SOURCE_EXTRACTION_AUDIT.md) | `sources/` 课件 → 站点页面映射总览 | 维护者内部 |
| [COURSE_INTEGRATION_REVIEW.md](COURSE_INTEGRATION_REVIEW.md) | 课件 PDF 逐页段融入决策 | 页级复核真源 |
| [source_extraction_index.json](source_extraction_index.json) | 课件逐页 JSON 索引（标题/关键词/摘要） | 脚本输出 |
| [BLQ_REVIEW_INTEGRATION.md](BLQ_REVIEW_INTEGRATION.md) | BLQ 考前串讲 75 页融入复核 | 已合入正文 |
| [blq_review_extraction_index.json](blq_review_extraction_index.json) | BLQ 逐页 JSON 索引 | 脚本输出 |
| [blq_review_vision_transcripts.json](blq_review_vision_transcripts.json) | BLQ 稀疏页视觉转写缓存 | 可选输入 |
| [SITE_RESEARCH_AND_OPTIMIZATION.md](SITE_RESEARCH_AND_OPTIMIZATION.md) | 类似站点调研与十轮 UX 优化记录 | R1–R10 已落地 |

## 相关脚本

```bash
# 重跑课件抽取（需本地 sources/）
python scripts/tools/extract_course_sources.py

# 重跑 BLQ 串讲抽取（需本地 sources/）
python scripts/tools/extract_blq_review.py
```

输出写入本目录。重跑后请核对 `content/` 是否仍无需引用站外出处。

## 被 `content/` 引用的维护者链接

站点正文中的维护者备注使用 GitHub blob URL（不进 Pages 内链）：

- [SOURCE_EXTRACTION_AUDIT.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/docs/audit/SOURCE_EXTRACTION_AUDIT.md)
- [COURSE_INTEGRATION_REVIEW.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/docs/audit/COURSE_INTEGRATION_REVIEW.md)
- [AUDIT_NOTES.md](https://github.com/estelledc/hust-eic-microwave-from-scratch/blob/main/docs/audit/AUDIT_NOTES.md)
