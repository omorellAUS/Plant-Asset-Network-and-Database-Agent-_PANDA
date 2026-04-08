import gradio as gr
import os
from pathlib import Path
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

def import_shutdown_folder(folder_path: str):
    """Recursively scan shutdown folder and group by Work Order sub-folders"""
    folder_path = Path(folder_path)
    if not folder_path.exists():
        return "Error: Folder not found."

    results = []
    for wo_folder in folder_path.iterdir():
        if wo_folder.is_dir():
            wo_name = wo_folder.name
            files = list(wo_folder.glob("**/*.*"))
            file_count = len(files)
            results.append(f"Work Order: {wo_name} | Files found: {file_count}")

    if not results:
        return "No Work Order sub-folders found in the selected shutdown folder."

    summary = "\n".join(results)
    return f"Successfully scanned shutdown folder:\n\n{summary}\n\nFiles have been indexed. You can now ask PANDA questions about these jobs."

def panda_agent(message: str):
    rag_text = str(query_engine.query(message)) if query_engine else "No documents loaded yet."
    
    full_input = f"User Query: {message}\n\nRelevant Context:\n{rag_text}"
    
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=full_input)
    ])
    return response

# ====================== Gradio UI ======================
with gr.Blocks(title="PANDA", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# PANDA\n**Plant Asset and Network Database Agent**\nPersistent knowledge bridge for BHP maintenance")

    chatbot = gr.Chatbot(height=650, label="PANDA Chat", show_copy_button=True)

    with gr.Tab("Import Data"):
        with gr.Row():
            folder_btn = gr.Button("Import Shutdown Folder", variant="primary", size="large")
            space_btn = gr.Button("Import from Webex Space Link")

        shutdown_folder = gr.Textbox(label="Selected Shutdown Folder", interactive=False)
        space_link = gr.Textbox(label="Paste Webex Space Link", placeholder="webexteams://im?spaceId=...")

    msg = gr.Textbox(
        placeholder="Example: Summarise changes and flag un-actioned items for SouthFlank Shut Part 1 Work Orders",
        label="Ask PANDA",
        lines=2
    )

    def import_folder():
        # This will be replaced with actual folder picker in next iteration
        return "Folder import feature active. Select a shutdown folder containing Work Order sub-folders."

    def import_space_link(link):
        if not link:
            return "Please paste a Webex Space Link."
        return f"Webex Space Link received: {link}\n\nFor now, export the chat manually and drop files into the correct Work Order folder in my_knowledge_base."

    folder_btn.click(import_folder, None, shutdown_folder)
    space_btn.click(import_space_link, space_link, chatbot)

    def respond(message, chat_history):
        if not message.strip():
            return "", chat_history
        bot_message = panda_agent(message)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    gr.Markdown("""
    **How to use PANDA**
    • Click "Import Shutdown Folder" and select the main shutdown folder (containing Work Order sub-folders).  
    • Drop Webex transcripts, photos, notes into the correct WO folders.  
    • Ask questions about changes, accountability, or reliability trends.  
    All outputs are for human review only.
    """)

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    inbrowser=True
)
