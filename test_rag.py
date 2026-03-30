from backend.rag.pipeline import RAGPipeline

rag = RAGPipeline()

question = "What skills are required for AI Architect?"

result = rag.answer(question)

print("\nAnswer:\n", result["answer"])
print("\nSources:", result["sources"])
print("Chunks used:", result["chunks_used"])
print("Top score:", result["top_score"])