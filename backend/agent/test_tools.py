from backend.agent.tools import search_knowledge_base, summarise_topic


def test_tools():
    print("\n🔍 Testing search tool...")
    result1 = search_knowledge_base.invoke({"query": "What is RAG"})
    print(result1)

    print("\n📘 Testing summarise tool...")
    result2 = summarise_topic.invoke({"topic": "RAG"})
    print(result2)


if __name__ == "__main__":
    test_tools()