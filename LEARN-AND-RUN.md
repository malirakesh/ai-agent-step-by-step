# Learn & Run: Your First AI Agent Script

This guide is written for someone who has **never built an AI agent before** and wants to
understand exactly what [scripts/agent.py](scripts/agent.py) does, line by line, and how to
run it themselves.

We'll cover two things:

1. **How the script works** — a line-by-line walkthrough.
2. **How to run it** — a step-by-step setup guide, from zero to a working response from
   Claude.

---

## 1. The big picture

At its core, an "AI agent" script does three things:

1. Send a message (a *prompt*) to an AI model.
2. Let the model think and generate a reply.
3. Receive and use that reply.

[scripts/agent.py](scripts/agent.py) is the smallest possible version of that: it sends one
question ("What is the capital of France?") to Anthropic's Claude model and prints the raw
answer. There's no loop, no memory, no tools yet — just one request and one response. This is
the foundation every more advanced agent (multi-turn chat, tool use, autonomous agents) is
built on top of.

---

## 2. Line-by-line walkthrough of `agent.py`

Here is the full file for reference:

```python
# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# load the anthropic library
from anthropic import Anthropic

client = Anthropic()
model = "claude-haiku-4-5-20251001"

message = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
)
print(message)
```

Now let's break down **every line**.

### `from dotenv import load_dotenv`

This imports a function called `load_dotenv` from the `python-dotenv` package.

- **Why it's needed:** Your Claude API key is a secret. You should never type it directly into
  your Python code (if you did, and pushed the code to GitHub, anyone could steal your key and
  run up your bill). Instead, secrets are kept in a separate file called `.env` that sits in
  your project folder and is *never* committed to version control.
- `load_dotenv` is the function that knows how to read that `.env` file.

### `load_dotenv()`

This actually **calls** the function you just imported.

- It looks for a file named `.env` in your project (or a parent folder) and reads every line
  formatted like `KEY=VALUE`.
- For every line it finds, it sets that value as an **environment variable** — basically a
  piece of data that's available to your running program, similar to how your operating system
  has variables like `PATH`.
- In this project, `.env` contains a single line: `ANTHROPIC_API_KEY=<your secret key>`. After
  this line runs, that key is now accessible to any code in the program, including libraries
  you didn't write yourself.

### `from anthropic import Anthropic`

This imports the `Anthropic` class from the `anthropic` Python package (the official SDK
Anthropic publishes for talking to Claude models over their API).

- Think of this class as a "phone" you'll use to call Claude. You need to construct one before
  you can make any requests.

### `client = Anthropic()`

This creates an instance of that `Anthropic` "phone" and stores it in a variable called
`client`.

- Notice you didn't type your API key anywhere here. That's intentional: the `Anthropic()`
  constructor automatically looks for an environment variable named `ANTHROPIC_API_KEY` (the
  same one `load_dotenv()` loaded a moment ago) and uses it to authenticate every request this
  client makes.
- This is exactly why `load_dotenv()` had to run **before** this line — order matters here. If
  you swapped these two lines, the client wouldn't find the key yet.
- `client` is the object you'll use for every future request to Claude in this program.

### `model = "claude-haiku-4-5-20251001"`

This is just a plain Python string stored in a variable, naming **which** Claude model you want
to talk to.

- Anthropic offers several models (e.g., faster/cheaper "Haiku" models vs. more capable
  "Sonnet"/"Opus" models). Each has a specific ID string like the one above.
- Storing it in a variable (instead of typing the string every time) means if you want to
  switch models later, you only change it in one place.

### `message = client.messages.create(...)`

This is the actual network request — the moment your program talks to Claude over the internet.

- `client.messages.create(...)` sends an HTTP request to Anthropic's servers with everything
  inside the parentheses, waits for Claude to generate a response, and returns that response as
  a Python object.
- That returned object is stored in the variable `message`.

Let's look at each argument passed into `create(...)`:

#### `model=model,`

Tells the API which model (from the variable defined above) should generate the response.
Different models have different capabilities, speeds, and costs.

#### `max_tokens=1024,`

A "token" is roughly a chunk of a word (for English text, ~4 characters or about ¾ of a word).
This parameter caps **how long the model's reply is allowed to be** — at most 1024 tokens here.

- This is a safety/cost control. Without a limit, a model could theoretically generate an
  extremely long response. Setting `max_tokens` ensures the response — and what you're billed
  for generating — stays bounded.
- If the model's answer would naturally be longer than this limit, the response gets cut off.

#### `messages=[ { "role": "user", "content": "What is the capital of France?" } ]`

This is the actual conversation you're sending to the model.

- The Claude API expects a **list of messages**, because conversations can have multiple turns
  (you ask something, Claude replies, you ask a follow-up, and so on). Here, the list only has
  one message, because this is a single-turn question.
