
# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# load the anthropic library
from anthropic import Anthropic

client = Anthropic()
model = "claude-haiku-4-5-20251001"

# create a prompt for the model. 
# Make a request to the model with the prompt and print the RAW response received from the Claude model.
# This gives you the opportunity to see the raw response and understand how to parse it for your needs and play around it.
message = client.messages.create(
    model=model,                    # this parameter is used to declare which model to use for the request.
    max_tokens=1024,                # this parameter is used to tell the claude model the maximum number of tokens to generate in the response.
    messages=[                      # this parameter is used to provide the messages to the claude model. The messages are provided in a list of dictionaries, where each dictionary represents a message. Each message has a role and content. The role can be either "user" or "assistant", and the content is YOUR prompt/query to the model.
        {
            "role": "user", 
            "content": "What is the capital of France?"
        }
    ]
)
print(message)                      # this simply prints the raw response received from the Claude model. You can parse this response to extract the information you need.