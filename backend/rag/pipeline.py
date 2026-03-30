from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from backend.rag.retriever import Retriever
from backend.config import settings

SYSTEM_PROMPT = """You are an expert AI knowledge assistant.

Answer using ONLY the context below.
If the answer is not in context, say:
'I cannot find this in the documents.'

Rules:
- Do NOT hallucinate
- Do NOT add external knowledge
- Always mention source document name
"""

class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()

        self.llm = ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=settings.temperature,
        )

    def answer(self, question: str):
        chunks = self.retriever.retrieve(question)

        if not chunks:
            return {
                "answer": "No documents found.",
                "sources": [],
                "chunks_used": 0
            }

        context = "\n\n---\n\n".join(
            f"[Source: {c['source']}]\n{c['content']}"
            for c in chunks
        )

        messages = [
            SystemMessage(content=f"{SYSTEM_PROMPT}\n\nCONTEXT:\n{context}"),
            HumanMessage(content=question),
        ]

        response = self.llm.invoke(messages)

        return {
            "answer": response.content,
            "sources": list({c["source"] for c in chunks}),
            "chunks_used": len(chunks),
            "top_score": chunks[0]["score"]
        }