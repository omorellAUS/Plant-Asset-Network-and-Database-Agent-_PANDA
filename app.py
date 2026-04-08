import gradio as gr
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from system_prompt import SYSTEM_PROMPT

load_dotenv()

DATA_DIR = "./my_knowledge_base"

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

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

def handle_webex_space_link(space_link: str):
    if not space_link:
        return "Please paste a Webex Space Link."
    
    return f"""
Webex Space Link received: {space_link}

**For this alpha test (Nyrstar Hobart Blower Overhaul):**

1. Open the Webex space "nyrstar hobart blower overhaul"
2. Export the chat (copy all messages or download transcript if available)
3. Save any attached Word docs, PDFs, and pictures
4. Drop all exported files into the `my_knowledge_base` folder (or create a subfolder named "Nyrstar blower overhaul")
5. Then ask PANDA questions about the content.

PANDA will process the files using the full system rules (accountability, change tracking, confidence levels, first principles thinking).

You can paste more space links as needed.
"""

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

    chatbot = gr.Chatbot(height=680, label="PANDA Chat", show_copy_button=True)

    with gr.Tab("Import Webex"):
        gr.Markdown("**Test Space:** nyrstar hobart blower overhaul")
        space_link = gr.Textbox(label="Paste Webex Space Link", placeholder="webexteams://im?spaceId=...")
        import_btn = gr.Button("Process Webex Space Link", variant="primary")

    msg = gr.Textbox(
        placeholder="Example: Summarise observations from the Nyrstar Hobart blower overhaul and flag any accountability gaps or potential BOM changes",
        label="Ask PANDA",
        lines=2
    )

    def process_space_link(link):
        return handle_webex_space_link(link)

    import_btn.click(process_space_link, space_link, chatbot)

    def respond(message, chat_history):
        if not message.strip():
            return "", chat_history
        bot_message = panda_agent(message)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    gr.Markdown("""
    **Alpha Test Instructions**
    • Paste the Webex Space Link above and click the button.  
    • Manually export the chat/files from the space and drop them into `my_knowledge_base`.  
    • Ask PANDA questions about the content.  
    PANDA will apply your full rules: first principles, evidence-only, accountability, and change tracking.
    """)

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    inbrowser=True
)
