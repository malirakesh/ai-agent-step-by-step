
# Author: Rakesh Kumar Mali

# This level builds on level-04_making_conversation_stateful, which showed how to keep a
# conversation stateful by resending the full message history with every request.

# Here, we turn that into an actual chatbot: instead of hardcoding two prompts, we take
# user input from the terminal in an infinite loop, and keep chatting until the user
# types 'X' to exit.

# Step 1: Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Step 2: Load the anthropic library
from anthropic import Anthropic

# Step 3: Create an instance of the Anthropic client
client = Anthropic()

# Step 4: Define the model to use
model = "claude-haiku-4-5-20251001"

# Step 5: Define additional methods to work as helper in keeping the message history and sending
# the prompt to the model.

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_claude_assistant_message(messages, text):
    claude_assistant_message = {"role": "assistant", "content": text}
    messages.append(claude_assistant_message)

def chat(messages):
    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=messages,
    )
    return response.content[0].text

messages = []  # This list will hold the conversation history

# Step 6: Start an infinite loop so the user can ask any number of questions.
# The loop keeps running until the user types 'X' (case-insensitive) to exit.

while True:

    # Step 7: Take the next prompt from the user instead of hardcoding it.
    user_prompt = input("You: ")

    # Step 8: Check if the user wants to exit the chat.
    if user_prompt.strip().upper() == "X":
        print("Chat ended. Goodbye!")
        break

    # Step 9: Add the user's prompt to the conversation history.
    add_user_message(messages, user_prompt)

    # Step 10: Send the full conversation history to the model and get the response.
    response_text = chat(messages)

    # Step 11: Print the response received from the Claude model.
    print("Claude:", response_text)

    # Step 12: Add the response from the model to the conversation history, so it is
    # available as context for the next prompt.
    add_claude_assistant_message(messages, response_text)

# NOTE: Because the full message history is resent on every call, the model remains
# stateful across as many turns as the user wants, until they type 'X' to exit.
