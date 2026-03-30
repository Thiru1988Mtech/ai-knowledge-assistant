from backend.rag.ingestor import DocumentIngestor

ingestor = DocumentIngestor()

# 👉 Change this path if needed
file_path = "data/AI Architect JD(26) - Azure.pdf"

count = ingestor.ingest_pdf(file_path)

print("Chunks ingested:", count)
print("Collection stats:", ingestor.collection_stats())