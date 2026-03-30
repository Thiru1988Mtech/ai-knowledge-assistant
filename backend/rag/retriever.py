import chromadb
from chromadb.utils import embedding_functions
from backend.config import settings

class Retriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_path)

        self.embed_fn = embedding_functions.OllamaEmbeddingFunction(
            url=f'{settings.ollama_base_url}/api/embeddings',
            model_name=settings.embed_model,
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            embedding_function=self.embed_fn,
        )

    def retrieve(self, query: str, top_k: int = None):
        k = top_k or settings.top_k

        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=min(k, self.collection.count())
        )

        return [
            {
                "content": doc,
                "source": meta.get("source", "unknown"),
                "score": round(1 - dist, 4)
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]