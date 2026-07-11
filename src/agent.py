"""Core agent loop: research a topic and produce a lesson dict.

Shared by the CLI (generate_lesson.py) and the web app (app.py) so there's
one place that talks to the Claude API.
"""

import os

from curriculum import UNITS, descriptors_for_unit
from prompts import SYSTEM_PROMPT, LESSON_JSON_SCHEMA, build_user_prompt

MODEL = os.environ.get("LESSON_AGENT_MODEL", "claude-sonnet-5")
MAX_TOOL_TURNS = 8


class AgentError(Exception):
    """Raised for problems the caller should show to the user, not a stack trace."""


def run_agent(topic: str, unit_key: str, duration: int) -> dict:
    try:
        import anthropic
    except ImportError:
        raise AgentError("Missing dependency: run `pip install -r requirements.txt` first.")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise AgentError("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in.")

    if unit_key not in UNITS:
        raise AgentError(f"Unknown unit: {unit_key!r}")

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

    raise AgentError("Agent did not produce a lesson within the allowed turns. Try again.")
