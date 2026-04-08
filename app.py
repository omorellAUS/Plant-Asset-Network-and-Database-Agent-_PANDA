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

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.1,
    num_gpu=999,
    num_ctx=8192
)

def panda_agent(message: str):
    rag_text = str(query_engine.query(message)) if query_engine else "No documents in my_knowledge_base yet."

    full_input = f"""
User Query: {message}

Relevant Context:
{rag_text}
"""

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=full_input)
    ])
    return response

with gr.Blocks(title="PANDA", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# PANDA\n**Plant Asset and Network Database Agent**\nPersistent knowledge bridge for BHP maintenance")

    chatbot = gr.Chatbot(height=700, label="PANDA Chat", show_copy_button=True)

    msg = gr.Textbox(
        placeholder="Example: Summarise execution reality for CV203 from recent Webex and flag any un-actioned items with confidence levels",
        label="Ask PANDA",
        lines=2
    )

    with gr.Row():
        submit_btn = gr.Button("Send", variant="primary")
        clear_btn = gr.Button("Clear")

    def respond(message, chat_history):
        if not message.strip():
            return "", chat_history
        bot_message = panda_agent(message)
        chat_history.append((message, bot_message))
        return "", chat_history

    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(lambda: [], None, chatbot)

    gr.Markdown("Drop job files into `my_knowledge_base` folder. PANDA highlights patterns and discrepancies only — human review required.")

demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
