# Official Sources

This folder stores user-downloaded official source files and normalized text extracted from them.

## Layout

- `raw/`: original downloaded official files. Keep these as provenance evidence.
- `normalized/`: text extracted from raw files and metadata notes used for ingestion.

## Loading strategy

1. Keep PDF originals in `raw/`.
2. Use `pdftotext -layout` output in `normalized/*/extracted.txt` for ingestion.
3. Chunk consolidated law/rule texts by article (`제N조`, `제N조의M`) and supplementary provisions (`부칙`).
4. Preserve revision markers such as `<개정 YYYY. M. D.>` or `삭제 <YYYY. M. D.>` in chunk metadata.
5. Do not treat amendment reason/history files as consolidated current law text.

## Corpus groups

- `appraisal_act_framework`: law, enforcement decree, enforcement rule.
- `appraisal_standards`: appraisal method/standard rule (`감정평가에 관한 규칙`).
