import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

def start_chat():
    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: Missing GOOGLE_API_KEY. Please add your key to the .env file.")
        return

    db_dir = "./chroma_db"
    if not os.path.exists(db_dir):
        print(f"ERROR: No database found at {db_dir}. Please run ingest.py first!")
        return

    print("Loading vector database and LLM...")
    
    # 1. Load the existing Chroma vector store using gemini-embedding-001
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = Chroma(persist_directory=db_dir, embedding_function=embeddings)
    
    # 2. Connect to the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # 3. Create Memory and Prompt Template
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    system_prompt = (
        "You are a focused assistant. Use ONLY the provided context to answer the question. "
        "If the answer is not in the context, say 'I'm sorry, that information is not in my current knowledge base.' "
        "Do not make up information."
    )
    
    prompt_template = system_prompt + "\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    CUSTOM_PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # Create the Conversational Retrieval Chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": CUSTOM_PROMPT}
    )

    print("\n" + "="*50)
    print("RAG Chatbot Initialized (Powered by Gemini)!")
    print("Ask a question about your documents. Type 'exit' or 'quit' to stop.")
    print("="*50 + "\n")

    # 4. Set up the interactive chat loop
    while True:
        try:
            user_input = input("\nYou: ")
        except EOFError:
            break
            
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
            
        if not user_input.strip():
            continue

        print("Bot is searching the Vector DB and thinking...")
        try:
            response = qa_chain.invoke({"question": user_input})
            print(f"\nBot: {response['answer']}")
        except Exception as e:
            print(f"\nError generating answer: {e}")

if __name__ == "__main__":
    start_chat()
