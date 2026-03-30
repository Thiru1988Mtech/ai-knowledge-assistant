import logging
from pathlib import Path
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from backend.config import settings

logger = logging.getLogger(__name__)

class DocumentIngestor:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_path)

        self.embed_fn = embedding_functions.OllamaEmbeddingFunction(
            url=f'{settings.ollama_base_url}/api/embeddings',
            model_name=settings.embed_model,
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            embedding_function=self.embed_fn,
            metadata={'hnsw:space': 'cosine'},
        )

    def _chunk_text(self, text: str, chunk_size=500, overlap=50):
        words = text.split()
        chunks, i = [], 0

        while i < len(words):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap

        return [c for c in chunks if len(c.strip()) > 50]

    def ingest_pdf(self, file_path: str):
        path = Path(file_path)

        reader = PdfReader(file_path)
        full_text = '\n'.join(p.extract_text() or '' for p in reader.pages)

        chunks = self._chunk_text(full_text)

        ids = [f'{path.stem}_{i}' for i in range(len(chunks))]
        metas = [{'source': path.name, 'chunk': i} for i in range(len(chunks))]

        existing = set(self.collection.get(ids=ids)['ids'])
        new_ids = [id for id in ids if id not in existing]

        if not new_ids:
            print("Already ingested")
            return 0

        idx = [ids.index(i) for i in new_ids]

        self.collection.add(
            ids=new_ids,
            documents=[chunks[i] for i in idx],
            metadatas=[metas[i] for i in idx],
        )

        print(f"Ingested {len(new_ids)} chunks")
        return len(new_ids)

    def collection_stats(self):
        return {"total_chunks": self.collection.count()}