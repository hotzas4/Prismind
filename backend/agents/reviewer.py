from __future__ import annotations

import uuid
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from core.config import settings


class ReviewerState(TypedDict):
    paper_id: str
    reviewer_agent_id: str
    paper_content: dict
    methodology_evaluation: str
    citation_check: str
    review_text: str
    recommendation: str
    submitted: bool
    error: str


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY, temperature=0.3)


async def read_paper(state: ReviewerState) -> ReviewerState:
    """Fetch the paper from the Prismind API."""
    import httpx

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:8000/api/v1/papers/{state['paper_id']}",
                timeout=10.0,
            )
            response.raise_for_status()
            paper_data = response.json()
        return {**state, "paper_content": paper_data}
    except Exception as exc:
        return {**state, "error": str(exc)}


async def evaluate_methodology(state: ReviewerState) -> ReviewerState:
    """Evaluate the research methodology."""
    llm = _get_llm()
    paper = state["paper_content"]
    response = await llm.ainvoke(
        f"As a peer reviewer, evaluate the methodology of this paper:\n"
        f"Title: {paper.get('title', '')}\n"
        f"Methodology: {paper.get('methodology', '')}\n\n"
        "Provide a structured evaluation of scientific rigor, validity, and potential flaws."
    )
    return {**state, "methodology_evaluation": response.content.strip()}


async def check_citations(state: ReviewerState) -> ReviewerState:
    """Check citations and references."""
    llm = _get_llm()
    paper = state["paper_content"]
    response = await llm.ainvoke(
        f"Review the references section for completeness and appropriateness:\n"
        f"Title: {paper.get('title', '')}\n"
        f"References: {paper.get('references', [])}\n\n"
        "Identify any missing key references or citation issues."
    )
    return {**state, "citation_check": response.content.strip()}


async def write_review(state: ReviewerState) -> ReviewerState:
    """Write a comprehensive peer review."""
    llm = _get_llm()
    paper = state["paper_content"]
    response = await llm.ainvoke(
        f"Write a comprehensive peer review for:\n"
        f"Title: {paper.get('title', '')}\n"
        f"Abstract: {paper.get('abstract', '')}\n\n"
        f"Methodology Evaluation:\n{state['methodology_evaluation']}\n\n"
        f"Citation Check:\n{state['citation_check']}\n\n"
        "Provide: 1) Summary, 2) Major concerns, 3) Minor concerns, 4) Recommendation (Accept/Revise/Reject)"
    )
    review_text = response.content.strip()

    # Extract recommendation
    recommendation = "revise"
    if "accept" in review_text.lower() and "reject" not in review_text.lower():
        recommendation = "accept"
    elif "reject" in review_text.lower():
        recommendation = "reject"

    return {**state, "review_text": review_text, "recommendation": recommendation}


async def submit_review(state: ReviewerState) -> ReviewerState:
    """Submit the peer review to the Prismind platform."""
    import httpx

    if state.get("error"):
        return {**state, "submitted": False}

    try:
        # Update paper with peer review notes
        update_payload = {
            "peer_review_notes": state["review_text"],
            "peer_reviewed": True,
        }
        if state["recommendation"] == "accept":
            update_payload["status"] = "published"

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"http://localhost:8000/api/v1/papers/{state['paper_id']}",
                json=update_payload,
                timeout=10.0,
            )
            response.raise_for_status()
        return {**state, "submitted": True}
    except Exception as exc:
        return {**state, "submitted": False, "error": str(exc)}


def build_reviewer_graph() -> StateGraph:
    graph = StateGraph(ReviewerState)

    graph.add_node("read_paper", read_paper)
    graph.add_node("evaluate_methodology", evaluate_methodology)
    graph.add_node("check_citations", check_citations)
    graph.add_node("write_review", write_review)
    graph.add_node("submit_review", submit_review)

    graph.set_entry_point("read_paper")
    graph.add_edge("read_paper", "evaluate_methodology")
    graph.add_edge("evaluate_methodology", "check_citations")
    graph.add_edge("check_citations", "write_review")
    graph.add_edge("write_review", "submit_review")
    graph.add_edge("submit_review", END)

    return graph


reviewer_app = build_reviewer_graph().compile()


async def run_reviewer_agent(paper_id: uuid.UUID, reviewer_agent_id: uuid.UUID) -> dict:
    """Entry point for running a reviewer agent workflow."""
    initial_state: ReviewerState = {
        "paper_id": str(paper_id),
        "reviewer_agent_id": str(reviewer_agent_id),
        "paper_content": {},
        "methodology_evaluation": "",
        "citation_check": "",
        "review_text": "",
        "recommendation": "",
        "submitted": False,
        "error": "",
    }
    result = await reviewer_app.ainvoke(initial_state)
    return result
