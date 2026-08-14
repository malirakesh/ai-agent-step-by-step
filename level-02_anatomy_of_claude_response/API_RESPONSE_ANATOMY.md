# 🧩 Anatomy of a Claude API Response

> A beginner-friendly breakdown of every field in the `Message` object returned by the Claude Messages API — using a real example (`"What is the capital of France?"`) as reference.

---

## 📦 Example Response

```python
Message(
    id='msg_011Cdv1HNhYebBLHWWTFrZvf',
    container=None,
    content=[
        TextBlock(
            citations=None,
            text='The capital of France is Paris.',
            type='text'
        )
    ],
    model='claude-haiku-4-5-20251001',
    role='assistant',
    stop_details=None,
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=Usage(
        cache_creation=CacheCreation(
            ephemeral_1h_input_tokens=0,
            ephemeral_5m_input_tokens=0
        ),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        inference_geo='not_available',
        input_tokens=14,
        output_tokens=10,
        output_tokens_details=None,
        server_tool_use=None,
        service_tier='standard'
    )
)
```

---

## 🟦 Top-Level Fields

### 🔑 `id`
A unique identifier for this specific API call, e.g. `msg_011Cdv1H...`.

> 💡 **Why it matters:** Useful for logging, debugging, or referencing a specific request when troubleshooting with support.

---

### 📦 `container`
Only relevant when using the **code execution tool** — points to the sandboxed execution environment.

> ⚪ `None` here because no tools were used.

---

### 🟩 `content` — *the actual response*
A **list** of content blocks (not a plain string!). Claude can return multiple types of content in one response — text, tool calls, images, etc.

| Sub-field | Meaning |
|---|---|
| `text` | The actual answer — `"The capital of France is Paris."` |
| `type` | `'text'` tells you what *kind* of block this is (vs. `'tool_use'`, `'server_tool_use'`, etc.) |
| `citations` | Populated only when the answer is grounded in a source (e.g. web search). `None` here. |

> ⚠️ **Common beginner mistake:** Treating `content` as a string instead of a list of blocks. Always loop through it.

---

### 🤖 `model`
Confirms exactly which model snapshot generated the response — `claude-haiku-4-5-20251001`.

> 💡 **Why it matters:** If you use model aliases, check this field to see the exact version that actually ran.

---

### 👤 `role`
Always `'assistant'` for a response.

> 💡 **Why it matters:** When building multi-turn conversations, append this back into your `messages` array as `role: 'assistant'` before sending the next user turn.

---

### 🛑 `stop_reason` — *the most important field for beginners*
Tells you **why** Claude stopped generating.

| Value | Meaning |
|---|---|
| ✅ `end_turn` | Claude finished naturally (what happened here) |
| ✂️ `max_tokens` | Cut off — hit your `max_tokens` limit |
| 🚧 `stop_sequence` | Hit a custom stop string you defined |
| 🔧 `tool_use` | Claude wants to call a tool and is pausing for you to run it |
| 🚫 `refusal` | Claude declined to continue for policy reasons |

> ⚠️ **Always check this in production.** If `stop_reason == 'max_tokens'`, your response is likely truncated and incomplete.

---

### 📋 `stop_details`
Extra structured detail about the stop — mainly populated when `stop_reason` is `'refusal'` (identifies the policy category).

> ⚪ `None` for a normal completed answer.

---

### ✂️ `stop_sequence`
If you configured custom stop sequences and one was hit, it appears here.

> ⚪ `None` because none were used/hit.

---

### 🏷️ `type`
Confirms the object type is `'message'`.

> 💡 **Why it matters:** Useful when parsing different event/object types, especially during streaming.

---

## 🟨 `usage` — Token Accounting (the billing section)

| Field | Value | Meaning |
|---|---|---|
| 📥 `input_tokens` | `14` | Tokens processed at full price (not from cache) |
| 📤 `output_tokens` | `10` | Tokens Claude generated in the reply |
| 💾 `cache_creation_input_tokens` | `0` | Tokens newly written to the prompt cache |
| ⚡ `cache_read_input_tokens` | `0` | Tokens read cheaply from an existing cache |
| 🌍 `inference_geo` | `'not_available'` | Geographic region that handled inference, if available |
| 🔧 `server_tool_use` | `None` | Usage stats for server-side tools (web search, code exec) — only populated if used |
| 🏗️ `service_tier` | `'standard'` | Processing tier handling the request (affects cost/latency) |

### 💾 Nested: `cache_creation`
| Field | Meaning |
|---|---|
| `ephemeral_5m_input_tokens` | Tokens written with a 5-minute cache TTL |
| `ephemeral_1h_input_tokens` | Tokens written with a 1-hour cache TTL |

> ℹ️ **Both cache fields are `0` here** because this was a short, one-off prompt — prompts below the model's minimum cacheable length simply aren't cached, silently and without error.

---

## ✅ TL;DR — What Matters Most for Beginners

| Priority | Field | Why |
|---|---|---|
| 🥇 | `content` | This is your actual answer — parse it as a list |
| 🥈 | `usage` | This is what you're billed for (`input_tokens + output_tokens`) |
| 🥉 | `stop_reason` | Silently forgetting this = silently truncated responses |

---

## 📚 Reference

- [Claude API Docs](https://docs.claude.com/en/api/overview)
- [Prompt Caching Guide](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Working with Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
