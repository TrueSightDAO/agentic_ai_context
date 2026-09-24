#!/usr/bin/env python3
"""Render a SunMint / TrueSight DAO "Certificate of Tree Guardianship".

Deterministic and registry-sourced. Three hard rules (see
sops/SUNMINT_CERTIFICATE_ISSUE_SOP.md):

  1. The QR is ALWAYS the registry's own image
     (lineage-assets/pngs/<qr-id>.png) -- never re-encoded, never generated.
     It is sampled to its true module grid and re-rendered at an INTEGER
     scale (a non-integer NEAREST resize smears modules and kills scanning).
  2. The tree photo comes from the signed ledger payload's "Photo URL".
  3. The signature mark is a PRIVATE asset (signature_assets) passed in with
     --mark; it is deliberately never committed alongside the template.

Usage:
  python3 render_sunmint_certificate.py \
      --config example.config.json \
      --mark /path/to/sophia_truesight_signature_mark.png \
      --outdir /tmp/cert_out

Outputs, per variant: <outdir>/certificate_<variant>.png and .pdf (300 dpi).
"""

from __future__ import annotations

import argparse
import glob
import io
import json
import os
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- colours
CACAO = (58, 36, 22)
SAFFRON = (176, 102, 18)
GREEN = (30, 77, 43)
GREY = (122, 101, 86)
GOLD = (200, 121, 30)
INK = (28, 42, 68)

DEFAULTS = {
    "registry_base": "https://raw.githubusercontent.com/TrueSightDAO/lineage-assets/main",
    "scan_url_template": "https://edgar.truesight.me/agroverse/qr-code-check?qr_code={qr_id}",
    "kicker": "TRUESIGHT DAO   \u00b7   SUNMINT",
    "title": "Certificate of Tree Guardianship",
    "awarded_kicker": "AWARDED TO",
    "org_byline": "TrueSight DAO",
    "issuing_authority": "Issuing authority  \u00b7  SunMint reforestation",
    "issuer_name": "Sophia Truesight",
    "issuer_role": "SOPHIA TRUESIGHT  \u00b7  AUTOPILOT ADMINISTRATOR, TRUESIGHT DAO",
    "qr_caption": ["Scan \u2014 the registry QR", "for this cacao tree"],
    "border": "certificate_border.png",
    "with_photo": True,
    "variants": {
        "personal": [
            "is the guardian of a living cacao tree,",
            "planted in the Amazon rainforest on {date},",
            "in her name.",
        ],
        "institutional": [
            "is the guardian of a living cacao tree,",
            "planted in the Amazon rainforest on {date} and",
            "recorded on the TrueSight DAO's public, signed ledger.",
        ],
    },
}


def fetch_bytes(src: str) -> bytes:
    """Local path or http(s) URL -> bytes."""
    if src.startswith("http://") or src.startswith("https://"):
        with urllib.request.urlopen(src, timeout=60) as r:  # noqa: S310
            return r.read()
    with open(src, "rb") as fh:
        return fh.read()


def find_font(*patterns: str) -> str:
    for pat in patterns:
        hits = sorted(glob.glob(pat, recursive=True))
        if hits:
            return hits[0]
    raise SystemExit(f"font not found; tried: {patterns}")


