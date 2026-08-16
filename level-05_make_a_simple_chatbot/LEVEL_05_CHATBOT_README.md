# 💬 Level 05: Let's Make a Chatbot

> [Level 04](../level-04_making_conversation_stateful/LEVEL-04-README.md) gave the conversation memory — a growing `messages` list plus two helper functions that made multi-turn chat feel automatic. But the two questions were still hardcoded into the script. This level removes that last piece of scaffolding: you type your own questions, as many as you like, and Claude replies for real — a proper chatbot.

This level uses one script:

| Script | What it shows |
|---|---|
| [`scripts/level-05_chatbot.py`](scripts/level-05_chatbot.py) | The Level 04 stateful-conversation pattern wrapped in an interactive `while True` loop driven by `input()` |

---

## 🎯 The idea in one sentence

> Everything from Level 04 stays exactly the same — same `messages` list, same helper functions, same `chat()` call. The only change: instead of two hardcoded `user_prompt` strings, the prompt now comes from `input("You: ")` inside a loop that keeps running until you type `X`.

---

## 1️⃣ What actually changed from Level 04

Nothing about *how* the conversation works changed. What changed is *where the prompt comes from* and *how many turns you get*.

### Before (Level 04) — two hardcoded turns

```python
user_prompt = "What is the capital of France?"
add_user_message(messages, user_prompt)
response_text = chat(messages)
add_claude_assistant_message(messages, response_text)

user_prompt = "Can you tell me something more?"
add_user_message(messages, user_prompt)
response_text = chat(messages)
```

### After (Level 05) — an unlimited, interactive loop

```python
while True:
    user_prompt = input("You: ")

    if user_prompt.strip().upper() == "X":
        print("Chat ended. Goodbye!")
        break

    add_user_message(messages, user_prompt)
    response_text = chat(messages)
    print("Claude:", response_text)
    add_claude_assistant_message(messages, response_text)
```

The body of the loop is doing precisely what Level 04 did twice by hand — `add_user_message` → `chat()` → `add_claude_assistant_message` — just wrapped so it repeats for however many turns you want, instead of being copy-pasted a fixed number of times.

### The exit condition

```python
if user_prompt.strip().upper() == "X":
    print("Chat ended. Goodbye!")
    break
```

- `.strip()` trims accidental leading/trailing spaces so `" x "` still counts as exiting.
- `.upper()` makes the check case-insensitive, so both `x` and `X` work.
- `break` exits the `while True` loop cleanly — the script then falls through to the final `print` statement after the loop and ends normally.

Everything else — the API client setup, the `model`, the helper functions, and `messages = []` sitting outside the loop — is unchanged from Level 04. `messages` is still declared **once, before** the loop, so it keeps accumulating across every turn instead of resetting each time around.

---

## 🖥️ What actually happens when you run it

```
You: What is the capital of France?
Claude: The capital of France is Paris.
You: Can you tell me something more?
Claude: Of course! Here are some interesting facts about Paris:

- **Location**: Paris is situated in north-central France along the Seine River.
- **Population**: It's the most populous city in France, with around 2 million people...
- **History**: Paris has a rich history dating back over 2,000 years...
You: X
Chat ended. Goodbye!
```

> ℹ️ Your own output's wording will differ — Claude doesn't produce identical text on every run. That's expected. You can also keep going for as many turns as you like before typing `X`; the transcript above just stops after two questions for illustration.

---

## ⚠️ Things worth noticing (and mistakes to avoid)

| Watch out for... | Why it matters |
|---|---|
| `messages = []` must sit **outside** (before) the `while True` loop | If you accidentally move it inside the loop, the history resets every turn and you're back to Level 03's "amnesia" bug — Claude will forget every previous question |
| Checking the exit condition **before** calling `add_user_message` | If you added `"X"` to the message history first, it would get sent to Claude as an actual question instead of quietly ending the chat |
| The list only ever grows | Same warning as Level 04 — every turn resends the *entire* conversation so far, so a long interactive chat costs more tokens with each question. We'll tackle trimming/summarizing history in a future level |
| `max_tokens=200` | Still small on purpose, carried over from Level 04. Raise it (e.g. to `1024`) if you want fuller answers that don't cut off mid-sentence |

---

## ▶️ How to run this yourself

1. Make sure your virtual environment is active and your `.env` file has `ANTHROPIC_API_KEY` set (see [Level 01](../level-01_build_a_basic_agent/LEARN-AND-RUN.md) if you haven't set this up yet).
2. From the project root, run:
   ```powershell
   python level-05_make_a_simple_chatbot/scripts/level-05_chatbot.py
   ```
3. Type any question at the `You:` prompt and press Enter. Keep the conversation going — ask a follow-up and confirm Claude still remembers the earlier turns, exactly like in Level 04, except now *you* are choosing the questions.
4. Type `X` (or `x`) and press Enter when you're done to exit the loop cleanly.

---

## 🧪 Try this next

1. **Print token usage each turn.** `client.messages.create(...)` returns a `usage` object (see [Level 02](../level-02_anatomy_of_claude_response/API_RESPONSE_ANATOMY.md)) — log `response.usage.input_tokens` inside `chat()` and watch it climb turn after turn as the history grows.
2. **Support multiple exit words.** Extend the exit check to also accept `"quit"` or `"exit"`, not just `"X"`.
3. **Give the loop a personality.** Add a `system` prompt to `client.messages.create(...)` so Claude answers in a particular tone or role throughout the whole chat.
4. **Handle empty input.** What happens right now if you just press Enter without typing anything? Add a check that skips the API call (and re-prompts) when `user_prompt` is empty.

---

## 📚 Reference

- [Claude API Docs — Messages](https://docs.claude.com/en/api/messages)
- [Working with Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Level 01: First AI Agent Script](../level-01_build_a_basic_agent/LEARN-AND-RUN.md)
- [Level 02: Anatomy of a Claude API Response](../level-02_anatomy_of_claude_response/API_RESPONSE_ANATOMY.md)
- [Level 03: The Claude API Is Stateless (And How to Fix It)](../level-03_claude_llm_model_api_is_stateless/LEVEL-03-README.md)
- [Level 04: Making the Conversation Stateful](../level-04_making_conversation_stateful/LEVEL-04-README.md)
