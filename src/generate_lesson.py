#!/usr/bin/env python3
"""
CLI agent that researches a Year 9 Geography topic on the web and writes out
a ready-to-use online lesson (HTML + JSON) for South Australian Year 7-10
HASS classes.

Usage:
    python src/generate_lesson.py --topic "Desertification and food security in the Sahel" \
        --unit biomes-and-food-security

    python src/generate_lesson.py --list-descriptors

Requires ANTHROPIC_API_KEY to be set (see .env.example).
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from agent import AgentError, run_agent
from curriculum import UNITS, format_checklist
from render import render_lesson_html

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "lessons"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "lesson"


def load_env_file():
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--topic", help="The lesson topic, e.g. 'Desertification in the Sahel'")
    parser.add_argument(
        "--unit",
        choices=list(UNITS.keys()),
        default="biomes-and-food-security",
        help="Which Year 9 Geography unit this lesson belongs to",
    )
    parser.add_argument("--duration", type=int, default=70, help="Target lesson length in minutes")
    parser.add_argument("--out", default=None, help="Output filename stem (default: derived from topic)")
    parser.add_argument("--list-descriptors", action="store_true", help="Print the curriculum checklist and exit")
    args = parser.parse_args()

    if args.list_descriptors:
        print(format_checklist())
        return

    if not args.topic:
        parser.error("--topic is required (or use --list-descriptors)")

    load_env_file()

    print(f"Researching and drafting: {args.topic!r} ({args.unit})...")
    try:
        lesson = run_agent(args.topic, args.unit, args.duration)
    except AgentError as e:
        sys.exit(str(e))

    OUTPUT_DIR.mkdir(exist_ok=True)
    stem = slugify(args.out or lesson.get("title") or args.topic)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    json_path = OUTPUT_DIR / f"{timestamp}-{stem}.json"
    html_path = OUTPUT_DIR / f"{timestamp}-{stem}.html"

    json_path.write_text(json.dumps(lesson, indent=2))
    html_path.write_text(render_lesson_html(lesson))

    print(f"Wrote {html_path}")
    print(f"Wrote {json_path}")
    print("Review the sources and content before using this in class.")


if __name__ == "__main__":
    main()

