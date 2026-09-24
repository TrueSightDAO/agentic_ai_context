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

    If the registry PNG carries a smooth centre overlay (e.g. the Agroverse
    mark), thresholding would shatter it into speckle, so we ALSO return the
    overlay's native-resolution pixels + module box for render_qr() to paste back
    on top of the crisp tile. Returns (clean, payload, logo_src, logo_box).
    """
    from pyzbar.pyzbar import decode
    import numpy as np

    url = f"{registry_base}/pngs/{qr_id}.png"
    im = Image.open(io.BytesIO(fetch_bytes(url))).convert("RGB")
    hits = decode(im)
    if not hits:
        # Some registry PNGs embed the QR small enough that pyzbar fails at native
        # size though the image decodes fine at 2-3x (cv2 and real scanners read it).
        # This affects the whole 2023SA... (Santa Anna) family -> every such cert was
        # previously un-renderable. Retry on an upscale before giving up; keep the
        # upscaled image so the crop and the overlay stay at (higher) native res.
        # NOTE: each retry must resize from the ORIGINAL image, never chain onto
        # the previous upscale -- chaining (2x then 3x then 5x) compounds to a
        # ~13500px image and the cv2 fallback below (another 5x) then allocates
        # >10 GB and gets OOM-killed. The whole 2023SA... (Santa Anna) family
        # (~450px PNGs) hit this: the cert was un-renderable on a small box.
        _native = im
        for _scale in (2, 3, 5):
            im = _native.resize(
                (_native.width * _scale, _native.height * _scale), Image.LANCZOS
            )
            hits = decode(im)
            if hits:
                break
    if not hits:
        # pyzbar can fail on some small RGBA registry PNGs at EVERY scale (e.g. the
        # 2024PF_20250505_28 bag QR) while OpenCV reads them cleanly. Fall back to
        # cv2 so the certificate is not left un-renderable.
        from types import SimpleNamespace

        import cv2

        im = _native.resize((_native.width * 5, _native.height * 5), Image.LANCZOS)
        _txt, _pts, _ = cv2.QRCodeDetector().detectAndDecode(np.array(im.convert("L")))
        if _txt:
            _xs, _ys = _pts[0][:, 0], _pts[0][:, 1]
            _rect = SimpleNamespace(
                left=int(_xs.min()),
                top=int(_ys.min()),
                width=int(_xs.max() - _xs.min()),
                height=int(_ys.max() - _ys.min()),
            )
            hits = [SimpleNamespace(data=_txt.encode(), rect=_rect)]
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
    # Quiet zone in modules. The spec wants >=4 light modules around the symbol;
    # the renderer ALSO draws a white rounded box (fill=255) with 9px padding, so
    # 2 baked modules (8px @ k=4) + 9px box padding == 17px ~= 4.25 modules -> still
    # spec-compliant, while letting the tile shrink. (q=4 forced every k>=4 tile to
    # be >=228px, which read as oversized vs the surrounding elements.)
    q = 2  # quiet zone, in modules (the white box supplies the remainder)
    full = np.zeros((N + 2 * q, N + 2 * q), bool)  # False = white
    full[q : q + N, q : q + N] = grid
    clean = Image.fromarray(np.where(full, 0, 255).astype("uint8"), "L").convert("RGB")
    if not decode(clean.resize((clean.width * 8, clean.height * 8), Image.NEAREST)):
        raise SystemExit(f"quiet-zoned module grid does not decode: {url}")

    # The registry PNG may carry a smooth overlay (e.g. the Agroverse mark) in its
    # centre. Thresholding every module to pure black/white shatters that overlay
    # into speckle -- it *looks* garbled even though the QR still scans. Detect the
    # overlay as the block of modules whose source pixels are anti-aliased
    # (mid-grey), keep the source pixels at native resolution, and hand them back so
    # render_qr() can paste the original overlay back on top of the crisp grid.
    logo_src, logo_box = None, None
    mid = np.zeros((N, N), float)
    for j in range(N):
        for i in range(N):
            y0, y1 = int(j * a.shape[0] / N), int((j + 1) * a.shape[0] / N)
            x0, x1 = int(i * a.shape[1] / N), int((i + 1) * a.shape[1] / N)
            hh, ww = y1 - y0, x1 - x0
            # interior-only window: ignore module-boundary anti-aliasing
            sub = a[y0 + hh // 4 : y1 - hh // 4, x0 + ww // 4 : x1 - ww // 4]
            if sub.size:
                mid[j, i] = ((sub > 45) & (sub < 215)).mean()
    ys, xs = np.where(mid > 0.7)
    # grow ~2 modules so the whole overlay is covered, not just its solid core
    if len(ys) >= 4:  # a real overlay spans several modules
        pad = 2
        ly0 = max(0, ys.min() - pad)
        ly1 = min(N, ys.max() + 1 + pad)
        lx0 = max(0, xs.min() - pad)
        lx1 = min(N, xs.max() + 1 + pad)
        logo_src = crop.crop(
            (
                int(lx0 * a.shape[1] / N),
                int(ly0 * a.shape[0] / N),
                int(lx1 * a.shape[1] / N),
                int(ly1 * a.shape[0] / N),
            )
        )
        logo_box = (lx0 + q, ly0 + q, lx1 + q, ly1 + q)  # modules, incl. quiet zone
        print(
            f"  registry QR overlay: {logo_src.size}px at modules "
            f"x{lx0}-{lx1} y{ly0}-{ly1} (restored at native resolution)"
        )

    print(
        f"  registry QR: {crop.size} native -> {N}x{N} modules "
        f"({crop.width / N:.3f} px/module), payload ok"
    )
    return clean, payload, logo_src, logo_box


def _paste_overlay(tile: Image.Image, k: int, logo_src, logo_box) -> Image.Image:
    """Paste the registry's native-resolution overlay pixels back onto the crisp,
    integer-scaled module grid, so a centre mark (e.g. the Agroverse logo) renders
    smooth instead of being shattered into speckle by the module threshold."""
    if logo_src is None or logo_box is None:
        return tile
    lx0, ly0, lx1, ly1 = logo_box
    dest = (lx0 * k, ly0 * k, lx1 * k, ly1 * k)
    w, h = dest[2] - dest[0], dest[3] - dest[1]
    if w <= 0 or h <= 0:
        return tile
    out = tile.copy()
    out.paste(logo_src.resize((w, h), Image.LANCZOS), (dest[0], dest[1]))
    return out


def render_qr(
    registry_qr: Image.Image, px: int, logo_src=None, logo_box=None
) -> Image.Image:
    """Integer-scale the clean module image to ~px, using NEAREST so every pixel
    is pure black or white (module size = whole pixels -> crisp, never garbled);
    then re-composite the registry's own overlay pixels (if any) at native
    resolution so a centre logo stays smooth and recognisable."""
    from pyzbar.pyzbar import decode

    modules = registry_qr.width  # N + 2*quiet
    # HARD PRINT FLOOR: k >= 4 (4px == 0.339mm/module on this 2.88in card).
    # Digital decode() is NOT a print-safety gate -- #1354 shipped k=3 and
    # survived decode but was below the floor. Never round below 4.
    k = max(4, round(px / modules))  # integer pixels per module
    base_tile = registry_qr.resize((modules * k, modules * k), Image.NEAREST)

    # Preferred: overlay at the intended scale. If the centre mark pushes the
    # tile past pyzbar's error-correction budget (a native-res overlay pasted
    # over the symbol centre and heavily downscaled -- e.g. the 2024PAULO_*
    # bag QRs), FIRST shrink the overlay inward a few modules. That keeps BOTH
    # the centre mark AND the requested tile size / k, so the tile never grows
    # out of its layout box (the old behaviour escalated k, which silently
    # enlarged the tile + its box ~25% and overlapped the border art).
    tile = _paste_overlay(base_tile, k, logo_src, logo_box)
    if decode(tile):
        return tile
    if logo_src is not None and logo_box is not None:
        lx0, ly0, lx1, ly1 = (int(v) for v in logo_box)
        for shrink in (1, 2, 3, 4, 5):
            if (lx1 - lx0) - 2 * shrink < 2 or (ly1 - ly0) - 2 * shrink < 2:
                break
            t = _paste_overlay(
                base_tile,
                k,
                logo_src,
                (lx0 + shrink, ly0 + shrink, lx1 - shrink, ly1 - shrink),
            )
            if decode(t):
                print(
                    f"  registry QR overlay: shrunk {shrink} module(s)/side to "
                    f"stay within the error-correction budget at k={k}"
                )
                return t
    # Last resort only: escalate k (grows the tile -> may overflow the layout box).
    for k2 in (k + 1, k + 2, max(4, k - 1)):
        t2 = _paste_overlay(
            registry_qr.resize((modules * k2, modules * k2), Image.NEAREST),
            k2,
            logo_src,
            logo_box,
        )
        if decode(t2):
            return t2
    # never ship a non-decoding QR: fall back to the plain crisp tile
    if logo_src is not None and decode(base_tile):
        print(
            "  WARNING: overlay QR did not decode; shipping crisp tile "
            "without the centre overlay"
        )
        return base_tile
    raise SystemExit("could not integer-scale the registry QR to a scannable tile")


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
    photo_box = None
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
        photo_x = int(0.135 * w)
        photo_holder = (card, (photo_x, box_top + (avail_h - th) // 2))
        photo_box = (photo_holder[1][1], th)  # (top_y, height) of the placed photo
        print(
            f"  [{variant}] info_end={info_end / h:.3f}H "
            f"photo={tw}x{th} @y={photo_holder[1][1] / h:.3f}H"
        )

    sy = int(0.782 * h)
    d.line(
        [(int(0.135 * w), sy), (int(0.46 * w), sy)],
        fill=CACAO,
        width=max(1, int(1.1 * s)),
    )
    d.text(
        (int(0.135 * w), sy + int(0.009 * h)),
        cfg["org_byline"],
        font=f_seri_24,
        fill=CACAO,
    )
    # issuing_authority is a HEADER caption ("Issuing authority . SunMint
    # reforestation"), so it belongs on the byline row -- not at x=0.135w below
    # the rule, where it collided with the signature mark pasted at
    # (0.135w, 0.812h). The overlap produced the "two signatures" garbling Gary
    # flagged (2026-09-24).
    # Right-align to the content margin (mirror of the 0.135w left margin) so the
    # byline row reads as a balanced pair: "TrueSight DAO" left, authority right.
    bb_ia = d.textbbox((0, 0), cfg["issuing_authority"], font=f_seri_15)
    d.text(
        (int(0.865 * w) - (bb_ia[2] - bb_ia[0]), sy + int(0.009 * h)),
        cfg["issuing_authority"],
        font=f_seri_15,
        fill=GREY,
    )

    mk = mark.convert("RGBA")
    mw = int(0.150 * w)
    mk = mk.resize((mw, int(mk.height * (mw / mk.width))))
    mk_x, mk_y = int(0.135 * w), int(0.812 * h)
    d.text(
        (int(0.135 * w) + int(0.168 * w), int(0.808 * h)),
        cfg["issuer_name"],
        font=f_sig,
        fill=INK,
    )
    d.text(
        (int(0.135 * w) + int(0.168 * w), int(0.842 * h)),
        cfg["issuer_role"],
        font=f_seri_13,
        fill=GREY,
    )

    # QR tile = (modules) x integer k, where modules = 49 symbol + 2*q quiet-zone
    # (57 at q=4, 53 at q=2). k MUST stay >= 4 (4px == 0.339mm/module on this
    # 2.88in-wide card) to survive 150-dpi printing; k=3 (3px == 0.254mm/module,
    # the 171px tile) does NOT -- the #1350 comment '171 -> 3px/module did not' was
    # RIGHT. With q=2: 212px -> k=4 -> 212px, ~7% smaller than the 228px q=4 tile
    # and still print-safe. (Do NOT set qpx near 196: 196/53 rounds to k=3 -> 159px,
    # and at q=4 196/57 -> k=3 -> 171px, BOTH below the floor.)
    qr_px, qx = 212, int(0.60 * w)
    qr_tile = render_qr(
        registry_qr, qr_px, cfg.get("_qr_logo"), cfg.get("_qr_logo_box")
    )
    # Use the tile's ACTUAL width (modules x k, k>=4) for the box, vertical
    # centring and caption. Sizing those from the *requested* px desyncs them
    # from the pasted tile when round() lands off (the #1354 bug).
    qpx = qr_tile.width
    # Vertical-centre the QR against the photo it sits beside, so the two read as
    # ONE paired block rather than two floating elements. qy must derive from the
    # photo's ACTUAL placement: a hardcoded constant can only line up by coincidence,
    # because the photo's y depends on info_end, which varies with text length --
    # brittle for a reusable template. Fall back to the old constant with no photo.
    if photo_box:
        qy = photo_box[0] + (photo_box[1] - qpx) // 2
    else:
        qy = int(0.686 * h)
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
    out.paste(
        qr_tile,
        (qx, qy),
    )

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
    registry_qr, payload, qr_logo, qr_logo_box = load_registry_qr(
        cfg["qr_id"], cfg["registry_base"]
    )
    cfg["_qr_logo"], cfg["_qr_logo_box"] = qr_logo, qr_logo_box

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
