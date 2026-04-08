import gradio as gr
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from system_prompt import SYSTEM_PROMPT

load_dotenv()

DATA_DIR = "./my_knowledge_base"

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_query_engine():
    if not os.path.exists(DATA_DIR):
        print(f"ERROR: Folder '{DATA_DIR}' does not exist!")
        return None

    print(f"Scanning '{DATA_DIR}' and all subfolders...")
    file_count = 0
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            file_count += 1
            print(f"  Found: {os.path.join(root, file)}")

    print(f"Total files found: {file_count}")

    if file_count == 0:
        print("WARNING: No files found.")
        return None

    try:
        documents = SimpleDirectoryReader(DATA_DIR, recursive=True).load_data()
        print(f"Successfully loaded {len(documents)} documents.")
        index = VectorStoreIndex.from_documents(documents)
        return index.as_query_engine()
    except Exception as e:
        print(f"ERROR loading documents: {e}")
        return None

query_engine = get_query_engine()

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.1,
    num_gpu=999,
    num_ctx=8192
)

def panda_agent(message: str):
    if query_engine is None:
        return "Knowledge base is empty. Add files to my_knowledge_base and restart."

    try:
        rag_text = str(query_engine.query(message))
    except Exception as e:
        rag_text = f"RAG error: {e}"

    full_input = f"User Query: {message}\n\nRelevant Context:\n{rag_text}"

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=full_input)
    ])
    return response.content if hasattr(response, 'content') else str(response)

with gr.Blocks(title="PANDA") as demo:
    gr.Markdown("# PANDA - Plant Asset Truth Agent")

    chatbot = gr.Chatbot(height=700, label="PANDA Chat")

    msg = gr.Textbox(
        placeholder="Example: Summarise the Nyrstar Blower Overhaul and flag accountability gaps",
        label="Ask PANDA",
        lines=2
    )

    def respond(message, chat_history):
        if not message.strip():
            return "", chat_history
        bot_message = panda_agent(message)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    gr.Markdown("**Tip:** Files are in my_knowledge_base. Restart Launch PANDA.bat after adding new files.")

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    inbrowser=True,
    show_error=True
)
