# SunMint Certificate template

Renderer for the TrueSight DAO / SunMint **Certificate of Tree Guardianship**.
Canonical procedure: [`sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md`](../../sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md).

```
python3 render_sunmint_certificate.py \
    --config example.config.json \
    --mark /path/to/sophia_truesight_signature_mark.png \
    --outdir /tmp/cert_out
```

- `--mark` is a **private** asset (`signature_assets`) — never commit it here.
- Emits `certificate_<variant>.png` and `.pdf` (300 dpi), personal + institutional.
- The build **fails** unless the finished cert's QR decodes to the exact registry payload.

## QR rule (important)

The QR is always the registry's own image (`lineage-assets/pngs/<qr-id>.png`) — never
generated or re-encoded. It is center-sampled onto its true module grid, given a
4-module quiet zone, and rendered at an **integer** pixels-per-module scale with
**NEAREST**. That yields pure black/white modules (0% anti-aliasing) — a LANCZOS resize
decodes but leaves ~20% mid-grey pixels and looks garbled.
