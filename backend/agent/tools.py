from langchain_core.tools import tool
from backend.rag.retriever import Retriever

# Initialize retriever (from Phase 2)
retriever = Retriever()


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search internal knowledge base for relevant information.
    Use this for document-related questions.
    """
    results = retriever.retrieve(query, top_k=4)

    if not results:
        return "No relevant documents found."

    return "\n\n---\n\n".join(
        f"[{r['source']} | score:{r['score']}]\n{r['content']}"
        for r in results
    )


@tool
def summarise_topic(topic: str) -> str:
    """
    Retrieve and summarise information about a topic.
    Use for general overview questions.
    """
    results = retriever.retrieve(topic, top_k=6)

    if not results:
        return "No information found."

    combined = " ".join(r["content"] for r in results)

    return combined[:2000]


# Register tools
TOOLS = [search_knowledge_base, summarise_topic]

# Mapping for execution
TOOL_MAP = {tool.name: tool for tool in TOOLS}