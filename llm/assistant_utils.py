def create_dcc_assistant(model_path, dcc_type):
    from llama_cpp import Llama  # Import the Llama class from llama-cpp-python

    # Initialize the LLaMA model with specified settings
    llm = Llama(
        model_path = str(model_path),  # Path to the LLaMA model file
        n_ctx =4096,                   # Maximum number of context tokens the model can handle
        n_threads = 16,                # Number of CPU threads to use
        chat_format = "llama-2"        # Use LLaMA-2 chat format for structured conversation
    )

    # Define the system prompt that sets the assistant's behavior and expertise
    system_prompt = {
        "role": "system",
        "content":f""" You are a highly knowledgeable and helpful {dcc_type} assistant with expertise in:
        - {dcc_type} design and implementation.
        - {dcc_type} 3d Topology.
        - {dcc_type} testing and debugging.
        - {dcc_type} performance optimization.
        - {dcc_type} animation and rendering.
        - {dcc_type} user interface and user experience.
        - {dcc_type} shader and pipelines.
        - {dcc_type} lights and materials.

        provide detailed and accurate information about the {dcc_type} design and implementation, including:
        - What the {dcc_type} does.
        - How the {dcc_type} is implemented.
        - Why the {dcc_type} is important.
        - How the {dcc_type} can be optimized."""

    }
    # Basic CLI UI intro
    print("\nLlama Chat Interface")
    print("Type 'exit' to quit.\n")
    print("." * 50)

    messages = [system_prompt]   # Start conversation with the system prompt
    
    # Main chat loop
    while True:
        user_input = input("\nYou:").strip()    # Get user input

        if user_input.lower() == "exit":
           break                                # Exit the chat loop if user types 'exit'

        # Append user message to the conversation history
        messages.append({"role": "user", "content": user_input})

        # Get model response based on the full conversation history
        response = llm.create_chat_completion(messages)
        
        # Extract assistant's message from the response
        assistant_message = response["choices"][0]["message"]["content"]

        # Append assistant message to the conversation
        messages.append({"role": "assistant", "content": assistant_message})

        # Print assistant's reply
        print("\nAssistant:")
        print(assistant_message.strip())
        print("." * 50)

        # Limit the message history to prevent exceeding context size
        # Keeps system prompt + last 9 messages (e.g., recent turns)
        if len(messages) > 10:
            messages = [system_prompt] + messages[-9:]