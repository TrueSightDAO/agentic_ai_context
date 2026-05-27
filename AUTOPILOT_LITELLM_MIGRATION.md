# LiteLLM Harness for Autopilot — Execution Roadmap

**Status as of 2026-05-27:** pre-flight  
**Goal:** Replace the homegrown HTTP transport + regex-based DeepSeek XML/DSML
tool-call parsing with `litellm`, a battle-tested library that handles provider
quirks natively.

## Rationale

- DeepSeek sometimes emits tool calls as raw XML/DSML in `content` instead of
  the standard `tool_calls` array — a class of bugs that regex patching cannot
  fully close.
- LiteLLM is the industry standard abstraction for 100+ LLM providers; it
  returns clean, standard `tool_calls` arrays regardless of provider.
- Switching provider later (e.g. DeepSeek → Claude) becomes a one-line config
  change (`LITELLM_MODEL=anthropic/claude-sonnet-4-20250514`).

## Pre-flight checklist

- [x] LiteLLM is compatible with our DeepSeek API key (OpenAI-compatible endpoint)
- [x] `litellm>=1.75.0` is in `requirements.txt`
- [x] `_parse_xml_tool_calls` and `_strip_provider_artifacts` are no longer
  needed — LiteLLM returns standard tool_calls
- [ ] `SESSION_LOG_DIR` set to `/opt/truesight_autopilot/sessions` in production `.env`
- [ ] DeepSeek API key available in production `.env` (`DEEPSEEK_API_KEY`)

## Sequenced plan

### PR1 — Add LiteLLM provider + switch config (this PR)

| Step | Description |
|------|-------------|
| 1a | Create `app/llm/litellm_provider.py` — `LiteLLMProvider` using `litellm.completion()` |
| 1b | Register `litellm` provider in `app/llm/registry.py` |
| 1c | Add `litellm>=1.75.0` to `requirements.txt` |
| 1d | Switch `.env`: `LLM_PROVIDER=litellm`, add `LITELLM_MODEL=deepseek/deepseek-chat` |
| 1e | Commit, push, deploy to production |
| 1f | Smoke test: send a message to autopilot via Telegram, verify no XML leak |
| 1g | Verify session persistence: restart service, send another message, confirm history |

### PR2 (future) — Clean up dead code

| Step | Description |
|------|-------------|
| 2a | Remove `_parse_xml_tool_calls` and `_strip_provider_artifacts` from `deepseek.py` |
| 2b | Remove `_normalize_tool_calls` override — standard path handles everything |
| 2c | Remove the session-restore XML-cleaning regex from `main.py:_load_or_create_session` |

## Resume tracker

| Unit | Status |
|------|--------|
| PR1 — LiteLLM provider | ☐ open |
| PR1 — merged | ☐ |
| PR1 — deployed & smoke-tested | ☐ |
| PR1 — contribution reported | ☐ |
| PR2 — dead code cleanup | ☐ |

> **RESUME HERE:** PR1 step 1a — create `app/llm/litellm_provider.py`
