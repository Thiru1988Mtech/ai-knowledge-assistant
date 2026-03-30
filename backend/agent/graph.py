from langgraph.graph import StateGraph, END

from backend.agent.state import AgentState
from backend.agent.nodes import agent_node, tool_node, final_node, router


def build_agent():
    graph = StateGraph(AgentState)

    # 🧠 Nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_node("final", final_node)

    # 🚀 Entry point
    graph.set_entry_point("agent")

    # 🔀 Conditional routing
    graph.add_conditional_edges(
        "agent",
        router,
        {
            "tools": "tools",
            "end": "final"
        }
    )

    # 🔁 Loop: tools → agent
    graph.add_edge("tools", "agent")

    # 🏁 Finish
    graph.add_edge("final", END)

    return graph.compile()


# 🔥 Compile graph
agent_app = build_agent()


# 🚀 Run function
def run_agent(question: str):
    result = agent_app.invoke({
        "messages": [{"role": "user", "content": question}],
        "question": question,
        "retrieved_context": "",
        "sources": [],
        "final_answer": "",
        "steps": [],
        "iteration_count": 0
    })

    return {
        "answer": result["final_answer"],
        "steps": result["steps"]
    }