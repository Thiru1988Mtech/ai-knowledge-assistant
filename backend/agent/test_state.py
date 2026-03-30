from backend.agent.state import AgentState


def test_state_structure():
    state: AgentState = {
        "messages": [],
        "question": "What is RAG?",
        "final_answer": "",
        "steps": [],
        "iteration_count": 0,
        "sources": []
    }

    print("\n✅ Initial State:")
    print(state)


if __name__ == "__main__":
    test_state_structure()