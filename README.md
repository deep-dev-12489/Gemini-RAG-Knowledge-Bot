# 🤖 Project Zero: Intelligent RAG Document Assistant

## 📖 About the Project
This project is an advanced, fully functional **Retrieval-Augmented Generation (RAG)** chatbot designed to answer questions strictly based on a provided knowledge base. Leveraging the power of Google's Gemini models and LangChain's Expression Language (LCEL), the assistant maintains conversation memory and strictly adheres to a zero-hallucination protocol—if the information isn't in the provided documents, it will honestly tell you it doesn't know.

## 🚀 Key Features
- **Strict RAG Protocol:** Enforces a rigid prompt template to eliminate AI hallucinations. 
- **Conversation Memory:** Context-aware chat functionality that remembers follow-up questions seamlessly.
- **Dynamic UI:** A clean, intuitive dashboard built natively with Streamlit.
- **Local Vector Database:** Fast, scalable document embeddings stored locally using ChromaDB.

## 💻 Tech Stack
- **Python 3.x:** Core programming language.
- **Streamlit:** Frontend web framework building the interactive dashboard.
- **LangChain:** LLM framework orchestrating memory, LCEL chains, and retrieval.
- **Google Gemini API:** Powering the intelligence (`gemini-2.5-flash`) and numerical embeddings (`gemini-embedding-001`).
- **ChromaDB:** Local vector database for semantic search.

---

## 📸 Screenshots

*(Replace the placeholder links below with your screenshots!)*

### 1. Ingestion Success
> *Take a screenshot of your terminal showing the successful output of `ingest.py` processing the documents and saving to ChromaDB.*  
![Ingestion Terminal Screenshot](docs/ingestion.png)

### 2. UI Dashboard & Memory
> *Take a screenshot of the Streamlit interface showing a successful Q&A interaction and follow-up question.*  
![UI Dashboard Screenshot](docs/dashboard.png)

### 3. Strict Response Protocol
> *Take a screenshot showing the chatbot correctly refusing to answer an off-topic question (e.g. "What is the capital of France?").*  
![Strict Response Screenshot](docs/strict-protocol.png)

---

## 🛠️ Installation Guide

Follow these steps to run the RAG chatbot on your local machine:

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up the Environment Variables**
Create a `.env` file in the root directory and add your Google API key:
```env
GOOGLE_API_KEY="your_actual_api_key_here"
```

**4. Ingest your Data**
Add any `.txt` or `.pdf` files to the root directory, then run:
```bash
python ingest.py
```

**5. Start the Application**
```bash
streamlit run app.py
```
