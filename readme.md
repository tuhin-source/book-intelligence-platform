### Ergosphere Intel: AI-Powered Book Intelligence Platform

Ergosphere Intel is a sophisticated RAG (Retrieval-Augmented Generation) platform designed to transform static book catalogs into interactive intelligence hubs. It combines a high-performance Django backend with a modern React frontend to allow users to explore book metadata and perform deep-contextual queries across the entire library using LLMs.

🚀 Key Features

Intelligence Nexus (RAG Chat): Perform semantic searches and ask complex questions across cataloged books.

Automated Catalog: A dynamic, responsive bookshelf view that pulls real-time metadata from a PostgreSQL/SQLite database.

Source Attribution: Every AI response includes specific source citations from the library to ensure accuracy and reduce hallucinations.

Modern UI/UX: Built with React, Tailwind CSS, and Lucide icons, featuring a sleek dark-mode navigation and glass-morphism card designs.

🏗️ Architecture

The platform follows a decoupled architecture:

Frontend: React (Vite) + Tailwind CSS (Client-side logic and UI).

Backend: Django REST Framework (API, Database management, and Auth).

AI Engine: LangChain + OpenAI/Anthropic (Vector embeddings and Retrieval logic).

Vector Store: FAISS/ChromaDB (Stores mathematical representations of book content for semantic search).

🛠️ Installation & Setup

1. Prerequisites

Python 3.9+

Node.js 18+

API Key (OpenAI or Gemini)

2. Backend Setup

# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver


3. Frontend Setup

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev


🤖 How the RAG System Works

Ingestion: Book contents are processed and broken into small, semantic "chunks."

Embedding: These chunks are converted into high-dimensional vectors using an Embedding Model.

Storage: Vectors are stored in a specialized Vector Database.

Retrieval: When a user asks a question, the system finds the most relevant "chunks" based on vector similarity.

Generation: The LLM uses the retrieved chunks as "context" to generate a precise, cited answer.

📸 Screenshots

Bookshelf View

AI Assistant (Nexus)

#### Screenshots from my app

## Quering Part
<img width="944" height="398" alt="image" src="https://github.com/user-attachments/assets/c3867c0a-2d3b-4772-b044-be67c7bf81c7" />
## Books from database
<img width="953" height="412" alt="image" src="https://github.com/user-attachments/assets/83c115c9-ef5d-4d90-9cab-174a7b8c3880" />

📝 Example Queries to Try

"What are the recurring themes across the biology-related books?"

"Summarize the primary argument of [Book Title] based on the catalog data."

"Which books discuss the concept of ergospheres or black holes?"

🛠️ Tech Stack

Frontend: React, Vite, Tailwind CSS, Lucide-React, Axios.

Backend: Django, Django REST Framework, CORS-headers.

AI/ML: LangChain, OpenAI API, FAISS.

🛡️ License

not licensed 
