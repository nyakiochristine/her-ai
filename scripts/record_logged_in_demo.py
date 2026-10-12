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
print("Verify the demo state, hide account data and unrelated tabs, then record only the post-login demo actions.")
print("Use macOS Cmd-Shift-5 (or your approved local recorder) and save the raw file under:")
print(f"{args.project}/raw/")
print("Never share passwords, cookies, browser profiles, or session_state files with this project.")
