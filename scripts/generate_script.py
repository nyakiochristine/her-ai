#!/usr/bin/env python3
"""Create a concise, editable reel-script draft from an approved brief.

This intentionally produces a transparent template rather than making unverified
claims about a product. Edit and approve the result before voice generation.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def field(brief: str, label: str, default: str = "") -> str:
    match = re.search(rf"^-\s*{re.escape(label)}:\s*(.+)$", brief, re.M | re.I)
    return match.group(1).strip() if match else default


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True, type=Path)
    parser.add_argument("--language", choices=("en", "nl"), default="en")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    brief = args.brief.read_text(encoding="utf-8")
    claim = field(brief, "Core claim", "One practical thing worth knowing about AI")
    cta = field(brief, "CTA/end card", "Follow Her AI for practical AI literacy.")
    topic = field(brief, "Topic/pillar", "Practical AI education")
    if args.language == "nl":
        text = (f"Even een snelle reality check over {topic.lower()}.\n\n"
                f"Vandaag testen we dit idee: {claim}\n\n"
                "Kijk naar wat er in beeld gebeurt. De uitkomst hangt af van de context, instellingen en invoer die de tool op dat moment kan gebruiken.\n\n"
                "Dit is de praktische les: controleer altijd wat de AI echt kan zien, onthouden of afleiden.\n\n"
                f"{cta}")
    else:
        text = (f"Quick reality check about {topic.lower()}.\n\n"
                f"Here is the idea we are testing: {claim}\n\n"
                "Watch what happens on screen. The result depends on the context, settings, and input the tool can access at that moment.\n\n"
                "The practical lesson is simple: check what an AI can actually see, remember, or infer.\n\n"
                f"{cta}")
    out = args.out or args.brief.parent / f"script.{args.language}.txt"
    out.write_text(text + "\n", encoding="utf-8")
    words = len(re.findall(r"\b[\w’'-]+\b", text))
    print(f"Wrote {out} ({words} words; target is 70–85). Edit and approve before voice generation.")


if __name__ == "__main__":
    main()