- Each message is a Python dictionary with two keys:
  - `"role"`: who is "speaking" this message. It's `"user"` here because this message
    represents something *you* (the human/application) are sending. The model's replies come
    back with role `"assistant"`. (A conversation history you send back on a follow-up request
    would include both `"user"` and `"assistant"` entries, alternating.)
  - `"content"`: the actual text of the message — in this case, the question
    `"What is the capital of France?"`.

### `print(message)`

Finally, this prints the entire `message` object that came back from Claude to your terminal.

- This isn't just the answer text — it's the **raw response object** the SDK returns, which
  includes metadata like:
  - `id`: a unique identifier for this API call.
  - `role`: will be `"assistant"` (the model's role).
  - `content`: a list containing the actual reply text (e.g., "The capital of France is
    Paris.").
  - `model`: confirms which model actually handled the request.
  - `stop_reason`: why the model stopped generating (e.g., it finished naturally, or hit
    `max_tokens`).
  - `usage`: how many tokens were used for your input and for the output — useful for
    understanding cost.
- Printing the *raw* object (instead of just the text) is intentional here — it's meant as a
  learning exercise so you can see the full shape of what the API gives you, before you learn
  to parse out just the parts you need (like `message.content[0].text`).

---

## 3. Step-by-step: setting up and running the script

### Prerequisites

- **Python 3.9+** installed on your machine. Check with:
  ```
  python --version
  ```
- **An Anthropic API key.** Get one from the [Anthropic Console](https://console.anthropic.com/)
  under "API Keys" (requires an Anthropic account and billing set up). Keep this key private —
  never share it or commit it to a public repository.

### Step 1 — Get the project and open a terminal

Open a terminal in the project folder:
`<YOUR_DIRECTORY_LOCATION>\ai-agent-step-by-step`

### Step 2 — Create and activate a virtual environment

A virtual environment keeps this project's Python packages separate from other projects on
your machine, so they don't conflict.

```powershell
python -m venv .venv
.venv\Scripts\activate
```

After activation, your terminal prompt should show `(.venv)` at the start of the line. This
project already has a `.venv` folder set up, but this is the command that created it — useful
if you ever need to recreate it elsewhere.

### Step 3 — Install the required packages

This script depends on two packages: `anthropic` (the SDK that talks to Claude) and
`python-dotenv` (which loads your `.env` file). Install them with:

```powershell
pip install anthropic python-dotenv
```

### Step 4 — Create your `.env` file

In the project root (same folder as `README.md`), create a file named exactly `.env` containing
one line:

```
ANTHROPIC_API_KEY=your-actual-api-key-here
```

Replace `your-actual-api-key-here` with the key you generated in the Anthropic Console. Do not
add quotes around the value, and don't commit this file to git (check `.gitignore` — it should
already be excluded).

### Step 5 — Run the script

From the project root, run:

```powershell
python scripts/agent.py
```

### Step 6 — Read the output

You should see a printed Python object in your terminal that looks roughly like:

```
Message(id='msg_...', content=[TextBlock(text='The capital of France is Paris.', type='text')], model='claude-haiku-4-5-20251001', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(input_tokens=..., output_tokens=...))
```

If instead you see an error, check the troubleshooting section below.

---

## 4. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `AuthenticationError` or `401` | API key missing, wrong, or `.env` not found | Confirm `.env` exists in the project root and contains a valid `ANTHROPIC_API_KEY=...` line with no typos or quotes |
| `ModuleNotFoundError: No module named 'anthropic'` (or `'dotenv'`) | Packages not installed, or venv not activated | Re-run Step 2 (activate venv) then Step 3 (install packages) |
| `RateLimitError` or `overloaded_error` | Too many requests, or Anthropic's servers are busy | Wait a moment and try again |
| Script runs but nothing happens for a while, then errors with a timeout | Network/firewall/VPN issue | Check your internet connection; try disabling VPN temporarily |

---

## 5. Ideas to learn more (try these next)

Once the script runs successfully, try modifying it yourself to deepen your understanding:

1. **Print just the answer text**, not the whole object:
   ```python
   print(message.content[0].text)
   ```
2. **Change the question.** Edit the `"content"` string and re-run.
3. **Add a system prompt** to steer the model's behavior/persona:
   ```python
   message = client.messages.create(
       model=model,
       max_tokens=1024,
       system="You are a helpful assistant who always answers in one short sentence.",
       messages=[{"role": "user", "content": "What is the capital of France?"}]
   )
   ```
4. **Make it a multi-turn conversation** by appending the assistant's reply and a new user
   message to the `messages` list, then sending the whole list again.
5. **Turn it into a loop** using `input()` so you can type questions interactively instead of
   hardcoding one.
6. **Inspect `message.usage`** to see how many tokens your input and output cost — this is the
   first step toward understanding API pricing.

Each of these steps builds naturally toward the next stage of "agent" behavior: conversation
memory, tool use, and eventually autonomous multi-step agents.
