# 🧵 Level 04: Making the Conversation Stateful

> In [Level 03](../level-03_claude_llm_model_api_is_stateless/LEVEL-03-README.md) we learned Claude has no memory of its own — *you* have to handle the whole conversation, every single time. That level did it by hand, one variable per message. This level turns that trick into something reusable: a `messages` list and two small helper functions that make multi-turn chat feel automatic.

This level uses one script:

| Script | What it shows |
|---|---|
| [`scripts/level-04-agent.py`](scripts/level-04-agent.py) | A clean, reusable pattern for keeping conversation history and replaying it on every call |

---

## 🎯 The idea in one sentence

> Keep a single growing list called `messages`. Every time you or Claude says something, append it to the list. Every time you want a reply, send the **whole list** — not just the latest line.

That's it. That's the entire "memory" system. No database, no session ID, no magic — just a Python list that keeps getting longer.

---

## 1️⃣ The building blocks — walking through `level-04-agent.py`

### Two tiny helper functions

```python
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_claude_assistant_message(messages, text):
    claude_assistant_message = {"role": "assistant", "content": text}
    messages.append(claude_assistant_message)
```

These don't do anything you couldn't write inline (in fact, Level 03 did write it inline) — they just save you from repeating `{"role": "user", "content": ...}` by hand every time. Give them a `messages` list and some text, and they tack the right dictionary onto the end of it, with the correct `"role"`.

> 💡 Notice the roles again: `"user"` is you, `"assistant"` is Claude. Get these backwards and Claude will get confused about who said what — see the Level 03 mistakes table if you want a refresher.

### One tiny helper function to talk to Claude

```python
def chat(messages):
    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=messages,
    )
    return response.content[0].text
```

This wraps the API call itself. You hand it the *entire* `messages` list so far, it sends that whole thing to Claude, and it hands back just the plain text of the reply — no digging through `response.content[0].text` yourself every time.

### The conversation loop, one turn at a time

```python
messages = []  # This list will hold the conversation history

user_prompt = "What is the capital of France?"
add_user_message(messages, user_prompt)

response_text = chat(messages)
add_claude_assistant_message(messages, response_text)

user_prompt = "Can you tell me something more?"
add_user_message(messages, user_prompt)

response_text = chat(messages)
```

Follow `messages` through these lines like a flip-book:

| Step | `messages` list contains |
|---|---|
| Start | `[]` |
| After `add_user_message` (1st question) | `[user: "What is the capital of France?"]` |
| After `chat()` + `add_claude_assistant_message` | `[user: "...capital...", assistant: "Paris."]` |
| After `add_user_message` (2nd question) | `[user: "...capital...", assistant: "Paris.", user: "Can you tell me something more?"]` |

By the time the second `chat(messages)` call fires, Claude isn't just seeing *"Can you tell me something more?"* in isolation — it's seeing the **entire transcript**, including its own first answer. That's why it knows "more" means "more about Paris."

This is exactly the manual fix from Level 03 (`agent_03_revised.py`), just generalized: instead of hardcoding `message1`, `message2`, and building lists by hand each time, one list keeps growing and two helper functions keep it tidy.

---

## 🖥️ What actually happens when you run it

```
User Prompt 1 : What is the capital of France?
Response 1 Text : The capital of France is Paris.
User Prompt 2 : Can you tell me something more?
Response 2 Text : Of course! Here are some interesting facts about Paris:

- **Location**: Paris is situated in north-central France along the Seine River.
- **Population**: It's the most populous city in France, with around 2 million people...
- **History**: Paris has a rich history dating back over 2,000 years...
- **Famous landmarks**: The city is home to iconic structures like the Eiffel Tower...
```

Same shape of result as Level 03's fix, but notice the second answer trails off mid-sentence this time. That's `max_tokens=200` cutting the reply short — a nice reminder that `max_tokens` is a hard limit, not a suggestion, on the response length, not on how much the model "knows."

> ℹ️ Your own output's wording will differ — Claude doesn't produce identical text on every run. That's expected.

---

## ⚠️ Things worth noticing (and mistakes to avoid)

| Watch out for... | Why it matters |
|---|---|
| Forgetting to call `add_claude_assistant_message` after `chat()` | If you skip this, the next turn won't include Claude's previous reply, and you've silently recreated the Level 03 "amnesia" bug |
| Calling `add_user_message` *after* `chat()` instead of before | The order matters — you must add the new question to `messages` **before** calling `chat(messages)`, otherwise Claude never sees it |
| `max_tokens=200` | Small on purpose here so you can see truncation happen. Raise it (e.g. to `1024`) if you want fuller answers |
| The list only ever grows | Every turn resends *all* previous turns, so a long chat costs more tokens each time. Same warning as Level 03 — we'll tackle trimming/summarizing history in a future level |

---

## ▶️ How to run this yourself

1. Make sure your virtual environment is active and your `.env` file has `ANTHROPIC_API_KEY` set (see [Level 01](../level-01_build_a_basic_agent/LEARN-AND-RUN.md) if you haven't set this up yet).
2. From the project root, run:
   ```powershell
   python level-04_making_conversation_stateful/scripts/level-04-agent.py
   ```
3. Read the two prompts and two responses printed to your terminal. Confirm the second answer clearly "knows" the first question was about Paris — that's the whole lesson, working in front of you.

---

## 🧪 Try this next

1. **Add a third turn.** Add another `add_user_message` / `chat` / `add_claude_assistant_message` block with a follow-up question like *"Which of those is the most visited?"* — the pattern already supports it, you're just calling it one more time.
2. **Turn it into a real chat loop.** Replace the two hardcoded `user_prompt` blocks with a `while True:` loop that calls `input("You: ")`, so you can type questions interactively instead of hardcoding them.
3. **Print token usage each turn.** `client.messages.create(...)` returns a `usage` object (see [Level 02](../level-02_anatomy_of_claude_response/API_RESPONSE_ANATOMY.md)) — log `response.usage.input_tokens` inside `chat()` and watch it climb turn after turn as the history grows.
4. **Raise `max_tokens`** and see the second response finish its thought instead of cutting off mid-sentence.

---

## 📚 Reference

- [Claude API Docs — Messages](https://docs.claude.com/en/api/messages)
- [Working with Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Level 01: First AI Agent Script](../level-01_build_a_basic_agent/LEARN-AND-RUN.md)
- [Level 02: Anatomy of a Claude API Response](../level-02_anatomy_of_claude_response/API_RESPONSE_ANATOMY.md)
- [Level 03: The Claude API Is Stateless (And How to Fix It)](../level-03_claude_llm_model_api_is_stateless/LEVEL-03-README.md)
