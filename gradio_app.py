import gradio as gr
import requests
import base64
import os


def trim_history(history):
    return history[-10:] if len(history) > 10 else history


# ------------------------------
# SPEECH-TO-TEXT ENDPOINT
# ------------------------------
def transcribe_audio(audio_path):
    if audio_path is None:
        return None

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    b64_audio = base64.b64encode(audio_bytes).decode()

    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/speech-to-text",
            json={"audio_base64": b64_audio},
            timeout=15  # prevent long hanging requests
        )
        return response.json().get("text", "")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {e}"



# ------------------------------
# CHAT FUNCTION
# ------------------------------
def chat_function(input_message, history):

    # 🔥 FIX 1 — If textbox is empty, do NOT send request
    if not input_message or input_message.strip() == "":
        return history, history

    if history is None:
        history = []

    # Add user's message
    history.append({"role": "user", "content": input_message})
    history = trim_history(history)

    try:
        # Send chat history to backend
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/chat",
            json={"history": history},
            timeout=20     # 🔥 FIX 2 — prevent infinite hang
        )

        bot_reply = response.json().get("response", "No response received.")

    except Exception as e:
        bot_reply = f"Backend error: {str(e)}"

    # Add bot reply
    history.append({"role": "assistant", "content": bot_reply})
    history = trim_history(history)

    return history, history




# ------------------------------
# NEW FUNCTION:
# VOICE → TEXT → TEXTBOX
# ------------------------------
def convert_voice_to_text(audio_file):
    text = transcribe_audio(audio_file)
    if not text or text == "Could not understand audio.":
        return ""  # avoid sending empty or error text
    return text.strip()




custom_css = """
#chatbot {
    height: 520px !important;
}
"""

with gr.Blocks(css=custom_css) as demo:

    gr.Markdown("<h2 style='text-align:center;'>🌾 AgriBot – Your Crop Assistant</h2>")

    chatbot = gr.Chatbot(label="AgriBot Chat", type="messages", elem_id="chatbot")
    state = gr.State([])

    with gr.Row():
        text_box = gr.Textbox(
            placeholder="Ask about crops, diseases, fertilizers...",
            scale=8
        )
        voice = gr.Audio(
            sources=["microphone"],
            type="filepath",
            scale=1
        )

    # TEXT SUBMIT
    text_box.submit(chat_function, inputs=[text_box, state], outputs=[chatbot, state])

    # VOICE → TEXTBOX
    voice.change(
        convert_voice_to_text, 
        inputs=voice, 
        outputs=text_box
    )

demo.launch()
