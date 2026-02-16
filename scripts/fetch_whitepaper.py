#!/usr/bin/env python3
"""
Fetch TrueSight DAO whitepaper(s) from truesight.me.

Each public URL redirects (via JS + meta refresh) to a Google Doc.
This script tries:
  1. Google Docs export URL (no credentials; works if doc is "anyone with link can view")
  2. Google Docs API (if GOOGLE_APPLICATION_CREDENTIALS or --credentials is set)

Whitepapers on truesight.me:
  - main     truesight.me/whitepaper           (governance, project narrative)
  - edgar    truesight.me/edgar/whitepaper
  - agroverse truesight.me/agroverse/whitepaper
  - sunmint  truesight.me/sunmint/whitepaper

Usage:
  pip install -r requirements.txt
  python fetch_whitepaper.py                         # main only, print to stdout
  python fetch_whitepaper.py -o ../WHITEPAPER_SNAPSHOT.md
  python fetch_whitepaper.py --all -o ../            # fetch all four, write to ../*_SNAPSHOT.md
  python fetch_whitepaper.py --which edgar -o ../EDGAR_WHITEPAPER_SNAPSHOT.md
  python fetch_whitepaper.py --credentials /path/to/service-account.json --all -o ../
"""

import argparse
import os
import sys

# All whitepapers on truesight.me (from truesight_me/*/whitepaper/index.html)
WHITEPAPERS = {
    "main": {
        "doc_id": "1P-IJq71N0lXszUOdqdjrGwonZAfEuG1q_tJFDdKKIic",
        "url": "https://truesight.me/whitepaper",
        "snapshot_file": "WHITEPAPER_SNAPSHOT.md",
    },
    "edgar": {
        "doc_id": "1Ud19BdIKrg_2SvVYEfS2fxCFCwFGwuccqOD9z53k-oc",
        "url": "https://truesight.me/edgar/whitepaper",
        "snapshot_file": "EDGAR_WHITEPAPER_SNAPSHOT.md",
    },
    "agroverse": {
        "doc_id": "1b3JiawnqA1QNpA_XZMH6oNQ9ZVJnLRGtOWzM31YLvJs",
        "url": "https://truesight.me/agroverse/whitepaper",
        "snapshot_file": "AGROVERSE_WHITEPAPER_SNAPSHOT.md",
    },
    "sunmint": {
        "doc_id": "1BcrV4rtG5cNTdcycw2H94OI-pmT-dDal3x5jPcyvWC0",
        "url": "https://truesight.me/sunmint/whitepaper",
        "snapshot_file": "SUNMINT_WHITEPAPER_SNAPSHOT.md",
    },
}


def fetch_doc_via_export(doc_id: str) -> str | None:
    """Try to fetch via Google Docs export URL (no auth). Works if doc is public."""
    try:
        import requests
    except ImportError:
        return None
    url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
    r = requests.get(url, allow_redirects=True, timeout=30)
    if r.status_code != 200:
        return None
    text = r.text
    if "accounts.google.com" in text or ("Sign in" in text and "Google" in text):
        return None
    return text.strip() or None


def fetch_doc_via_docs_api(doc_id: str, credentials_path: str | None) -> str | None:
    """Fetch via Google Docs API using service account credentials."""
    creds_path = credentials_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path or not os.path.isfile(creds_path):
        return None
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
    except ImportError:
        return None
    SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]
    try:
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        service = build("docs", "v1", credentials=creds)
        doc = service.documents().get(documentId=doc_id).execute()
    except (HttpError, OSError, ValueError):
        return None
    content = doc.get("body", {}).get("content") or []
    parts = []
    for el in content:
        if "paragraph" in el:
            for e in el["paragraph"].get("elements", []):
                run = e.get("textRun", {}).get("content", "")
                if run:
                    parts.append(run)
        if "table" in el:
            for row in el["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    for e in cell.get("content", []):
                        if "paragraph" in e:
                            for pe in e["paragraph"].get("elements", []):
                                run = pe.get("textRun", {}).get("content", "")
                                if run:
                                    parts.append(run)
    return "".join(parts).strip() or None


def fetch_one(key: str, credentials_path: str | None) -> str | None:
    """Fetch a single whitepaper by key (main, edgar, agroverse, sunmint)."""
    info = WHITEPAPERS.get(key)
    if not info:
        return None
    doc_id = info["doc_id"]
    text = fetch_doc_via_export(doc_id)
    if not text:
        text = fetch_doc_via_docs_api(doc_id, credentials_path)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch TrueSight DAO whitepaper(s)")
    parser.add_argument("-o", "--output", metavar="PATH", help="Output file or directory (for --all)")
    parser.add_argument("--credentials", metavar="PATH", help="Path to Google service account JSON (optional)")
    parser.add_argument("--all", action="store_true", help="Fetch all four whitepapers (main, edgar, agroverse, sunmint)")
    parser.add_argument("--which", choices=list(WHITEPAPERS), help="Fetch only this whitepaper (default: main)")
    parser.add_argument("--list", action="store_true", help="List whitepaper keys and URLs, then exit")
    args = parser.parse_args()

    if args.list:
        for key, info in WHITEPAPERS.items():
            print(f"  {key:10} {info['url']}  -> doc id {info['doc_id']}")
        return 0

    which = args.which or "main"
    keys = list(WHITEPAPERS) if args.all else [which]
    credentials_path = args.credentials

    if args.all:
        if not args.output:
            parser.error("With --all, -o PATH is required (output directory, e.g. ..)")
        out_dir = args.output.rstrip("/")
        if not os.path.isdir(out_dir):
            out_dir = os.path.dirname(args.output) or "."
        ok = 0
        for key in keys:
            text = fetch_one(key, credentials_path)
            out_file = os.path.join(out_dir, WHITEPAPERS[key]["snapshot_file"])
            if text:
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Wrote {len(text)} chars -> {out_file}", file=sys.stderr)
                ok += 1
            else:
                print(f"Could not fetch {key} -> {out_file}", file=sys.stderr)
        if ok == 0:
            print(
                "Could not fetch any whitepaper. Try --credentials or ensure docs are 'Anyone with the link can view'.",
                file=sys.stderr,
            )
            return 1
        return 0

    text = fetch_one(which, credentials_path)
    if not text:
        info = WHITEPAPERS[which]
        print(
            f"Could not fetch {which} whitepaper ({info['url']}). Try:\n"
            "  1. Ensure the Google Doc is 'Anyone with the link can view', or\n"
            "  2. Set GOOGLE_APPLICATION_CREDENTIALS (or --credentials) to a service account JSON that has access.\n"
            f"  3. Use a browser to open {info['url']} and copy the content.",
            file=sys.stderr,
        )
        return 1

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote {len(text)} chars to {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
