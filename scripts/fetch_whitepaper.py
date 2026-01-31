#!/usr/bin/env python3
"""
Fetch TrueSight DAO whitepaper content from truesight.me/whitepaper.

The public URL redirects (via JS + meta refresh) to a Google Doc.
This script tries:
  1. Google Docs export URL (no credentials; works if doc is "anyone with link can view")
  2. Google Docs API (if GOOGLE_APPLICATION_CREDENTIALS or --credentials is set)

Usage:
  pip install -r requirements.txt
  python fetch_whitepaper.py                    # print to stdout
  python fetch_whitepaper.py -o ../WHITEPAPER_SNAPSHOT.md
  python fetch_whitepaper.py --credentials /path/to/service-account.json -o ../WHITEPAPER_SNAPSHOT.md
"""

import argparse
import os
import sys

# Canonical Google Doc ID (from truesight_me/whitepaper/index.html)
WHITEPAPER_DOC_ID = "1P-IJq71N0lXszUOdqdjrGwonZAfEuG1q_tJFDdKKIic"
EXPORT_URL = f"https://docs.google.com/document/d/{WHITEPAPER_DOC_ID}/export?format=txt"


def fetch_via_export() -> str | None:
    """Try to fetch via Google Docs export URL (no auth). Works if doc is public."""
    try:
        import requests
    except ImportError:
        return None
    r = requests.get(EXPORT_URL, allow_redirects=True, timeout=30)
    if r.status_code != 200:
        return None
    text = r.text
    # Export often returns HTML; if it looks like login page or error, treat as failure
    if "accounts.google.com" in text or "Sign in" in text and "Google" in text:
        return None
    return text.strip() or None


def fetch_via_docs_api(credentials_path: str | None) -> str | None:
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
        doc = service.documents().get(documentId=WHITEPAPER_DOC_ID).execute()
    except (HttpError, OSError, ValueError):
        return None
    # Build plain text from structural content
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch TrueSight DAO whitepaper content")
    parser.add_argument("-o", "--output", metavar="FILE", help="Write content to FILE (default: stdout)")
    parser.add_argument("--credentials", metavar="PATH", help="Path to Google service account JSON (optional)")
    args = parser.parse_args()

    text = None
    # 1) Try export URL first (no creds)
    text = fetch_via_export()
    if not text:
        # 2) Try Docs API if credentials available
        text = fetch_via_docs_api(args.credentials)

    if not text:
        print(
            "Could not fetch whitepaper. Try:\n"
            "  1. Ensure the Google Doc is 'Anyone with the link can view', or\n"
            "  2. Set GOOGLE_APPLICATION_CREDENTIALS (or --credentials) to a service account JSON that has access.\n"
            "  3. Use a browser to open https://truesight.me/whitepaper and copy the content.",
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
