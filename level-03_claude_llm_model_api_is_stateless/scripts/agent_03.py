
# Author: Rakesh Kumar Mali

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
# print the text of the first response received from the Claude model.
print("Response 1 Text:", message1.content[0].text)


# send second prompt to the model.
message2 = client.messages.create(
    model=model,                    
    max_tokens=1024,                
    messages=[                      
        {
            "role": "user", 
            "content": "Can you tell me something more?"
        }
    ]
)
# print the text of the second response received from the Claude model.
print("Response 2 Text:", message2.content[0].text)


"""
I received the following responses from the Claude model for the two prompts I sent.
This clearly shows that the Claude model is stateless, meaning it does not remember the previous conversation 
or context. Each prompt is treated independently, and the model does not retain any information from previous 
interactions.


Response 1 Text: The capital of France is Paris.

Response 2 Text: I'd be happy to help! But I'm not sure what you're referring to since this is the start of our conversation. Could you let me know:

- What topic would you like to learn more about?
- Or are you continuing from a previous conversation?

Feel free to ask about anything—I'm here to help!
"""

# NOW , let's enhance this and rewrite the prompt to preserve the conversation history 
# Refer to the next script level-03_claude_llm_model_api_is_stateless/scripts/agent_03_revised.py for the enhanced version of this script that preserves the conversation history in the prompt.
