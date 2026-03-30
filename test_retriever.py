from backend.rag.retriever import Retriever

retriever = Retriever()

query = "What is this document about?"

results = retriever.retrieve(query)

for i, r in enumerate(results):
    print(f"\nResult {i+1}")
    print("Score:", r["score"])
    print("Source:", r["source"])
    print("Content:", r["content"][:200])