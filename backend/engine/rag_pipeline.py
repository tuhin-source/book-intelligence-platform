import os
import django
import pandas as pd
from dotenv import load_dotenv

# LangChain & AI Imports
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
from langchain_community.document_loaders import DataFrameLoader

# --- Django Setup ---
import sys
# Adjust path so we can import Django models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Book

load_dotenv()

class BookRAGPipeline:
    def __init__(self):
        """Initialize models and Vector DB connections."""
        # Requirements: Local Embeddings (all-MiniLM-L6-v2) [cite: 74, 122]
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.persist_dir = "./chroma_db"
        
        # Requirements: LLM Setup (Gemini 1.5 Flash) [cite: 79]
        self.llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

    def ingest_data(self):
        """
        1. Collects book data from MySQL [cite: 30]
        2. Performs Smart Chunking 
        3. Generates Embeddings and stores in ChromaDB [cite: 41, 42]
        """
        print("🔋 Ingesting data from MySQL to Vector DB...")
        
        # Fetch metadata from MySQL [cite: 71]
        books = Book.objects.all().values('id', 'title', 'description', 'rating', 'book_url')
        if not books:
            print("⚠️ No books found in MySQL. Please run the scraper first.")
            return

        df = pd.DataFrame(list(books))
        
        # Requirement: "Construct relevant context" - combining title and description [cite: 43]
        df['combined_text'] = df.apply(lambda row: f"Title: {row['title']}. Description: {row['description']}", axis=1)
        
        loader = DataFrameLoader(df, page_content_column="combined_text")
        docs = loader.load()

        # Bonus: Smart Chunking Strategy (Overlapping windows) [cite: 113]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600, 
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " "]
        )
        splits = text_splitter.split_documents(docs)

        # Requirement: Vector Search using ChromaDB [cite: 74, 108]
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        print(f"✅ Successfully indexed {len(splits)} chunks into ChromaDB.")

    def get_qa_chain(self):
        """Builds the RAG Chain with required Insight Generation[cite: 35, 40]."""
        
        # Custom Prompt Template to return Summary, Genre, and Recommendations [cite: 36, 38, 52]
        template = """
        You are a Book Intelligence Assistant. Use the provided context to answer the question.
        
        Context: {context}
        Question: {question}

        Follow this format strictly:
        ANSWER: [Provide a detailed contextual answer]
        SUMMARY: [Provide a 2-sentence summary of the specific books discussed]
        GENRE: [Identify the primary genre of these books]
        RECOMMENDATIONS: [If you like these, mention 1-2 other relevant books from the context]
        SOURCES: [Cite the specific Book Titles used to answer this query]
        """
        
        PROMPT = PromptTemplate(
            template=template, 
            input_variables=["context", "question"]
        )

        # Requirement: Return source citations 
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

    def query(self, user_question):
        """Executes the RAG query and extracts results safely."""
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir, 
            embedding_function=self.embeddings
        )
        chain = self.get_qa_chain()
        
        print(f"🔍 Processing Question: {user_question}")
        response = chain.invoke(user_question)
        
        # Safely extract titles from metadata
        sources = []
        for doc in response.get("source_documents", []):
            # Try 'title' first, then fallback to other common keys or 'Unknown'
            title = doc.metadata.get('title') or doc.metadata.get('row_title') or "Untitled Source"
            sources.append(title)
            
        return {
            "result": response["result"],
            "sources": list(set(sources)) # Remove duplicates
        }

if __name__ == "__main__":
    # --- Execution Logic ---
    rag = BookRAGPipeline()
    
    # Run ingestion only if chroma_db doesn't exist or data changed
    if not os.path.exists("./chroma_db"):
        rag.ingest_data()
    
    # Test Question (Requirement 94)
    sample_query = "Find me science books about evolution and explain what they cover."
    output = rag.query(sample_query)
    
    print("\n--- SYSTEM OUTPUT ---")
    print(output["result"])
    print(f"Verified Sources: {output['sources']}")