# 🧠 Level 03: The Claude API Is Stateless (And How to Fix It)

> A beginner-friendly walkthrough of the single most surprising thing about talking to an LLM through an API: **it doesn't remember you** — not even from the message you sent ten seconds ago — unless you remind it yourself, every single time.

This level uses two small scripts:

| Script | What it shows |
|---|---|
| [`scripts/agent_03.py`](scripts/agent_03.py) | The **problem** — two prompts sent one after another, and Claude forgets the first one completely |
| [`scripts/agent_03_revised.py`](scripts/agent_03_revised.py) | The **fix** — manually resending the conversation so far, so Claude can "remember" |

---

## 😲 The problem: Claude has no memory of its own

Imagine calling a helpdesk, explaining your issue in detail... and then being transferred to a *brand new agent* for your very next sentence — one who has never heard of you or your issue. That's exactly what happens if you call the Claude API twice in a row without doing anything special.

This isn't a bug. It's how the API is **designed to work**:

> 🔑 **Every call to `client.messages.create()` is completely independent.** Claude doesn't have a "session" sitting on Anthropic's servers remembering your chat. It only ever sees exactly what you put inside the `messages` list you send it — nothing more, nothing less.

Let's watch this happen.

---

## 1️⃣ The problem, in code — `agent_03.py`

```python
client = Anthropic()
model = "claude-haiku-4-5-20251001"

# send first prompt to the model.
message1 = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)
print("Response 1 Text:", message1.content[0].text)


# send second prompt to the model.
message2 = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Can you tell me something more?"}
    ]
)
print("Response 2 Text:", message2.content[0].text)
```

Walking through what's new compared to [Level 01](../level-01_build_a_basic_agent/LEARN-AND-RUN.md):

- **Two separate requests.** `message1` asks *"What is the capital of France?"*. `message2` asks *"Can you tell me something more?"* — a follow-up that only makes sense if you already know we were talking about Paris.
- **Two separate `messages` lists.** Look closely: the second call's `messages` list contains *only* the new question. Nothing about France or Paris is in there. As far as the API is concerned, this is a **first message in a brand-new conversation**, not a follow-up.

### 🖥️ What actually happens when you run it

```
Response 1 Text: The capital of France is Paris.

Response 2 Text: I'd be happy to help! But I'm not sure what you're referring
to since this is the start of our conversation. Could you let me know:

- What topic would you like to learn more about?
- Or are you continuing from a previous conversation?
```

Claude answers the first question perfectly — then gets completely confused by the second one, because from its point of view, **nothing came before it.**

> ⚠️ **Common beginner mistake:** Assuming that because you're using the same `client` object for both calls, the model "remembers" the earlier one. It doesn't. The `client` is just your connection to the API — it holds no conversation state at all. *You* are responsible for that.

---

## 2️⃣ The fix, in code — `agent_03_revised.py`

The fix doesn't involve any special "memory" feature — because there isn't one to turn on. Instead, **you replay the conversation yourself**, by including the earlier turns inside the `messages` list of your next request.

```python
message1 = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)
print("Response 1 Text:", message1.content[0].text)


message2 = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[
        {"role": "assistant", "content": message1.content[0].text},
        {"role": "user", "content": "Can you tell me something more?"}
    ]
)
print("Response 2 Text:", message2.content[0].text)
```

Only one thing changed — but it changes everything. Compare the second call's `messages` list to the version in `agent_03.py`:

| Before (`agent_03.py`) | After (`agent_03_revised.py`) |
|---|---|
| `[{"role": "user", "content": "Can you tell me something more?"}]` | `[{"role": "assistant", "content": "The capital of France is Paris."}, {"role": "user", "content": "Can you tell me something more?"}]` |

