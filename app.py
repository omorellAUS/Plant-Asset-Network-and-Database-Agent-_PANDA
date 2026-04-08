import gradio as gr
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from system_prompt import SYSTEM_PROMPT

load_dotenv()

DATA_DIR = "./my_knowledge_base"

# Changed to a more reliable embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_query_engine():
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        print("Warning: my_knowledge_base folder is empty. Add your documents.")
        return None
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()

query_engine = get_query_engine()

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.1,
    num_gpu=999,
    num_ctx=8192
)

def panda_agent(message: str):
    rag_text = str(query_engine.query(message)) if query_engine else "No documents loaded in my_knowledge_base yet."
    
    full_input = f"User Query: {message}\n\nRelevant Context:\n{rag_text}"
    
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=full_input)
    ])
    return response

with gr.Blocks(title="PANDA", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# PANDA\n**Plant Asset and Network Database Agent**\nPersistent knowledge bridge for BHP maintenance")

    chatbot = gr.Chatbot(height=700, label="PANDA Chat", show_copy_button=True)

    msg = gr.Textbox(
        placeholder="Example: Summarise observations from the Nyrstar Hobart blower overhaul and flag any accountability gaps",
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

    gr.Markdown("Drop your job files (Webex notes, Fiori exports, photos, VA reports, manuals) into the `my_knowledge_base` folder.")

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    inbrowser=True
)
