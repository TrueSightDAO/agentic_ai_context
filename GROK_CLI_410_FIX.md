# Grok CLI 410 "Live search is deprecated" fix

## What happened

xAI deprecated the **Live Search API** (the old `search_parameters` in chat requests). Any request that includes `search_parameters` now returns **410 Gone** with:

```text
Live search is deprecated. Please switch to the Agent Tools API:
https://docs.x.ai/docs/guides/tools/overview
```

The **Grok CLI** you use is **@vibe-kit/grok-cli** (installed globally). It was sending `search_parameters: { mode: "auto" }` or `{ mode: "off" }` on every request, which triggered this 410.

## What was done

The **installed package** was patched so it **no longer sends** `search_parameters` to the API:

- **File:**  
  `~/.nvm/versions/node/v20.19.1/lib/node_modules/@vibe-kit/grok-cli/dist/grok/client.js`
- **Change:**  
  In both `chat()` and `chatStream()`, the code that adds `requestPayload.search_parameters` was commented out. Requests are now plain chat completions (no live search).

After this patch, `grok` in the CLI should work again, but **without** built-in web/live search until the CLI is updated to use xAI’s new Agent Tools API.

## After `npm update -g` or reinstall

Reinstalling or updating the package will overwrite the patched file and the 410 can come back. If it does:

1. **Option A – Patch again**  
   In the same `client.js` file, comment out again the two blocks that set `requestPayload.search_parameters` (in `chat()` and `chatStream()`).

2. **Option B – Update CLI**  
   Check for a new version of **@vibe-kit/grok-cli** that uses the [Agent Tools API](https://docs.x.ai/docs/guides/tools/overview) instead of Live Search, and upgrade.

3. **Option B – Other CLI**  
   Use another Grok CLI that already supports the new API (e.g. one that uses `/v1/responses` and tools like `web_search` / `x_search`).

## Auto-accept edits (no per-edit confirmation)

A separate patch adds a way to skip confirming every file edit and bash command:

- **CLI flag:** run `grok --yes` (or `grok -y`) to auto-accept all operations for that session.
- **Env var:** set `GROK_AUTO_ACCEPT=1` (or `true`) so every `grok` run auto-accepts (e.g. in `~/.zshrc` or project `.env`).

**Patched file:** `$(npm root -g)/@vibe-kit/grok-cli/dist/index.js` (adds `-y, --yes` option and checks `GROK_AUTO_ACCEPT` before starting the UI).

Reinstalling/updating the package will remove this; re-apply the same changes to `index.js` if needed.

---

## Reference

- xAI Agent Tools API: https://docs.x.ai/docs/guides/tools/overview  
- Your Grok CLI: `npm list -g @vibe-kit/grok-cli`  
- Patched files: `dist/grok/client.js` (410 fix), `dist/index.js` (--yes / GROK_AUTO_ACCEPT)
