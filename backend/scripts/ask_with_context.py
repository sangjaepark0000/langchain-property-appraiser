from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.rag.answer import compose_answer


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ask the configured answer model using a local file inserted directly as prompt context, without DB/RAG ingestion."
    )
    parser.add_argument("context_file", help="Local text/markdown file to insert into the prompt as evidence")
    parser.add_argument("question", help="Question to ask about the prompt-inserted context")
    parser.add_argument("--data-mode", default="prompt_context", help="Evidence data_mode label; default: prompt_context")
    args = parser.parse_args()

    context_path = Path(args.context_file)
    text = context_path.read_text(encoding="utf-8")
    evidence = [
        {
            "chunk_id": None,
            "document_id": None,
            "chunk_index": 0,
            "text": text,
            "score": 1.0,
            "relevance": "prompt_context",
            "source_path": str(context_path),
            "source_name": context_path.name,
            "source_url": "unknown",
            "data_mode": args.data_mode,
            "is_official": args.data_mode == "official",
            "citation": {
                "source_path": str(context_path),
                "source_name": context_path.name,
                "source_url": "unknown",
                "data_mode": args.data_mode,
                "chunk_index": 0,
                "document_id": None,
                "chunk_id": None,
                "law_name": None,
                "article_number": None,
                "article_title": None,
                "effective_date": None,
                "revision_date": None,
                "source_authority": "user-provided prompt context",
                "document_kind": "prompt_inserted_context",
                "chunk_type": "full_context",
            },
            "metadata": {
                "source_name": context_path.name,
                "source_path": str(context_path),
                "data_mode": args.data_mode,
                "document_kind": "prompt_inserted_context",
            },
        }
    ]
    result = compose_answer(args.question, evidence)
    print(f"status={result.status}")
    print(f"provider={result.provider}")
    print(f"fallback={result.fallback}")
    print(f"data_mode={result.data_mode}")
    print("\nANSWER\n" + result.answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
