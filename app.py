import gradio as gr
import os
import warnings
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from system_prompt import SYSTEM_PROMPT

warnings.filterwarnings("ignore", category=UserWarning)

print("=== PANDA STARTUP STARTED ===")

DATA_DIR = "./my_knowledge_base"

def get_file_list():
    files = []
    for root, dirs, filenames in os.walk(DATA_DIR):
        for f in filenames:
            full_path = os.path.join(root, f)
            files.append(full_path)
    return files

file_list = get_file_list()
print(f"Found {len(file_list)} files in knowledge base.")

llm = ChatOllama(model="qwen3:8b", temperature=0.1, num_gpu=999, num_ctx=8192)
print("LLM ready.")

print("Starting polished PANDA interface...")

bhp_theme = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="slate",
    neutral_hue="slate"
).set(
    body_background_fill="#f8f9fa",
    block_background_fill="#ffffff",
    block_label_background_fill="#464343",   # White background for readable labels
    button_primary_background_fill="#f97316",
    button_primary_text_color="#ffffff",
    input_background_fill="#e5e7eb",         # Grey message box
    input_border_color="#d1d5db"
)

with gr.Blocks(title="PANDA - Plant Assets Networks Data and Analysis Agent", theme=bhp_theme) as demo:
    with gr.Row(equal_height=True):
        gr.Image(value="panda_icon.png", width=90, height=90, show_label=False, container=False)
        gr.Markdown("# PANDA - Plant Assets Networks Data and Analysis Agent")

    chatbot = gr.Chatbot(height=650, label="Chat with PANDA")

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask anything about the Nyrstar blower overhaul... (press Enter)",
            label="Your message",
            lines=2,
            scale=8
        )
        submit_btn = gr.Button("Send", variant="primary", scale=2)

    def respond(message, chat_history):
        if not message or not message.strip():
            return chat_history

        try:
            file_info = "\n".join([f"- {os.path.basename(f)}" for f in file_list])
            full_input = f"""User Query: {message}

Available files:
{file_info}

Use the actual file names and any context you have. Be blunt, action-oriented, list real file names, flag what needs to be actioned, and follow the full SYSTEM_PROMPT rules strictly. Do not be overly cautious."""

            response = llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=full_input)
            ])
            bot_reply = response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            bot_reply = f"Error: {e}"

        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_reply})
        return chat_history

    msg.submit(respond, [msg, chatbot], chatbot)
    submit_btn.click(respond, [msg, chatbot], chatbot)

    gr.Markdown("**PANDA UI with File Reading active.** Restart after adding new files to my_knowledge_base.")

print("Launching polished PANDA interface...")
demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    inbrowser=True,
    show_error=True
)
