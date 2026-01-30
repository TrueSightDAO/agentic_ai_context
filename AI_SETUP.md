# AI CLI Setup (Claude Code, OpenAI Codex, Gemini)

This file documents how to check and set up the three AI code CLIs so they can use this workspace and **agentic_ai_context** to get up to speed.

## Check current setup

```bash
# Claude Code (Anthropic)
claude --version   # e.g. 2.1.5 (Claude Code)

# OpenAI Codex
codex --version   # e.g. codex-cli 0.23.0

# Google Gemini CLI
gemini --version  # e.g. 0.25.x
```

## Install what’s missing

### Claude Code

- **Official install (recommended):**  
  `curl -fsSL https://claude.ai/install.sh | bash`
- Requires: Node.js 18+, macOS 13+ / Ubuntu 20+ / Windows 10+
- Docs: https://docs.anthropic.com/en/docs/claude-code/setup

### OpenAI Codex

- Install via npm:  
  `npm install -g @openai/codex` (or the package name from [OpenAI Codex CLI](https://developers.openai.com/codex/quickstart))
- Requires: Node 22+ on Linux (GLIBC 2.39+); check official quickstart for macOS/Windows
- Docs: https://developers.openai.com/codex/quickstart

### Gemini CLI

- **npm (global):**  
  `npm install -g @google/gemini-cli`  
  Then run: `gemini`
- **Homebrew (macOS/Linux):**  
  `brew install gemini-cli`
- **Without install:**  
  `npx @google/gemini-cli`
- Requires: Node 18+ (20+ recommended)
- First run: sign in with Google or use API key from Google AI Studio
- Docs: https://google-gemini.github.io/gemini-cli/docs/get-started/

## Using this workspace with AIs

1. **Point AIs at context:** Ensure they can read:
   - `agentic_ai_context/WORKSPACE_CONTEXT.md` — workspace overview
   - `agentic_ai_context/PROJECT_INDEX.md` — per-project summary
2. **Credentials:** Never put secrets in agentic_ai_context. Use **agentic_ai_api_credentials** for env var names and docs only; real values stay in each project’s `.env`.
