# Ingestion Plan for Downloaded Appraisal Official Sources

## File classification

| Folder | Role | Chunking |
|---|---|---|
| `appraisal_act` | 감정평가법 본문 | article chunks + supplementary provisions |
| `appraisal_act_enforcement_decree` | 감정평가법 시행령 본문 | article chunks + supplementary provisions |
| `appraisal_act_enforcement_rule` | 감정평가법 시행규칙 본문 | article chunks + deleted article marker |
| `appraisal_standards_rule` | 감정평가에 관한 규칙, 별도 기준/방법론 corpus | article chunks |

## Not a direct diff

The dates `2023-08-10`, `2024-09-26`, and `2026-03-12` refer to different legal levels: act, decree, and enforcement rule. They are not versions of the same document. Diff-like signals should be extracted from each document's internal markers, for example:

- `<개정 YYYY. M. D.>`
- `삭제 <YYYY. M. D.>`
- `부칙 <제...호, YYYY. M. D.>`

## Recommended chunk metadata

```json
{
  "corpus_group": "appraisal_act_framework",
  "document_kind": "current_consolidated_rule",
  "law_level": "enforcement_rule",
  "law_name": "감정평가 및 감정평가사에 관한 법률 시행규칙",
  "article_number": "제27조",
  "article_title": null,
  "chunk_type": "article",
  "change_type": "deleted",
  "revision_date": "2026-03-12",
  "effective_date": "2026-03-12",
  "source_authority": "국가법령정보센터",
  "data_mode": "official"
}
```

## Manual review notes

- PDF original files are preserved under `raw/` for provenance.
- `extracted.txt` files are generated via `pdftotext -layout` and should be inspected before production ingestion.
- The enforcement rule has a known marker: `제27조 삭제 <2026. 3. 12.>`.
- Do not infer missing revision/effective dates beyond visible source notes or official text markers.
