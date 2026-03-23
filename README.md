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

## 📸 Screenshots & Demo

To see the Intelligent RAG Document Assistant in action, including the terminal data ingestion process, the interactive Streamlit UI, and the strict zero-hallucination protocol, please view the project gallery below:

[**🔗 View Project Screenshots (Google Docs)**](https://docs.google.com/document/d/1UGcxFVI9emYG7cnDOYn6vzo1pB2y3x9w33EH-Tbly8M/edit?usp=sharing)

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
