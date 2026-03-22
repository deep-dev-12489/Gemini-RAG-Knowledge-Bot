import os
import streamlit as st
from dotenv import load_dotenv
from operator import itemgetter

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# --- Configuration & Setup ---
load_dotenv()
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

# --- UI Sidebar ---
st.sidebar.title("🤖 Project Status")
st.sidebar.info(
    "**Phase 5 Active:** Streamlit UI Integration\n\n"
    "✅ Database connected\n"
    "✅ LCEL architecture (Modern LangChain Core)\n"
    "✅ Memory active\n"
    "✅ Strict custom prompt enforced"
)

# Clear chat function
def clear_chat_history():
    st.session_state.messages = []
    st.session_state.chat_history = []

if st.sidebar.button("🗑️ Clear Chat"):
    clear_chat_history()


# --- Main Application Header ---
st.title("📚 Document QA Assistant")
st.write("Welcome! I'm ready to answer questions based strictly on the context of your uploaded documents.")


# --- State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Core Logic Loading ---
@st.cache_resource
def load_rag_components():
    if not os.environ.get("GOOGLE_API_KEY"):
        st.error("ERROR: Missing GOOGLE_API_KEY. Please add your key to the .env file.")
        st.stop()

    db_dir = "./chroma_db"
    if not os.path.exists(db_dir):
        st.error(f"ERROR: No database found at {db_dir}. Please run ingest.py first!")
        st.stop()

    # Load Embeddings & Vector Store
    api_key = os.environ.get("GOOGLE_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", 
        google_api_key=api_key
    )
    vector_store = Chroma(persist_directory=db_dir, embedding_function=embeddings)
    
    # Load LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0,
        google_api_key=api_key
    )
    
    # Strict prompt template
    system_prompt = (
        "You are a focused assistant. Use ONLY the provided context to answer the question.\n"
        "If the answer is not in the context, say 'I'm sorry, that information is not in my current knowledge base.'\n"
        "Do not make up information.\n\n"
        "Context:\n{context}"
    )
    
    # Chat prompt with history placeholder
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Modern LCEL Chain (LangChain Expression Language)
    rag_chain = (
        {
            "context": itemgetter("question") | retriever | format_docs,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history")
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

qa_chain = load_rag_components()

# --- Chat Interface ---
# 1. Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Handle user chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Render user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Render assistant response with a loading spinner
    with st.chat_message("assistant"):
        with st.spinner("Searching my knowledge base..."):
            try:
                # Ask the chain, passing in explicit history
                answer = qa_chain.invoke({
                    "question": prompt,
                    "chat_history": st.session_state.chat_history
                })
                st.markdown(answer)
                
                # Save visual history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # Save memory history for LangChain
                st.session_state.chat_history.extend([
                    HumanMessage(content=prompt),
                    AIMessage(content=answer)
                ])
            except Exception as e:
                st.error(f"An error occurred: {e}")
