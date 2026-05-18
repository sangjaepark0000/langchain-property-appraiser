from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph


class StudioRAGState(TypedDict, total=False):
    question: str
    intent: str
    retrieval_status: str
    grading_status: str
    answer_status: str
    citations_count: int
    note: str


def classify_intent(state: StudioRAGState) -> StudioRAGState:
    question = state.get("question", "")
    normalized = question.strip().lower()
    if normalized in {"hi", "hello", "hey", "안녕", "안녕하세요", "ㅎㅇ", "하이"}:
        state["intent"] = "smalltalk"
        state["retrieval_status"] = "skipped"
    else:
        state["intent"] = "appraisal_review_or_law_question"
        state["retrieval_status"] = "required"
    return state


def retrieve_context(state: StudioRAGState) -> StudioRAGState:
    if state.get("retrieval_status") == "skipped":
        return state
    state["retrieval_status"] = "vector_search_plus_article_boost"
    return state


def grade_evidence(state: StudioRAGState) -> StudioRAGState:
    if state.get("retrieval_status") == "skipped":
        state["grading_status"] = "not_applicable"
    else:
        state["grading_status"] = "sufficient_or_insufficient"
    return state


def generate_answer(state: StudioRAGState) -> StudioRAGState:
    if state.get("intent") == "smalltalk":
        state["answer_status"] = "local_guidance_no_citations"
        state["citations_count"] = 0
    else:
        state["answer_status"] = "langchain_openai_grounded_answer_or_insufficient_evidence"
        state["citations_count"] = state.get("citations_count", 0)
    return state


def persist_trace(state: StudioRAGState) -> StudioRAGState:
    state["note"] = "Design graph for LangGraph Studio visualization; FastAPI runtime uses app.graph.conversation."
    return state


builder = StateGraph(StudioRAGState)
builder.add_node("classify_intent", classify_intent)
builder.add_node("retrieve_context", retrieve_context)
builder.add_node("grade_evidence", grade_evidence)
builder.add_node("generate_answer", generate_answer)
builder.add_node("persist_trace", persist_trace)
builder.set_entry_point("classify_intent")
builder.add_edge("classify_intent", "retrieve_context")
builder.add_edge("retrieve_context", "grade_evidence")
builder.add_edge("grade_evidence", "generate_answer")
builder.add_edge("generate_answer", "persist_trace")
builder.add_edge("persist_trace", END)

graph = builder.compile()