# ------------------------------------------------- registry QR (rule 1)
def load_registry_qr(qr_id: str, registry_base: str):
    """Fetch the registry PNG, verify it decodes to the expected URL, and return
    a CLEAN, crisp module image: the registry's own modules center-sampled onto a
    module grid, then rendered as pure black/white (no anti-aliasing).

    The registry's pixels are the source of truth; we never re-encode a QR. We
    only threshold + integer-scale so the embedded tile is visually crisp (a
    LANCZOS downscale decodes but leaves ~20% mid-grey pixels -- it looks
    'garbled' even though scanners cope).
    """
    from pyzbar.pyzbar import decode
    import numpy as np

    url = f"{registry_base}/pngs/{qr_id}.png"
    im = Image.open(io.BytesIO(fetch_bytes(url))).convert("RGB")
    hits = decode(im)
    if not hits:
        raise SystemExit(f"registry PNG does not decode: {url}")
    payload = hits[0].data.decode()
    if qr_id not in payload:
        raise SystemExit(f"registry PNG payload {payload!r} lacks qr_id {qr_id!r}")
    r = hits[0].rect
    crop = im.crop((r.left, r.top, r.left + r.width, r.top + r.height))
    a = np.array(crop.convert("L")).astype(float)
    # Discover the module count N (QR v1..v40 -> 21,25,...,177) by center-sampling
    # each candidate grid and keeping the smallest N that still decodes.
    N = None
    for cand in range(21, 178, 4):
        g = np.zeros((cand, cand), bool)
        for j in range(cand):
            for i in range(cand):
                g[j, i] = (
                    a[
                        int((j + 0.5) * a.shape[0] / cand),
                        int((i + 0.5) * a.shape[1] / cand),
                    ]
                    < 128
                )
        tile = Image.fromarray(np.where(g, 0, 255).astype("uint8"), "L").convert("RGB")
        if decode(tile.resize((cand * 8, cand * 8), Image.NEAREST)):
            N = cand
            break
    if N is None:
        raise SystemExit(f"could not recover a decodable module grid for {url}")
    grid = np.zeros((N, N), bool)
    for j in range(N):
        for i in range(N):
            grid[j, i] = (
                a[int((j + 0.5) * a.shape[0] / N), int((i + 0.5) * a.shape[1] / N)]
                < 128
            )
    q = 4  # quiet zone, in modules
    full = np.zeros((N + 2 * q, N + 2 * q), bool)  # False = white
    full[q : q + N, q : q + N] = grid
    clean = Image.fromarray(np.where(full, 0, 255).astype("uint8"), "L").convert("RGB")
    if not decode(clean.resize((clean.width * 8, clean.height * 8), Image.NEAREST)):
        raise SystemExit(f"quiet-zoned module grid does not decode: {url}")
    print(
        f"  registry QR: {crop.size} native -> {N}x{N} modules "
        f"({crop.width / N:.3f} px/module), payload ok"
    )
    return clean, payload


def render_qr(registry_qr: Image.Image, px: int) -> Image.Image:
    """Integer-scale the clean module image to ~px, using NEAREST so every pixel
    is pure black or white (module size = whole pixels -> crisp, never garbled)."""
    from pyzbar.pyzbar import decode

    modules = registry_qr.width  # N + 2*quiet
    k = max(2, round(px / modules))  # integer pixels per module
    tile = registry_qr.resize((modules * k, modules * k), Image.NEAREST)
    if not decode(tile):
        for k2 in (k + 1, k - 1 if k > 2 else 3, 3, 4):
            t2 = registry_qr.resize((modules * k2, modules * k2), Image.NEAREST)
            if decode(t2):
                return t2
        raise SystemExit("could not integer-scale the registry QR to a scannable tile")
    return tile


def rounded(im: Image.Image, rad: int) -> Image.Image:
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, im.size[0] - 1, im.size[1] - 1], radius=rad, fill=255
    )
    out = Image.new("RGBA", im.size, (255, 255, 255, 255))
    out.paste(im.convert("RGBA"), (0, 0), mask)
    out.putalpha(mask)
    return out


