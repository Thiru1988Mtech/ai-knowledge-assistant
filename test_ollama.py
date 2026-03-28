from langchain_ollama import ChatOllama

# Initialize LLM
llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434"
)

# Ask a question
response = llm.invoke("Explain RAG in simple terms")

# Print response
print(response.content)