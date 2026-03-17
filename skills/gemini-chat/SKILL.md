---
name: gemini-chat
description: Interactive multi-turn chat with Google Gemini
argument-hint: "[-m 'message'] [--system 'prompt'] [--model gemini-2.5-pro]"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Gemini Chat

Interactive multi-turn conversation with Google Gemini. Uses the official
`google-genai` SDK for streaming chat with conversation history.

## Prerequisites

- **uv** installed
- **GEMINI_API_KEY** env var set (get a free key at https://aistudio.google.com/apikey)

## Usage

### Interactive chat (REPL)

```
uv run gemini-chat/scripts/chat.py
```

Start a back-and-forth conversation. Type messages, get streaming responses.
Type `quit` to exit, `save <file.json>` to save the conversation.

### Single message

```
uv run gemini-chat/scripts/chat.py -m "explain quantum computing simply"
```

### With a system prompt

```
uv run gemini-chat/scripts/chat.py --system "You are a senior Rust developer"
```

### Resume a previous conversation

```
uv run gemini-chat/scripts/chat.py --history chat.json
```

### With Google Search grounding (like AI Mode)

```
uv run gemini-chat/scripts/chat.py --search
uv run gemini-chat/scripts/chat.py --search -m "what happened in tech news today?"
```

### Options

| Flag                 | Description                                      |
|----------------------|--------------------------------------------------|
| `-m`, `--message`    | Single message (non-interactive mode)            |
| `--model MODEL`      | Model name (default: gemini-2.5-flash)           |
| `--system`, `-s`     | System instruction for the conversation          |
| `--history FILE`     | JSON file to load/save conversation history      |
| `--no-stream`        | Disable streaming (wait for full response)       |
| `--search`           | Enable Google Search grounding (like AI Mode)    |
| `--json`             | Output as JSON (single message mode only)        |

## Instructions

When the user wants to talk to Gemini or get Gemini's perspective on something:

1. Start an interactive session and relay the conversation:
   ```
   uv run gemini-chat/scripts/chat.py --system "<context about what to discuss>"
   ```

2. For a quick question, use single-message mode:
   ```
   uv run gemini-chat/scripts/chat.py -m "<question>" --json
   ```

3. To continue a previous conversation:
   ```
   uv run gemini-chat/scripts/chat.py --history /tmp/gemini-chat.json
   ```

4. When the user wants to compare perspectives or get a second opinion from
   Gemini, send the question and relay the response back.

5. If GEMINI_API_KEY is not set, instruct the user to get a free key at
   https://aistudio.google.com/apikey and set it:
   `export GEMINI_API_KEY='your-key'`

User arguments: $ARGUMENTS
