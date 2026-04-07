import gradio as gr
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from system_prompt import SYSTEM_PROMPT

load_dotenv()

# Configuration for your hardware
DATA_DIR = "./my_knowledge_base"

# Use local embeddings
Settings.embed_model = HuggingFaceEmbedding(model_name="nomic-embed-text")

def get_query_engine():
    """Load RAG from knowledge base folder"""
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        print("Warning: my_knowledge_base folder is empty. Add your documents.")
        return None
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()

query_engine = get_query_engine()

# LLM setup - Optimized for your 12GB GPU + 32GB RAM using qwen3:8b
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.1,      # Low temperature = more factual and consistent
    num_gpu=999,          # Full GPU offload
    num_ctx=8192,         # Large context window (your RAM can handle it)
    verbose=False
)

def panda_agent(message: str, history):
    """Main PANDA reasoning loop"""
    # Get relevant context from your knowledge base
    rag_text = str(query_engine.query(message)) if query_engine else "No documents loaded in my_knowledge_base yet."

    # Build the full prompt with context
    full_input = f"""
User Query: {message}

Relevant Context from Knowledge Base:
{rag_text}

Respond using the full PANDA system rules. Be blunt, factual, and always include source references where possible.
"""

    # Get response from the model using the strict system prompt
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=full_input)
    ])

    return response

# ====================== GRADIO WEB UI ======================
with gr.Blocks(
    title="PANDA - Plant Asset Truth Agent",
    theme=gr.themes.Soft(),
    css="""
    .chatbot { height: 680px; }
    """
) as demo:
    
    gr.Markdown("""
    # PANDA - Plant Asset and Network Database Agent
    **Central Nervous System for BHP Maintenance & Reliability**  
    Blunt • Factual • Accountability-Driven • Evidence-Based
    """)

    chatbot = gr.Chatbot(
        height=680,
        label="PANDA Chat",
        show_copy_button=True
    )

    msg = gr.Textbox(
        placeholder="Example: Summarise all changes discussed for Pump XYZ in this week's Webex and check if they were actioned in Fiori. Flag any accountability gaps.",
        label="Ask PANDA",
        lines=2
    )

    with gr.Row():
        clear_btn = gr.Button("Clear Chat")
        upload_btn = gr.File(label="Upload files (Webex notes, Fiori exports, photos, etc.)", file_count="multiple")

    def respond(message, chat_history):
        if not message.strip():
            return "", chat_history
        bot_message = panda_agent(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    def clear_history():
        return []

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(clear_history, None, chatbot)

    gr.Markdown("""
    **How to use PANDA:**
    • Drop Webex notes, Fiori work order exports, Sphera permits, VA reports, photos, manuals, and drawings into the `my_knowledge_base` folder.  
    • Ask questions about asset changes, accountability, reliability trends, or training on systems.  
    • PANDA will always cite sources and flag un-actioned items.
    """)

# Launch the UI
demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    share=False,
    inbrowser=True   # Automatically opens browser
)
