import gradio as gr
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000/process-voice-command/"

# Gradio Interface Function
def assistant(input_text):
    response = requests.post(API_URL, json={"text": input_text})
    return response.json()

# Gradio Interface
interface = gr.Interface(
    fn=assistant,
    inputs=["text"],
    outputs=["json"],
    title="ERP Voice/Text Assistant",
    description="Process voice or text commands to interact with the ERP system."
)

if __name__ == "__main__":
    interface.launch()
