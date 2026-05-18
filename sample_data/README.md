# Sample Data

Sample markdown/txt files in this directory are local test data only. They are not official legal/regulatory data and are not user-provided business documents.

## RAG Smoke Fixtures

- `sample-property-alpha.md`: Fictional Parcel Alpha facts for retrieval tests.
- `sample-property-beta.md`: Fictional Parcel Beta facts for retrieval tests.
- `sample-appraisal-report.md`: synthetic appraisal-report summary for prompt-inserted context tests. It is not an actual appraisal report and should not be ingested into the RAG database by default.
- `rag-smoke-questions.json`: smoke questions, expected answer hints, and expected citation/source paths.

All files are SAMPLE DATA ONLY. Property fixture files may be ingested with `data_mode=sample` for local smoke tests; `sample-appraisal-report.md` is intended for direct prompt-context experiments instead of default RAG ingestion. They are not official data and must not be presented as official evidence.
