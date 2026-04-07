import gradio as gr
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from system_prompt import SYSTEM_PROMPT

load_dotenv()

DATA_DIR = "./my_knowledge_base"

Settings.embed_model = HuggingFaceEmbedding(model_name="nomic-embed-text")

def get_query_engine():
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        return None
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()

query_engine = get_query_engine()

# Tailored for your 12GB GPU + 32GB RAM
llm = ChatOllama(
    model="llama3.3:8b",      # Strong and fast on your hardware
    temperature=0.1,
    num_gpu=999,              # Let Ollama use full GPU
    num_ctx=8192              # Higher context thanks to your RAM
)

def panda_agent(message, history):
    rag_text = str(query_engine.query(message)) if query_engine else "No RAG data loaded yet."
    
    full_prompt = f"""
User query: {message}
RAG context: {rag_text}
"""
    response = llm.invoke([SystemMessage(content=SYSTEM_PROMPT)] + [HumanMessage(content=full_prompt)])
    return response

with gr.Blocks(title="PANDA - Plant Asset Truth Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# PANDA\n**Plant Asset and Network Database Agent**\nCentral nervous system for BHP maintenance & reliability")

    chatbot = gr.Chatbot(height=650, label="PANDA Chat")
    msg = gr.Textbox(
        placeholder="Example: Summarise changes to Pump XYZ BOM from this week's Webex and flag any un-actioned items",
        label="Ask PANDA"
    )

    def respond(message, chat_history):
        bot_message = panda_agent(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    gr.Markdown("**How to use:** Drop Webex notes, Fiori exports, Sphera permits, photos, VA reports, manuals into `my_knowledge_base` folder.\nFuture: Direct API integration + automatic accountability reports.")

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    share=False,
    favicon_path=None
)