We took the reply we got back in `message1.content[0].text` (Claude's own answer) and fed it back in as an `"assistant"` turn, **before** the new `"user"` turn. Now the second request looks like a real conversation with two turns in it — because, as far as the API can tell, that's exactly what it is.

> 💡 **Why `"assistant"` and not `"user"` again?** The `role` field tells Claude *who said what*. `"user"` = you, `"assistant"` = Claude. To rebuild a conversation accurately, you replay it with the same roles it actually happened with — alternating `user → assistant → user → assistant...`, just like a real chat transcript.

### 🖥️ What actually happens when you run it

```
Response 1 Text: The capital of France is Paris.

Response 2 Text: # More About Paris

Here are some interesting facts about Paris:

- Population: Paris is home to about 2.2 million people...
- The Eiffel Tower: Built in 1889, it's the iconic symbol of Paris...
- River Seine: The city is beautifully situated along this famous river...
- Art & Culture: Paris is renowned for its world-class museums...

Is there any particular aspect of Paris you'd like to know more about?
```

Same follow-up question. Completely different — and now genuinely useful — answer. Claude correctly inferred we wanted "more" about *Paris*, because this time, Paris was actually in the conversation we sent it.

> ℹ️ You may get slightly different wording if you run this yourself — that's normal, the model isn't guaranteed to produce identical text every time.

---

## 🧵 Why does the API even work this way?

It's tempting to think of this as a missing feature, but it's a deliberate design choice, and understanding *why* will save you a lot of confusion later:

- **The server stays simple and scalable.** If Anthropic's servers had to remember millions of users' ongoing conversations, that's an enormous amount of state to store, secure, and clean up. Instead, the model is a pure function: *messages in → response out*. Nothing to remember, nothing to clean up.
- **You own the conversation.** Because *you* hold the history, *you* control it. You can edit a previous turn, delete something before resending it, summarize an old part of the conversation to save space, or branch one conversation into two different directions — none of that would be possible if the server owned your chat history.
- **This is literally what a "context window" is.** Every time you hear that a model has, say, a "200K token context window," this is what it means: the `messages` list you send *is* everything the model can see. There's no hidden memory beyond it.

---

## ⚠️ Mistakes to watch out for

| Mistake | What goes wrong |
|---|---|
| Only sending the newest message, forgetting earlier turns | Claude answers as if the conversation just started — exactly the bug in `agent_03.py` |
| Mixing up `"role"` values (e.g. labeling Claude's own reply as `"user"`) | Claude gets confused about who said what, and may respond as if talking to itself |
| Letting the `messages` list grow forever in a long-running app | Every resent turn costs input tokens again — a 50-turn conversation resends *all 50 turns* on message 51. (We'll deal with trimming/summarizing history in a later level.) |

---

## ▶️ How to run this yourself

1. Make sure your virtual environment is active and your `.env` file has `ANTHROPIC_API_KEY` set (see [Level 01](../level-01_build_a_basic_agent/LEARN-AND-RUN.md) if you haven't set this up yet).
2. From the project root, run the broken version first, so you can see the problem with your own eyes:
   ```
   python level-03_claude_llm_model_api_is_stateless/scripts/agent_03.py
   ```
3. Now run the fixed version, and compare the second response:
   ```
   python level-03_claude_llm_model_api_is_stateless/scripts/agent_03_revised.py
   ```
4. Read both outputs side by side. Same follow-up question, two very different answers — that gap *is* the lesson.

---

## 🧪 Try this next

1. **Add a third turn.** Take Claude's second reply and ask a third follow-up question (e.g. *"Which of those is the most visited?"*), remembering to include *both* previous turns in the `messages` list.
2. **Turn it into a loop.** Instead of writing out `message1`, `message2`, `message3` by hand, keep a single `messages = []` list, `.append()` the user's question and the assistant's reply after every call, and loop with `input()` to chat continuously.
3. **Watch the cost grow.** Print `message.usage.input_tokens` after each call in your loop — you'll see it climb every turn, because the entire history is being resent each time. This is *the* reason long conversations get more expensive as they go on.

---

## 📚 Reference

- [Claude API Docs — Messages](https://docs.claude.com/en/api/messages)
- [Working with Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Level 01: First AI Agent Script](../level-01_build_a_basic_agent/LEARN-AND-RUN.md)
- [Level 02: Anatomy of a Claude API Response](../level-02_anatomy_of_claude_response/API_RESPONSE_ANATOMY.md)
