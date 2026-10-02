import gradio as gr
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager

# If you use the native LlamaIndex Callback Handler for Gradio/standard outputs, 
# you can initialize a default CallbackManager or completely omit the chainlit callback line.
Settings.callback_manager = CallbackManager([])

# Now import your configured LlamaIndex query engine
from app.services.rag.engine import query_engine

def predict(message: str, history: list):
    """
    Handles user messages, queries the LlamaIndex engine, 
    and yields tokens in real-time to the Gradio chat window.
    """
    # 1. Initialize an empty string to accumulate our response text
    partial_message = ""
    
    try:
        # 2. Call your LlamaIndex engine.
        # Gradio handles async background tasks automatically, but since query() 
        # outputs a generator, we process it synchronously chunk by chunk.
        res = query_engine.query(message)
        
        # 3. Stream the response tokens in real-time using 'yield'
        for token in res.response_gen:
            partial_message += token
            yield partial_message
            
    except Exception as exc:
        # Surface DB or LLM errors in the chat instead of crashing the server
        yield f"Error: {exc}"

# 4. Create the native Gradio Chat Interface
demo = gr.ChatInterface(
    fn=predict,
    title="💬 RAG AI Assistant",
    description="Ask questions about your documents. Connected to your Supabase Vector DB.",
    theme="soft",
    # Add a custom welcome message to mimic your original cl.on_chat_start
    chatbot=gr.Chatbot(value=[[None, "Hello! I'm an AI assistant. How may I help you?"]])
)

if __name__ == "__main__":
    # Launching with share=False is perfect for Hugging Face Spaces embedding
    demo.launch()
