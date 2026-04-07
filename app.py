import gradio as gr
import os
from dotenv import load_dotenv
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

# Optimized for your desktop (12GB GPU + 32GB RAM)
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.1,
    num_gpu=999,
    num_ctx=8192
)

def panda_agent(message: str):
    """Core PANDA reasoning function"""
    rag_text = str(query_engine.query(message)) if query_engine else "No documents loaded in my_knowledge_base yet."

    full_input = f"""
User Query: {message}

Relevant Context from Knowledge Base:
{rag_text}
"""

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=full_input)
    ])
    return response

# ====================== Gradio Web UI ======================
with gr.Blocks(
    title="PANDA - Plant Asset Truth Agent",
    theme=gr.themes.Soft()
) as demo:
    
    gr.Markdown("""
    # PANDA
    **Plant Asset and Network Database Agent**  
    Persistent knowledge bridge between field execution and future planning
    """)

    chatbot = gr.Chatbot(
        height=700,
        label="PANDA Chat",
        show_copy_button=True,
        avatar_images=(None, "🛠️")
    )

    msg = gr.Textbox(
        placeholder="Example: Summarise execution reality for CV203 Drive Pulley from recent Webex and flag any un-actioned items",
        label="Ask PANDA",
        lines=2
    )

    with gr.Row():
        submit_btn = gr.Button("Send", variant="primary")
        clear_btn = gr.Button("Clear Chat")
        upload_btn = gr.File(label="Upload files (Webex notes, photos, Fiori exports, etc.)", file_count="multiple")

    def respond(message, chat_history):
        if not message or not message.strip():
            return "", chat_history
        bot_message = panda_agent(message)
        chat_history.append((message, bot_message))
        return "", chat_history

    def clear_history():
        return []

    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(clear_history, None, chatbot)

    gr.Markdown("""
    **How to use PANDA**  
    Drop Webex notes, Fiori exports, Sphera permits, photos, VA reports, manuals and drawings into the `my_knowledge_base` folder.  
    PANDA will highlight patterns, discrepancies and un-actioned items with transparent confidence levels.  
    All outputs are for human review only.
    """)

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    share=False,
    inbrowser=True
)
