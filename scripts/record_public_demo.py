#!/usr/bin/env python3
"""Record a public URL with Playwright. Never use for login-protected tools."""
from __future__ import annotations
import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--seconds", type=float, default=10)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1080, "height": 1350},
            record_video_dir=str(args.out_dir),
            record_video_size={"width": 1080, "height": 1350},
        )
        page = context.new_page()
        page.goto(args.url, wait_until="networkidle")
        page.evaluate("""() => { const c=document.createElement('div'); c.id='her-ai-cursor'; c.style.cssText='position:fixed;z-index:2147483647;width:22px;height:22px;border:3px solid white;border-radius:50%;background:#1b5e45;box-shadow:0 2px 8px #0008;pointer-events:none;left:50%;top:50%'; document.body.append(c); }""")
        page.wait_for_timeout(args.seconds * 1000)
        page.close(); context.close(); browser.close()
    print(f"Recording written to {args.out_dir}. This script records a public page only; add interaction beats once selectors are approved.")


if __name__ == "__main__":
    main()
