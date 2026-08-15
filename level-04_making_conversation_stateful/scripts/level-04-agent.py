
# Author: Rakesh Kumar Mali

# This level is to enhance the previous level-03_claude_llm_model_api_is_stateless to make 
# the conversation stateful by preserving the conversation history in the prompt.

# The simple trick is to add the previous response from the model in the next prompt to the model. 
# This way, the model will have the context of the previous conversation and can provide a more 
# relevant response.
# And the same process continues for the next prompts to the model. 
# This way, the conversation history is preserved in the prompt and the model can provide a more 
# relevant response.

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

# Step 6: Start the conversation with the first prompt to the model.
user_prompt = "What is the capital of France?"
print("User Prompt 1 :", user_prompt)
add_user_message(messages, user_prompt)

# Step 7: Send the prompt to the model and get the response.
response_text = chat(messages)

# Step 8: Print the response received from the Claude model.
print("Response 1 Text :", response_text)

# Step 9: Add the response from the model to the conversation history.
add_claude_assistant_message(messages, response_text)

# Step 10: Continue the conversation with the second prompt to the model.
user_prompt = "Can you tell me something more?"
print("User Prompt 2 :", user_prompt)
add_user_message(messages, user_prompt)

# Step 11: Send the prompt to the model and get the response.
response_text = chat(messages)

# Step 12: Print the response received from the Claude model.
print("Response 2 Text :", response_text)

# In my run, I received the following responses from the Claude model for the two prompts I sent.
# This clearly shows that the Claude model is now stateful, meaning it remembers the previous conversation
# NOTE: You may get different responses from the Claude model for the same prompts as the model generates the response. For any two runs, we can't expect the same response.

"""

User Prompt 1 : What is the capital of France?
Response 1 Text : The capital of France is Paris.
User Prompt 2 : Can you tell me something more?
Response 2 Text : Of course! Here are some interesting facts about Paris:

- **Location**: Paris is situated in north-central France along the Seine River.

- **Population**: It's the most populous city in France, with around 2 million people in the city proper and over 12 million in the metropolitan area.

- **History**: Paris has a rich history dating back over 2,000 years and has been a major center of art, fashion, gastronomy, and culture for centuries.

- **Famous landmarks**: The city is home to iconic structures like the Eiffel Tower, Notre-Dame Cathedral, the Louvre Museum, and the Arc de Triomphe.

- **UNESCO World Heritage**: Paris's historic center is recognized as a UNESCO World Heritage Site.

- **Economy**: It's an important global center for art, fashion, gastronomy, education, and business.

- **Nickname**: Paris is often called

"""