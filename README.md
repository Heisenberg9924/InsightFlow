# 🧠 InsightFlow AI

> Hybrid Document Intelligence Platform powered by Semantic Retrieval and Knowledge Graphs.

InsightFlow AI is an end-to-end document understanding platform that transforms unstructured documents into searchable knowledge using semantic embeddings and structured knowledge graphs.

Instead of relying solely on traditional Retrieval-Augmented Generation (RAG), InsightFlow AI combines vector retrieval with an Open Knowledge Format (OKF) graph to enable richer document understanding.

---

# ✨ Features

- 📄 Multi-document upload
    - PDF
    - DOCX
    - TXT

- 🔍 Automatic document parsing

- 🧩 Semantic Knowledge Unit generation

- 🧠 Embedding generation using BGE embeddings

- ⚡ High-speed semantic search using FAISS

- 🌐 Automatic Knowledge Graph generation using Gemini

- 💬 Conversational document chat

- 🗂 Conversation history

- ⚙ Modular FastAPI backend

- 🎨 Streamlit frontend

---

# 🏗 Architecture

```
                    ┌──────────────────────────┐
                    │     Upload Document      │
                    └─────────────┬────────────┘
                                  │
                                  ▼
                     Document Parsing Pipeline
                                  │
                                  ▼
                     Knowledge Unit Generation
                        │                 │
                        │                 │
                        ▼                 ▼
               Embedding Generator     OKF Extraction
                        │                 │
                        ▼                 ▼
                    FAISS Index      Knowledge Graph
                        │                 │
                        └────────┬────────┘
                                 ▼
                         Hybrid Retrieval
                                 ▼
                            Gemini 2.5 Flash
                                 ▼
                           Streamlit Chat UI
```

---

# 🛠 Tech Stack

## Backend

- FastAPI
- Python

## Database

- MongoDB

## Embeddings

- BAAI BGE Small v1.5

## Vector Search

- FAISS

## Knowledge Graph

- Custom Open Knowledge Format (OKF)

## LLM

- Gemini 2.5 Flash

## Frontend

- Streamlit

---

# 📂 Project Structure

```
InsightFlow/
│
├── app/
│   ├── api/
│   ├── database/
│   ├── parsers/
│   ├── processors/
│   ├── knowledge_units/
│   ├── embeddings/
│   ├── retrieval/
│   ├── okf/
│   ├── llm/
│   └── document_store/
│   └── retrieval/
|   └── chat/
|
├── frontend/
│
├── storage/
│
├── uploads/
│
├── pyproject.toml
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/InsightFlow.git

cd InsightFlow
```

Install dependencies

```bash
uv sync
```

Create a `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY
MONGODB_URI=mongodb://localhost:27017
GEMINI_MODEL=gemini-2.5-flash
```

---

# 🚀 Running the Backend

```bash
uv run fastapi dev
```

Backend

```
http://127.0.0.1:8000
```

API Docs

```
http://127.0.0.1:8000/docs
```

---

# 🎨 Running the Frontend

```bash
uv run streamlit run frontend/app.py
```

---

# 💬 How It Works

1. Upload a document.
2. The document is parsed into semantic sections.
3. Sections are converted into Knowledge Units.
4. Knowledge Units are embedded using BGE.
5. Gemini extracts entities and relationships to generate an OKF Knowledge Graph.
6. Embeddings are indexed in FAISS.
7. User questions retrieve relevant semantic context.
8. The retrieved context is sent to Gemini to generate grounded answers.

---

# 🧠 Open Knowledge Format (OKF)

InsightFlow AI introduces an intermediate structured representation called the **Open Knowledge Format (OKF)**.

Each document is transformed into a graph containing:

- Nodes
- Relationships
- Properties

Example

```
Python ──USES──► FastAPI
FastAPI ──USES──► REST API
```

The graph is used alongside semantic retrieval to provide additional structured context during question answering.


# 🚧 Current Limitations

- Graph retrieval currently performs lightweight entity matching.
- FAISS is used as the development vector database.
- Graph reasoning and multi-hop traversal are planned for future releases.

---

# 🔮 Roadmap

- Hybrid GraphRAG Retrieval

- Multi-hop Knowledge Graph Traversal

- Neo4j Integration

- Qdrant Vector Database

- Cross-Encoder Re-ranking

- Agentic Document Analysis

- Executive Report Generation

- Knowledge Graph Visualization

---

# 🤝 Contributing

Contributions are welcome.

Feel free to open issues or submit pull requests.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Rupdeep Ray**

B.Tech Computer Science and Engineering

National Institute of Technology Durgapur

GitHub: https://github.com/Heisenberg9924