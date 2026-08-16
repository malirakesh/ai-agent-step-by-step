# ai-agent-step-by-step

# 🪜 Learn & Run: Building an AI Agent, One Level at a Time

This repo is written for someone who has **never built an AI agent before**. Instead of
dropping you into a complex framework, it grows a single idea — "send text to Claude, get
text back" — one small, deliberate step at a time, until it turns into a real multi-turn
conversational agent.

Every level lives in its own folder with its own script and its own README. Read them in
order — each one only makes sense because of what the previous one taught you.

---

![image alt](
https://github.com/malirakesh/ai-agent-step-by-step/blob/15a1751381127d6d6148d57d6a6d1b13dfae9338/assets/anatomy-of-a-single-prompt.png)

[Read my articles on Medium](https://medium.com/@rakesh.mali/zero-to-claude-what-fifteen-lines-taught-me-about-ai-agents-ba33c21fb295)

---

## 🗺️ What you'll learn, level by level

| Level | Title | What you'll learn |
|---|---|---|
| [01](level-01_build_a_basic_agent/LEARN-AND-RUN.md) | Build a Basic Agent | Send your very first prompt to Claude and print the raw response. Sets up your `.env`, API key, and the three-step mental model every agent is built on: *send → think → receive*. |
| [02](level-02_anatomy_of_claude_response/API_RESPONSE_ANATOMY.md) | Anatomy of a Claude Response | Stop treating the response as a black box. Learn every field on the `Message` object — `content`, `stop_reason`, `usage`, token counts — so you know exactly what you're working with. |
| [03](level-03_claude_llm_model_api_is_stateless/LEVEL-03-README.md) | The Claude API Is Stateless | Discover the single most surprising thing about LLM APIs: Claude forgets everything between calls. See the "amnesia" bug happen live, then fix it by manually resending the conversation so far. |
| [04](level-04_making_conversation_stateful/LEVEL-04-README.md) | Making the Conversation Stateful | Turn the Level 03 fix into a reusable pattern — a growing `messages` list plus small helper functions (`add_user_message`, `add_claude_assistant_message`, `chat`) that make multi-turn chat feel automatic. |
| [05](level-05_make_a_simple_chatbot/LEVEL_05_CHATBOT_README.md) | Let's Make a Chatbot | Turn the Level 04 pattern into a real, interactive chatbot — swap the hardcoded prompts for `input()` inside a loop that keeps chatting until you type `X` to exit. |

Each level's README includes a full code walkthrough, sample output, common mistakes to
avoid, and hands-on exercises ("try this next") to deepen your understanding before moving
on.

---

## 1. The big picture

At its core, an "AI agent" script does three things:

1. Send a message (a *prompt*) to an AI model.
2. Let the model think and generate a reply.
3. Receive and use that reply.

Every level in this repo starts from that three-step loop and adds exactly one new idea on
top of it — reading the raw response, handling the API's statelessness, then making a real
conversation out of it. No level jumps ahead of what the previous one taught.

---

## 2. Prerequisites & one-time setup

These steps only need to be done once — every level after this reuses the same environment.

- **Python 3.9+** installed on your machine. Check with:
  ```
  python --version
  ```
- **An Anthropic API key.** Get one from the [Anthropic Console](https://console.anthropic.com/)
  under "API Keys" (requires an Anthropic account and billing set up). Keep this key private —
  never share it or commit it to a public repository.

### Step 1 — Open a terminal in the project folder

```
<YOUR_DIRECTORY_LOCATION>\ai-agent-step-by-step
```

### Step 2 — Create and activate a virtual environment

A virtual environment keeps this project's Python packages separate from other projects on
your machine, so they don't conflict.

```powershell
python -m venv .venv
.venv\Scripts\activate
```

After activation, your terminal prompt should show `(.venv)` at the start of the line.

### Step 3 — Install the required packages

Every level depends on the same two packages: `anthropic` (the SDK that talks to Claude) and
`python-dotenv` (which loads your `.env` file). Install them with:

```powershell
pip install anthropic python-dotenv
```

### Step 4 — Create your `.env` file

In the project root (same folder as this `README.md`), create a file named exactly `.env`
containing one line:

```
ANTHROPIC_API_KEY=your-actual-api-key-here
```

Replace `your-actual-api-key-here` with the key you generated in the Anthropic Console. Do not
add quotes around the value, and don't commit this file to git (check `.gitignore` — it should
already be excluded).

### Step 5 — Head to Level 01

With your environment set up, jump into
[Level 01: Build a Basic Agent](level-01_build_a_basic_agent/LEARN-AND-RUN.md) and work through
the levels in order using the table above.

---

## 3. Troubleshooting

These apply no matter which level's script you're running:

| Symptom | Likely cause | Fix |
|---|---|---|
| `AuthenticationError` or `401` | API key missing, wrong, or `.env` not found | Confirm `.env` exists in the project root and contains a valid `ANTHROPIC_API_KEY=...` line with no typos or quotes |
| `ModuleNotFoundError: No module named 'anthropic'` (or `'dotenv'`) | Packages not installed, or venv not activated | Re-run Step 2 (activate venv) then Step 3 (install packages) |
| `RateLimitError` or `overloaded_error` | Too many requests, or Anthropic's servers are busy | Wait a moment and try again |
| Script runs but nothing happens for a while, then errors with a timeout | Network/firewall/VPN issue | Check your internet connection; try disabling VPN temporarily |

---

## 4. Where this is headed

By the end of Level 05, you'll have a real, interactive chatbot — a script that holds a
growing conversation with Claude using nothing but a Python list, a couple of helper
functions, and a loop driven by your own typed input. That same pattern —
*keep history, replay history* — is the foundation for everything more advanced that usually
comes next: giving the agent tools it can call, letting it take multiple steps on its own, and
eventually building fully autonomous agents. Future levels will build on this repo in exactly
that direction.
