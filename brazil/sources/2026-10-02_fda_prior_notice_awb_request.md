# FDA Prior Notice — Iolanda requests the air waybill (2026-10-02)

**Source:** WhatsApp screenshot (Iolanda Santos — Omega, SISCOMEX/customs), shared by Gary in thread 10800, 2026-10-02 09:57 AM.
Higher-fidelity OCR (por) of the attachment.

## Verbatim (PT)

> "Assim que chegar na empresa, informo sobre a questão do status do embarque. Obrigado."
> "Oi Gary, conversei com a Isis que atua no nosso internacional e está cuidando do seu embarque. Ela irá passar para você e os envolvidos o status desse embarque."
> "Por favor, envie-me o conhecimento de embarque aéreo para que eu possa emitir a notificação prévia à FDA referente aos requisitos alfandegários dos EUA."

## Translation

> "As soon as I get to the company, I'll let you know about the shipment status question. Thanks."
> "Hi Gary, I spoke with Isis, who works in our international [department] and is handling your shipment. She'll pass the status of this shipment to you and everyone involved."
> "Please send me the **air waybill** so that I can issue the **FDA prior notice** regarding the US customs requirements."

## What it means

- **NEW hard gate identified: FDA Prior Notice (PN).** Iolanda (Omega, SISCOMEX/customs) will **file the FDA Prior Notice** for this consignment — a **mandatory** pre-arrival notification for US food imports. This was previously only implied in the runbook (Phase 7 "FDA processing ≈ $100 (if required)"); it is not optional for cacao.
- **Blocking dependency:** the PN **cannot be filed without the air waybill (AWB)**. The AWB is being reissued by SeaCoast (gated on flight-status confirmation, §5.5). So the critical path is:
  `flight confirmed → SeaCoast reissues HAWB/MAWB → AWB sent to Iolanda → Iolanda files FDA PN → arrival → US customs/CBP`.
- **Timing rules (21 CFR 1.279):** PN must be received & **confirmed by FDA no less than 4 hours before arrival by air**; and generally **no more than 15 calendar days before arrival** if filed via FDA's **PNSI** (or 30 days via CBP ABI/ACE).
- **Role split reaffirmed:** Isis = international/export operations (owns the shipment status + flight); Iolanda = SISCOMEX/customs — but here Iolanda owns the **US-side FDA filing** too. Iolanda says she is **back at the office** ("assim que chegar na empresa") as of this morning.

## Evidence

- `brazil/sources/2026-10-02_fda_prior_notice_awb_request.md` (this file)
- WhatsApp screenshot `a12db6f45d484f2eb6d53de01cf363f7.jpg` (thread 10800)
- FSVP process context: `fsvp/SHIPMENT_DOCUMENTATION_PROCESS.md` (doc #4 = FDA prior notice, "filed per FDA PNSI before arrival")
- FDA guidance: "Prior Notice of Imported Food Shipments" (21 CFR Part 1 Subpart I)

## Status

- ⬜ **AWB sent to Iolanda** — owner: Gary/SeaCoast (blocked on flight confirmation, §5.5).
- ⬜ **FDA Prior Notice filed** — owner: Iolanda (Omega).
