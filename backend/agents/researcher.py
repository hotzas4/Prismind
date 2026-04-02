from __future__ import annotations

import uuid
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from core.config import settings


class ResearcherState(TypedDict):
    agent_id: str
    topic: str
    literature_summary: str
    methodology: str
    data_analysis: str
    draft_paper: dict
    submitted: bool
    error: str


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY, temperature=0.7)


async def select_topic(state: ResearcherState) -> ResearcherState:
    """Agent autonomously selects a research topic based on its interests."""
    llm = _get_llm()
    response = await llm.ainvoke(
        "You are an autonomous scientific researcher. Select an interesting, novel research topic "
        "that you want to investigate. Respond with ONLY the topic title."
    )
    return {**state, "topic": response.content.strip()}


async def literature_review(state: ResearcherState) -> ResearcherState:
    """Conduct a literature review on the chosen topic."""
    llm = _get_llm()
    response = await llm.ainvoke(
        f"Conduct a brief literature review on the topic: '{state['topic']}'. "
        "Summarize key existing findings and identify gaps in the research."
    )
    return {**state, "literature_summary": response.content.strip()}


async def design_methodology(state: ResearcherState) -> ResearcherState:
    """Design a research methodology."""
    llm = _get_llm()
    response = await llm.ainvoke(
        f"Based on this literature review:\n{state['literature_summary']}\n\n"
        f"Design a research methodology for studying: '{state['topic']}'"
    )
    return {**state, "methodology": response.content.strip()}


async def analyze_data(state: ResearcherState) -> ResearcherState:
    """Simulate data analysis and generate results."""
    llm = _get_llm()
    response = await llm.ainvoke(
        f"Given the methodology:\n{state['methodology']}\n\n"
        "Simulate and describe the expected results and analysis for this research."
    )
    return {**state, "data_analysis": response.content.strip()}


async def write_paper(state: ResearcherState) -> ResearcherState:
    """Write the full scientific paper."""
    llm = _get_llm()

    sections = {}
    prompts = {
        "abstract": f"Write a concise abstract for a paper titled: '{state['topic']}'\nLiterature: {state['literature_summary'][:500]}",
        "introduction": f"Write an introduction for: '{state['topic']}'",
        "methodology": f"Write the methodology section:\n{state['methodology']}",
        "results": f"Write the results section:\n{state['data_analysis']}",
        "discussion": f"Write a discussion section interpreting these results for: '{state['topic']}'",
        "conclusion": f"Write a conclusion for the paper: '{state['topic']}'",
    }

    for section, prompt in prompts.items():
        response = await llm.ainvoke(prompt)
        sections[section] = response.content.strip()

    draft = {
        "title": state["topic"],
        "agent_id": state["agent_id"],
        "field": "Interdisciplinary",
        "keywords": [],
        "language": "en",
        **sections,
    }
    return {**state, "draft_paper": draft}


async def submit_paper(state: ResearcherState) -> ResearcherState:
    """Submit the paper to the Prismind platform via the API."""
    import httpx

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/v1/papers",
                json=state["draft_paper"],
                timeout=30.0,
            )
            response.raise_for_status()
        return {**state, "submitted": True}
    except Exception as exc:
        return {**state, "submitted": False, "error": str(exc)}


def build_researcher_graph() -> StateGraph:
    graph = StateGraph(ResearcherState)

    graph.add_node("select_topic", select_topic)
    graph.add_node("literature_review", literature_review)
    graph.add_node("design_methodology", design_methodology)
    graph.add_node("analyze_data", analyze_data)
    graph.add_node("write_paper", write_paper)
    graph.add_node("submit_paper", submit_paper)

    graph.set_entry_point("select_topic")
    graph.add_edge("select_topic", "literature_review")
    graph.add_edge("literature_review", "design_methodology")
    graph.add_edge("design_methodology", "analyze_data")
    graph.add_edge("analyze_data", "write_paper")
    graph.add_edge("write_paper", "submit_paper")
    graph.add_edge("submit_paper", END)

    return graph


researcher_app = build_researcher_graph().compile()


async def run_researcher_agent(agent_id: uuid.UUID) -> dict:
    """Entry point for running a researcher agent workflow."""
    initial_state: ResearcherState = {
        "agent_id": str(agent_id),
        "topic": "",
        "literature_summary": "",
        "methodology": "",
        "data_analysis": "",
        "draft_paper": {},
        "submitted": False,
        "error": "",
    }
    result = await researcher_app.ainvoke(initial_state)
    return result
