## 📌 Phase 1 — Foundation & Setup

### 🎯 Objective
Establish a robust foundation for a local AI-powered knowledge assistant using a modular, production-ready architecture.

---

### ⚙️ Key Components Implemented

#### 🧠 Local LLM Integration
- Integrated Ollama for running local models  
- Used `llama3.2` for inference  
- Eliminated dependency on external APIs (privacy + cost optimization)

---

#### 🏗️ Project Structure
ai-knowledge-assistant/
│
├── backend/ # Core AI logic
├── frontend/ # UI layer (planned)
├── data/ # Input documents
├── eval_dataset/ # Evaluation datasets
├── tests/ # Unit testing
├── docker/ # Deployment configs
├── README.md # Documentation


---

#### 🐍 Virtual Environment Setup
- Created isolated Python environment using `venv`
- Ensured dependency management and reproducibility

---

#### 📦 Dependency Management
- Installed and resolved dependencies for:
  - LangChain  
  - LangGraph  
  - ChromaDB  
  - FastAPI  
- Handled multiple version conflicts (real-world scenario)

---

#### 🔧 Configuration Management
- Implemented `.env` for environment variables  
- Built centralized config using `pydantic-settings`  
- Enabled flexible and scalable configuration  

---

#### 🔗 GitHub Integration
- Initialized Git repository  
- Connected to GitHub  
- Maintained clean repo using `.gitignore`  
- Removed unnecessary files (`venv/`)  

---

#### 🧪 LLM Testing
- Successfully tested LLM response using Python  
- Verified end-to-end integration of:
  - LangChain  
  - Ollama  

---

### ✅ Outcome

- Fully functional local LLM system  
- Clean project architecture  
- Production-ready configuration  
- Version-controlled codebase  

---

## Phase 2 — RAG Pipeline
🔍 Components Built:
1. Document Ingestion
PDF parsing using PyPDF
Text chunking (500 tokens with overlap)
Stored in ChromaDB vector database
2. Retrieval
Semantic search using embeddings
Top-K relevant chunks retrieved
3. Generation
LLM (Ollama) generates answers using retrieved context
Strict grounding to avoid hallucination
🔄 RAG Flow:

User Query
→ Embedding
→ Vector Search (ChromaDB)
→ Relevant Chunks
→ LLM (Ollama)
→ Final Answer

🎯 Outcome:
Context-aware answers
Reduced hallucination
Source-based responses 

# 🤖 Phase 3 — LangGraph Multi-Agent System

### 🧠 Overview

This phase introduces a **stateful multi-agent system** using LangGraph, implementing the **ReAct (Reason → Act → Observe)** pattern.

The agent dynamically decides when to:

* Answer directly
* Call tools
* Iterate until a final response is generated

---

### 🔧 Components

#### 1. Agent State

Maintains execution context:

* User messages
* Intermediate steps
* Retrieved context
* Final answer
* Iteration count

---

#### 2. Agent Node (Reasoning Engine)

* Uses LLM (Ollama)
* Performs step-by-step reasoning
* Decides whether to call tools

---

#### 3. Tool Node (Execution Layer)

* Executes tools such as:

  * Knowledge base search
  * Topic summarisation
* Returns observations back to agent

---

#### 4. Router (Control Flow)

* Determines next step:

  * Continue reasoning (loop)
  * End execution

---

### 🔁 Execution Flow

User Query
→ Agent (Reasoning)
→ Tool Call (if needed)
→ Observation
→ Repeat (loop)
→ Final Answer

---

### 🎯 Outcome

* Multi-step reasoning capability
* Dynamic tool usage
* Explainable decision process (ReAct pattern)

---

# 🔌 Phase 4 — MCP (Model Context Protocol) Integration

### 🧠 Overview

This phase integrates **MCP (Model Context Protocol)** — an open standard for connecting LLMs with external tools via a structured protocol.

Instead of calling tools directly, the agent now communicates with a **dedicated MCP server**.

---

### 🔧 Architecture

Agent (LangGraph)
→ MCP Client
→ MCP Server (FastMCP)
→ Tools (RAG, Calculator, Stats, etc.)

---

### ⚙️ Key Components

#### 1. MCP Server (`backend/mcp/server.py`)

* Exposes tools using `@mcp.tool()`
* Tools implemented:

  * `search_knowledge_base`
  * `ask_knowledge_base`
  * `calculate`
  * `get_knowledge_base_stats`
  * `summarise_document_topic`

---

#### 2. MCP Client (`backend/mcp/client.py`)

* Connects agent to MCP server
* Handles async tool execution
* Provides sync wrapper for LangGraph integration

---

#### 3. LangChain Tool Bridge (`langchain_tools.py`)

* Converts MCP tools into LangChain-compatible format
* Enables LangGraph agent to call MCP tools seamlessly

---

### 🔁 MCP Flow

User Query
→ Agent
→ MCP Client
→ MCP Server
→ Tool Execution
→ Response
→ Agent → Final Answer

---

### 🎯 Outcome

* Decoupled tool architecture
* Standardised tool communication
* Scalable and modular system design
* Compatible with external AI systems (e.g., Claude)

---

### 🚀 Why MCP Matters

* Industry-standard protocol (Anthropic)
* Enables plug-and-play tool ecosystem
* Makes system production-ready
* Strong differentiator in AI/GenAI interviews

---
