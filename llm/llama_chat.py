import os
import subprocess
import sys
from pathlib import Path
from assistant_utils import create_dcc_assistant

# Function to set up the LLaMA environment and download the model if it doesn't exist
def setup_llma(base_dir):
    # Resolve the base directory path and create it if it doesn't exist
    base_dir = Path(base_dir).resolve()
    base_dir.mkdir(exist_ok=True, parents=True)
    os.chdir(base_dir)

    print(f"Setting up LLaMA in: {base_dir}")

    # Install llama-cpp-python package using pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "llama-cpp-python"])

    # Define model download URL and expected local file name
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    model_path = base_dir / "llama-2-7b-chat.gguf"

    # Download the model file if it doesn't already exist
    if not model_path.exists():
        print(f"Downloading model file to {model_path}")
        subprocess.check_call(["curl", "-L", "-o", str(model_path), model_url])
    else:
        print("Model file already exists")

    return model_path

# Function to start an interactive chat loop with the model
def chat_with_llama(model_path):
    from llama_cpp import Llama

    # Initialize the LLaMA model with parameters
    llm = Llama(
        model_path=str(model_path),   # Path to the model file
        n_ctx=2048,                   # Number of tokens LLaMA considers in a context window
        n_threads=8,                  # Number of CPU threads to use
        chat_format="llama-2"         # Format that mimics chat-based interactions
    )

    print("\nLLaMA Chat Interface")
    print("Type: 'exit' to quit.\n")
    print("." * 50)

    # Initialize chat history with a system prompt
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        # Take user input
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            break

        # Add the user's message to the chat history
        messages.append({"role": "user", "content": user_input})

        # Get model response based on the chat history
        response = llm.create_chat_completion(messages)

        # Extract the assistant's reply
        assistant_message = response["choices"][0]["message"]["content"]

        # Add the assistant's reply to the chat history
        messages.append({"role": "assistant", "content": assistant_message})

        # Print the assistant's reply
        print("\nAssistant:")
        print(assistant_message.strip())
        print("-" * 50)

# Main script entry point
if __name__ == "__main__":
    try:
        # Use custom directory if provided, otherwise use current directory
        if len(sys.argv) > 1:
            custom_dir = sys.argv[1]
        else:
            custom_dir = "."

        # Setup model and begin chat
        model_path = setup_llma(custom_dir)
        create_dcc_assistant(model_path, str(sys.argv[2]))
    except Exception as e:
        print(f"An error occurred: {e}")
