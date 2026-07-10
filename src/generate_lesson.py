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

from curriculum import UNITS, descriptors_for_unit, format_checklist
from prompts import SYSTEM_PROMPT, LESSON_JSON_SCHEMA, build_user_prompt
from render import render_lesson_html

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "lessons"
MODEL = os.environ.get("LESSON_AGENT_MODEL", "claude-sonnet-5")
MAX_TOOL_TURNS = 8


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


def run_agent(topic: str, unit_key: str, duration: int) -> dict:
    try:
        import anthropic
    except ImportError:
        sys.exit("Missing dependency: run `pip install -r requirements.txt` first.")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in.")

    client = anthropic.Anthropic(api_key=api_key)

    unit = UNITS[unit_key]
    descriptors = descriptors_for_unit(unit_key)
    user_prompt = build_user_prompt(topic, unit["title"], unit["focus"], descriptors, duration)

    tools = [
        {"type": "web_search_20260209", "name": "web_search", "max_uses": 8},
        {
            "name": "emit_lesson",
            "description": "Submit the final, complete lesson content.",
            "input_schema": LESSON_JSON_SCHEMA,
        },
    ]

    messages = [{"role": "user", "content": user_prompt}]

    for _ in range(MAX_TOOL_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=8000,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        emit_call = next(
            (b for b in response.content if b.type == "tool_use" and b.name == "emit_lesson"),
            None,
        )
        if emit_call:
            return emit_call.input

        if response.stop_reason == "pause_turn":
            # web_search is a server-side tool; the API ran its own search
            # loop and hit the per-turn iteration cap. Re-send the same
            # exchange (no synthetic tool_result) so it can keep going.
            messages = [
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": response.content},
            ]
            continue

        # No emit_lesson call and nothing left to resume: nudge it to finish.
        messages.append({"role": "assistant", "content": response.content})
        messages.append(
            {"role": "user", "content": "Please call emit_lesson now with the finished lesson."}
        )

    sys.exit("Agent did not produce a lesson within the allowed turns. Try again or raise MAX_TOOL_TURNS.")


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
    lesson = run_agent(args.topic, args.unit, args.duration)

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
