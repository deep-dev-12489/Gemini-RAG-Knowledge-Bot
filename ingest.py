import os
import glob
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables (api keys) from a .env file
load_dotenv()

def ingest_files():
    # 1. Validation check for API Key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: Missing GOOGLE_API_KEY. Please add your key to the .env file.")
        return

    print("\n--- STEP 1: Loading Files ---")
    documents = []
    
    # Load all PDFs in the current directory
    pdf_files = glob.glob("*.pdf")
    for pdf_file in pdf_files:
        print(f"Loading PDF: {pdf_file}...")
        try:
            loader = PyPDFLoader(pdf_file)
            documents.extend(loader.load())
        except Exception as e:
            print(f"Error loading {pdf_file}: {e}")
            
    # Load all Text files in the current directory
    txt_files = glob.glob("*.txt")
    for txt_file in txt_files:
        print(f"Loading TXT: {txt_file}...")
        try:
            loader = TextLoader(txt_file, encoding='utf-8')
            documents.extend(loader.load())
        except Exception as e:
            print(f"Error loading {txt_file}: {e}")

    if not documents:
        print("ERROR: No .pdf or .txt files found to ingest in the current directory.")
        return

    print(f"Successfully loaded {len(documents)} document pages/sections.")

    print("\n--- STEP 2: Splitting text into chunks ---")
    # Using Recursive character splitter for better contextual cutoffs
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Broke documents down into {len(chunks)} chunks.")

    print("\n--- STEP 3: Creating Embeddings and Vector Store ---")
    print("Communicating with Google Gemini to create numerical embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    # Store the result in local ChromaDB directory
    db_dir = "./chroma_db"
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )
    
    print(f"\nSuccess! The knowledge base has been processed and saved locally to '{db_dir}'.")
    print("You can now run 'chat.py' to ask questions about your documents!")

if __name__ == "__main__":
    ingest_files()
