#!/usr/bin/env python3
"""Record an approved public-site demo with Playwright. Never use for login-protected tools."""
from __future__ import annotations
import argparse, json
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--seconds", type=float, default=10)
    ap.add_argument("--actions", type=Path, help="Approved JSON list: wait, click, type, scroll, or goto actions.")
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
        page.goto(args.url, wait_until="domcontentloaded")
        page.evaluate("""() => { const c=document.createElement('div'); c.id='her-ai-cursor'; c.style.cssText='position:fixed;z-index:2147483647;width:22px;height:22px;border:3px solid white;border-radius:50%;background:#1b5e45;box-shadow:0 2px 8px #0008;pointer-events:none;left:50%;top:50%'; document.body.append(c); }""")
        actions = json.loads(args.actions.read_text(encoding="utf-8")) if args.actions else [{"wait": args.seconds}]
        for action in actions:
            if "wait" in action:
                page.wait_for_timeout(float(action["wait"]) * 1000)
            elif "goto" in action:
                page.goto(action["goto"], wait_until="domcontentloaded")
            elif "click" in action:
                page.locator(action["click"]).click()
            elif "type" in action:
                typing = action["type"]
                target = page.locator(typing["selector"])
                target.click()
                # Visible typing makes the recorded demo feel live. Use 55 ms
                # per character unless a tested action plan specifies otherwise.
                target.press_sequentially(typing["text"], delay=float(typing.get("delay_ms", 55)))
            elif "press" in action:
                keypress = action["press"]
                page.locator(keypress["selector"]).press(keypress.get("key", "Enter"))
            elif "scroll" in action:
                page.mouse.wheel(0, float(action["scroll"]))
            else:
                raise SystemExit(f"Unsupported action: {action}")
        page.close(); context.close(); browser.close()
    print(f"Recording written to {args.out_dir}. This script is for public pages only; every action must be approved before recording.")


if __name__ == "__main__":
    main()
