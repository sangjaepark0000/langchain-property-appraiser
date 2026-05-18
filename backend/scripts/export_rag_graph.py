from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.graph.conversation import build_conversation_graph


class _GraphOnlySession:
    """Placeholder session; graph rendering only inspects node topology."""


def main() -> int:
    parser = argparse.ArgumentParser(description="Export the LangGraph conversation/RAG flow as Mermaid markdown.")
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "docs" / "rag-flow.md"),
        help="Markdown file to write. Default: docs/rag-flow.md",
    )
    args = parser.parse_args()

    graph = build_conversation_graph(_GraphOnlySession()).get_graph()
    mermaid = graph.draw_mermaid()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "# RAG Conversation Flow\n\n"
        "LangGraph가 실행하는 현재 `/chat` 대화/RAG 흐름입니다.\n\n"
        "```mermaid\n"
        f"{mermaid}\n"
        "```\n\n"
        "## Node responsibilities\n\n"
        "- `start`: 사용자 메시지를 conversation/message 테이블에 저장합니다.\n"
        "- `load_history`: 기존 대화 이력을 불러옵니다.\n"
        "- `rag_answer`: 질문 의도 확인, 검색, grading, rewrite, 답변 생성을 수행합니다.\n"
        "- `persist_assistant`: assistant 답변과 citation/trace metadata를 저장합니다.\n\n"
        "## Important branches inside `rag_answer`\n\n"
        "- 인사/잡담(`hi`, `안녕하세요` 등)은 retrieval을 건너뛰고 안내 답변을 반환합니다.\n"
        "- 법령 조문 질문은 vector search 결과에 조문번호/법령명 lexical boost를 병합합니다.\n"
        "- 검색 점수가 부족하면 insufficient evidence 경로로 이동하고 출처를 조작하지 않습니다.\n"
        "- 충분한 근거가 있으면 LangChain OpenAI answer provider가 근거 기반 답변을 생성합니다.\n",
        encoding="utf-8",
    )
    print(f"wrote={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
