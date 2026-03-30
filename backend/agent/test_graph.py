from backend.agent.graph import run_agent


def test_graph():
    print("\n🚀 TESTING FULL AGENT LOOP...\n")

    question = "Explain RAG in simple terms"

    result = run_agent(question)

    print("\n✅ FINAL ANSWER:\n")
    print(result["answer"])

    print("\n🧠 REASONING STEPS:\n")
    for step in result["steps"]:
        print("-", step)


if __name__ == "__main__":
    test_graph()