# ------------------------------------------------------------------- build
def build(
    cfg: dict,
    variant: str,
    registry_qr: Image.Image,
    mark: Image.Image,
    photo,
    outdir: str,
    payload: str,
) -> str:
    border = Image.open(cfg["_border_path"]).convert("RGB")
    w, h = border.size
    s = w / 1600.0

    def font(path, px):
        return ImageFont.truetype(path, max(9, int(px * s)))

    f_ser = font(cfg["_ser"], 28)
    f_serb_48 = font(cfg["_serb"], 48)
    f_serb_72 = font(cfg["_serb"], 72)
    f_serb_19 = font(cfg["_serb"], 19)
    f_serb_17 = font(cfg["_serb"], 17)
    f_seri_24 = font(cfg["_seri"], 24)
    f_seri_15 = font(cfg["_seri"], 15)
    f_seri_17 = font(cfg["_seri"], 17)
    f_seri_13 = font(cfg["_seri"], 13)
    f_sig = font(cfg["_sig"], 40)

    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle(
        [int(0.10 * w), int(0.135 * h), int(0.90 * w), int(0.895 * h)],
        radius=int(18 * s),
        fill=(255, 251, 242, 218),
        outline=(200, 121, 30, 150),
        width=max(1, int(1.6 * s)),
    )

    def ctext(y, text, fnt, fill, track=0):
        if track:
            text = " ".join(list(text))
        bb = d.textbbox((0, 0), text, font=fnt)
        d.text(((int(w) - (bb[2] - bb[0])) / 2, y), text, font=fnt, fill=fill)
        return bb[3] - bb[1]

    y = int(0.166 * h)
    y += ctext(y, cfg["kicker"], f_serb_19, SAFFRON) + int(0.011 * h)
    y += ctext(y, cfg["title"], f_serb_48, CACAO) + int(0.008 * h)
    d.line(
        [(int(0.31 * w), y), (int(0.69 * w), y)],
        fill=(200, 121, 30, 190),
        width=max(1, int(1.5 * s)),
    )
    y += int(0.022 * h)
    y += ctext(y, cfg["awarded_kicker"], f_serb_17, GOLD, track=1) + int(0.012 * h)

    awardee = cfg["awardee"]
    y += ctext(y, awardee, f_serb_72, GREEN) + int(0.006 * h)
    bb = d.textbbox((0, 0), awardee, font=f_serb_72)
    x0 = (int(w) - (bb[2] - bb[0])) // 2
    d.line(
        [(x0, y - int(0.004 * h)), (x0 + bb[2] - bb[0], y - int(0.004 * h))],
        fill=(200, 121, 30, 170),
        width=max(1, int(1.2 * s)),
    )
    y += int(0.020 * h)

    date = cfg["date_display"]
    for i, line in enumerate(cfg["variants"][variant]):
        gap = (
            int(0.016 * h) if i == len(cfg["variants"][variant]) - 1 else int(0.004 * h)
        )
        y += ctext(y, line.format(date=date), f_ser, CACAO) + gap

    for line, px, col in [
        (cfg["location_line"], 28, CACAO),
        (cfg["coords_line"], 23, GREY),
        (cfg["species_line"], 23, GREY),
        ("Ledger reference:   " + cfg["ledger_ref"], 19, GREY),
        (cfg["batch_line"], 17, GREY),
    ]:
        y += ctext(y, line, font(cfg["_ser"], px), col) + int(0.0075 * h)
    info_end = y

    photo_holder = None
    if cfg.get("with_photo", True) and photo is not None:
        box_top, box_bot = info_end + int(0.014 * h), int(0.775 * h)
        avail_h = box_bot - box_top
        pw, ph = photo.size
        sc = min(int(0.30 * w) / pw, avail_h / ph)
        tw, th = max(1, int(pw * sc)), max(1, int(ph * sc))
        card = rounded(photo.resize((tw, th), Image.LANCZOS), rad=max(4, int(6 * s)))
        ImageDraw.Draw(card).rounded_rectangle(
            [0, 0, tw - 1, th - 1],
            radius=max(4, int(6 * s)),
            outline=(255, 255, 255, 255),
            width=max(1, int(2 * s)),
        )
        # left-align the photo with the text column (Gary: "more to the left")
        photo_x = int(0.165 * w)
        photo_holder = (card, (photo_x, box_top + (avail_h - th) // 2))
        print(
            f"  [{variant}] info_end={info_end / h:.3f}H "
            f"photo={tw}x{th} @y={photo_holder[1][1] / h:.3f}H"
        )

    sy = int(0.782 * h)
    d.line(
        [(int(0.165 * w), sy), (int(0.49 * w), sy)],
        fill=CACAO,
        width=max(1, int(1.1 * s)),
    )
    d.text(
        (int(0.165 * w), sy + int(0.009 * h)),
        cfg["org_byline"],
        font=f_seri_24,
        fill=CACAO,
    )
    d.text(
        (int(0.165 * w), sy + int(0.035 * h)),
        cfg["issuing_authority"],
        font=f_seri_15,
        fill=GREY,
    )

    mk = mark.convert("RGBA")
    mw = int(0.205 * w)
    mk = mk.resize((mw, int(mk.height * (mw / mk.width))))
    mk_x, mk_y = int(0.165 * w), int(0.828 * h)
    d.text((int(0.168 * w), int(0.900 * h)), cfg["issuer_name"], font=f_sig, fill=INK)
    d.text(
        (int(0.168 * w), int(0.941 * h)), cfg["issuer_role"], font=f_seri_13, fill=GREY
    )

    # 228px = 57 modules x 4 px/module: survives 150-dpi printing (171 -> 3px/module did not)
    qpx, qx, qy = 228, int(0.60 * w), int(0.686 * h)
    d.rounded_rectangle(
        [qx - 9, qy - 9, qx + qpx + 9, qy + qpx + 9],
        radius=9,
        fill=(255, 255, 255, 255),
        outline=GOLD,
        width=max(1, int(1.3 * s)),
    )

    out = Image.alpha_composite(border.convert("RGBA"), ov)
    if photo_holder:
        out.paste(photo_holder[0], photo_holder[1], photo_holder[0])
    out.paste(mk, (mk_x, mk_y), mk)
    out = out.convert("RGB")
    out.paste(render_qr(registry_qr, qpx), (qx, qy))

    d2 = ImageDraw.Draw(out)
    for i, cap in enumerate(cfg["qr_caption"]):
        bb = d2.textbbox((0, 0), cap, font=f_seri_17)
        d2.text(
            (
                qx + qpx / 2 - (bb[2] - bb[0]) / 2,
                qy + qpx + int(0.015 * h) + i * int(0.018 * h),
            ),
            cap,
            font=f_seri_17,
            fill=GREY,
        )

    os.makedirs(outdir, exist_ok=True)
    png = os.path.join(outdir, f"certificate_{variant}.png")
    out.save(png)
    out.save(png.replace(".png", ".pdf"), "PDF", resolution=300.0)

    # acceptance gate: the finished certificate MUST decode to the registry URL
    from pyzbar.pyzbar import decode

    hits = decode(Image.open(png))
    if not hits or hits[0].data.decode() != payload:
        raise SystemExit(
            f"FAIL: finished {variant} certificate does not decode to the registry payload"
        )
    print(f"  [{variant}] QR_OK (payload == registry) -> {png}")
    return png


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True)
    ap.add_argument(
        "--mark", required=True, help="private signature mark PNG (signature_assets)"
    )
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--no-photo", action="store_true")
    args = ap.parse_args(argv)

    with open(args.config) as fh:
        cfg = {**DEFAULTS, **json.load(fh)}
    cfg["_border_path"] = os.path.join(
        os.path.dirname(os.path.abspath(args.config)), cfg["border"]
    )
    cfg["_ser"] = find_font("/usr/share/fonts/**/DejaVuSerif.ttf")
    cfg["_serb"] = find_font("/usr/share/fonts/**/DejaVuSerif-Bold.ttf")
    cfg["_seri"] = find_font("/usr/share/fonts/**/DejaVuSerif-Italic.ttf")
    cfg["_sig"] = find_font(
        "/usr/share/fonts/opentype/urw-base35/Z003-MediumItalic.otf",
        "/usr/share/fonts/**/Z003*.otf",
    )
    if args.no_photo:
        cfg["with_photo"] = False

    print(f"fetching registry QR for {cfg['qr_id']} ...")
    registry_qr, payload = load_registry_qr(cfg["qr_id"], cfg["registry_base"])

    photo = None
    if cfg.get("photo_url"):
        photo = Image.open(io.BytesIO(fetch_bytes(cfg["photo_url"]))).convert("RGB")
        print(f"  tree photo: {photo.size} <- {cfg['photo_url']}")
    mark = Image.open(args.mark)

    cfg["qr_id"] = cfg["qr_id"]
    for variant in cfg.get("variants", DEFAULTS["variants"]):
        build(cfg, variant, registry_qr, mark, photo, args.outdir, payload)


if __name__ == "__main__":
    sys.exit(main())
