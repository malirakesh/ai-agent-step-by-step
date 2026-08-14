
# Author: Rakesh Kumar Mali

# THIS SCRIPT IS A REVISED VERSION OF THE PREVIOUS SCRIPT level-03_claude_llm_model_api_is_stateless/scripts/agent_03.py
# You need to run this script after running the previous script level-03_claude_llm_model_api_is_stateless/scripts/agent_03.py to see the difference in the responses received from the Claude model when the conversation history is preserved in the prompt.

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# load the anthropic library
from anthropic import Anthropic

client = Anthropic()
model = "claude-haiku-4-5-20251001"

# send first prompt to the model.
message1 = client.messages.create(
    model=model,                   
    max_tokens=1024,               
    messages=[                     
        {
            "role": "user", 
            "content": "What is the capital of France?"
        }
    ]
)

print("Response 1 Text:", message1.content[0].text)


message2 = client.messages.create(
    model=model,                    
    max_tokens=1024,                
    messages=[                      
        {
            "role": "assistant", 
            "content": message1.content[0].text
        },
        {
            "role": "user", 
            "content": "Can you tell me something more?"
        }
    ]
)
print("Response 2 Text:", message2.content[0].text)


"""
I received the following responses from the Claude model for the two prompts I sent.
This clearly shows that the Claude model needs the conversation history to be preserved in the prompt to provide a more relevant response. 
Each prompt is treated independently, and the model does not retain any information from previous interactions unless it is provided in the 
prompt.
NOTE: You may get different responses from the Claude model for the same prompts.

Response 1 Text: The capital of France is Paris.

Response 2 Text: # More About Paris

Here are some interesting facts about Paris:

- **Population**: Paris is home to about 2.2 million people, making it one of Europe's largest cities

- **The Eiffel Tower**: Built in 1889, it's the iconic symbol of Paris and one of the most visited monuments in the world

- **River Seine**: The city is beautifully situated along this famous river, with many picturesque bridges

- **Art & Culture**: Paris is renowned for its world-class museums like the Louvre, which houses the Mona Lisa

- **Architecture**: Known for its elegant Haussmann-style buildings and Gothic cathedrals like Notre-Dame

- **History**: Has been a major center of art, fashion, gastronomy, and philosophy for centuries

- **Nickname**: Often called "The City of Light" (La Ville Lumière)

- **UNESCO World Heritage**: Much of Paris's historic center is recognized as a UNESCO World Heritage site

Is there any particular aspect of Paris you'd like to know more about?
"""