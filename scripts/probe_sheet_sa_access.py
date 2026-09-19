#!/usr/bin/env python3
"""Probe every Google service account against every tab of the Main Ledger.

Emits the SA->tab access matrix. Write-probe is an *empty string* written to the
bottom grid row of the tab (read back, never populated data) — so it is
non-destructive and safe to run any time.

Usage:
    python3 scripts/probe_sheet_sa_access.py [--spreadsheet <id>]

Requires the SA JSON keys on the box (see credentials/GOOGLE_SHEET_SA_ACCESS_MATRIX.md).
"""
import argparse
import glob
import json
import sys

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

MAIN_LEDGER = "1GE7PUq-UT6x2rBN-Q2ksogbWpgyuh2SaxJyG_uEK6PU"
KEY_GLOBS = [
    "/opt/truesight_autopilot/config/google/*.json",
    "/home/ubuntu/creds/*.json",
]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def load_keys():
    keys = {}
    for pattern in KEY_GLOBS:
        for path in glob.glob(pattern):
            try:
                with open(path) as fh:
                    data = json.load(fh)
            except Exception:
                continue
            email = data.get("client_email")
            if email:
                keys[email] = path
    return keys


def creds(path):
    return Credentials.from_service_account_file(path, scopes=SCOPES)


def classify(exc):
    msg = str(exc)
    if "protected" in msg:
        return "PROT"
    if "403" in msg:
        return "read"
    return "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spreadsheet", default=MAIN_LEDGER)
    args = ap.parse_args()

    keys = load_keys()
    if not keys:
        print("No SA keys found.", file=sys.stderr)
        return 1

    first = next(iter(keys.values()))
    svc = build("sheets", "v4", credentials=creds(first))
    meta = svc.spreadsheets().get(
        spreadsheetId=args.spreadsheet,
        fields="sheets(properties(title,gridProperties))",
    ).execute()
    dims = {
        s["properties"]["title"]: s["properties"]["gridProperties"].get("rowCount", 1000)
        for s in meta["sheets"]
    }

    order = sorted(keys)
    print(f"{'TAB':40}" + " ".join(f"{e.split('@')[0][:18]:>18}" for e in order))
    for tab, rows in dims.items():
        if tab == "Sheet51":
            continue
        rc = rows - 1 if rows > 1 else 1
        line = []
        for email in order:
            s = build("sheets", "v4", credentials=creds(keys[email]))
            try:
                s.spreadsheets().values().update(
                    spreadsheetId=args.spreadsheet,
                    range=f"'{tab}'!A{rc}",
                    valueInputOption="RAW",
                    body={"values": [[""]]},
                ).execute()
                line.append("W")
            except Exception as exc:  # noqa: BLE001 - classify, don't crash
                line.append(classify(exc))
        print(f"{tab:40}" + " ".join(f"{c:>18}" for c in line))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
