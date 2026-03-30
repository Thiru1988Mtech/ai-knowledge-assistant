from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    # Conversation messages (LLM + user)
    messages: Annotated[list, operator.add]

    # User input
    question: str

    # Final output
    final_answer: str

    # Reasoning steps (for debugging + UI)
    steps: Annotated[list[str], operator.add]

    # Loop control (VERY IMPORTANT)
    iteration_count: int

    # Sources (used later with RAG)
    sources: list[str]