
---

## Intro overlay standard (logo + title sizing)

Every **master** carries a rendered intro frame. Its logo height, band position, side margins and
title size are **normative** and live in one place:

> **`sops/INTRO_OVERLAY_STANDARD.md`** — the token set (`MARK_H`, `BADGE`, `PAD`, `CY`, `TITLE_PX`,
> `MARGIN_MIN`, `TITLE_MAX_W`), the canonical values, the pre-render assertions, and the open
> reconciliation against the `100-year-old-trees` reference master.

Why it is a separate, enforced standard: three build directories on this box rendered three
incompatible intro geometries (band top at y=297 / 283 / 117; side margins 186 / 253 / 125), so
masters from different builds do not match when played back-to-back. Builders must read the tokens
from that SOP and assert them **before** encoding — never hardcode px values.

A master's overlay is **baked in**. Share copies inherit it unchanged; changing it requires a new
master version, never a patch to a share copy.
