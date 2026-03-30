from backend.agent.nodes import agent_node, tool_node
from backend.agent.state import AgentState


def test_nodes():
    print("\n🚀 STARTING NODE TEST...\n")

    state: AgentState = {
        "messages": [{"role": "user", "content": "What is RAG?"}],
        "question": "What is RAG?",
        "final_answer": "",
        "steps": [],
        "iteration_count": 0,
        "sources": []
    }

    # 🧠 Run Agent Node
    print("🧠 Running agent node...")
    result = agent_node(state)

    print("\n📤 Agent Output:")
    print(result)

    # 🔍 Check if tool is called
    last_message = result["messages"][0]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("\n🛠 Tool call detected!")

        tool_result = tool_node({
            **state,
            **result
        })

        print("\n📤 Tool Output:")
        print(tool_result)

    else:
        print("\n⚠ No tool call — direct answer from agent")


# 🔥 THIS IS CRITICAL
if __name__ == "__main__":
    test_nodes()