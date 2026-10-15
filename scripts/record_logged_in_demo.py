#!/usr/bin/env python3
"""Print the safe capture checklist for demos requiring an authenticated session.

This script deliberately does not receive credentials or browser profiles.
"""
from __future__ import annotations
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--url", required=True)
ap.add_argument("--project", required=True)
args = ap.parse_args()
print(f"Open {args.url} in your usual signed-in browser session.")
print("CLIENT-LED LIVE DEMO MODE")
print("1. The client logs in personally; do not share passwords, cookies, browser profiles, API keys, or recovery codes.")
print("2. Open the agreed demo workspace only. Hide unrelated tabs, account data, and private conversations.")
print("3. Confirm the approved actions, exact prompt, visible data, and recording start point before anyone begins navigating.")
print("4. Record only the post-login demo actions. Stop immediately if unexpected private data appears.")
print("5. Do not publish, delete, invite users, change billing, or change account settings without explicit client approval.")
print("Use macOS Cmd-Shift-5 (or your approved local recorder) and save the raw file under:")
print(f"{args.project}/raw/")
print("Never share passwords, cookies, browser profiles, or session_state files with this project.")
