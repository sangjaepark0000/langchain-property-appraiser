from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TypedDict

from langgraph.graph import END, StateGraph
from sqlalchemy.orm import Session

from app.models.message import Message
from app.rag.answer import AnswerResult
from app.rag.query import answer_question
from app.services.conversation_service import append_message, get_message_history

logger = logging.getLogger(__name__)


class ConversationGraphState(TypedDict, total=False):
    question: str
    conversation_id: int | None
    query_vector: list[float] | None
    history: list[Message]
    answer: AnswerResult


@dataclass(frozen=True)
class ConversationGraphResult:
    conversation_id: int
    answer: AnswerResult
    history: list[Message] = field(default_factory=list)


def _log_transition(node: str, state: ConversationGraphState) -> None:
    logger.info(
        "node=%s conversation_id=%s history_count=%s",
        node,
        state.get("conversation_id"),
        len(state.get("history", [])),
    )


def build_conversation_graph(session: Session):
    def start(state: ConversationGraphState) -> ConversationGraphState:
        _log_transition("start", state)
        created = append_message(
            session,
            conversation_id=state.get("conversation_id"),
            role="user",
            content=state["question"],
        )
        state["conversation_id"] = created.conversation_id
        return state

    def load_history(state: ConversationGraphState) -> ConversationGraphState:
        _log_transition("load_history", state)
        state["history"] = get_message_history(session, state["conversation_id"])
        return state

    def rag_answer(state: ConversationGraphState) -> ConversationGraphState:
        _log_transition("rag_answer", state)
        rag_result = answer_question(
            session,
            state["question"],
            query_vector=state.get("query_vector"),
        )
        state["answer"] = rag_result.answer
        return state

    def persist_assistant(state: ConversationGraphState) -> ConversationGraphState:
        _log_transition("persist_assistant", state)
        append_message(
            session,
            conversation_id=state["conversation_id"],
            role="assistant",
            content=state["answer"].answer,
            metadata={
                "status": state["answer"].status,
                "data_mode": state["answer"].data_mode,
                "fallback": state["answer"].fallback,
                "provider": state["answer"].provider,
                "citations": state["answer"].citations,
            },
        )
        return state

    graph = StateGraph(ConversationGraphState)
    graph.add_node("start", start)
    graph.add_node("load_history", load_history)
    graph.add_node("rag_answer", rag_answer)
    graph.add_node("persist_assistant", persist_assistant)
    graph.set_entry_point("start")
    graph.add_edge("start", "load_history")
    graph.add_edge("load_history", "rag_answer")
    graph.add_edge("rag_answer", "persist_assistant")
    graph.add_edge("persist_assistant", END)
    return graph.compile()


def run_conversation_graph(
    session: Session,
    *,
    question: str,
    conversation_id: int | None = None,
    query_vector: list[float] | None = None,
) -> ConversationGraphResult:
    graph = build_conversation_graph(session)
    final_state = graph.invoke(
        {
            "question": question,
            "conversation_id": conversation_id,
            "query_vector": query_vector,
        }
    )
    return ConversationGraphResult(
        conversation_id=final_state["conversation_id"],
        answer=final_state["answer"],
        history=final_state.get("history", []),
    )
