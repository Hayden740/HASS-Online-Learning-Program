#!/usr/bin/env python3
"""
Point-and-click web form for the HASS lesson-research agent.

Run with:
    python app.py

Then open http://127.0.0.1:5000 in a browser. Requires ANTHROPIC_API_KEY to
be set (see .env.example) and the dependencies in requirements.txt installed.
"""

import os
import sys
import webbrowser
from pathlib import Path
from threading import Timer

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from flask import Flask, render_template, request  # noqa: E402

from agent import AgentError, run_agent  # noqa: E402
from curriculum import UNITS  # noqa: E402
from render import render_lesson_html  # noqa: E402

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))


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


load_env_file()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", units=UNITS, error=None)


@app.route("/generate", methods=["POST"])
def generate():
    topic = request.form.get("topic", "").strip()
    unit_key = request.form.get("unit", "biomes-and-food-security")
    duration = request.form.get("duration", "70")

    try:
        duration = int(duration)
    except ValueError:
        duration = 70

    if not topic:
        return render_template("index.html", units=UNITS, error="Please enter a topic."), 400

    if unit_key not in UNITS:
        return render_template("index.html", units=UNITS, error="Unknown unit selected."), 400

    try:
        lesson = run_agent(topic, unit_key, duration)
    except AgentError as e:
        return render_template("index.html", units=UNITS, error=str(e)), 500

    return render_lesson_html(lesson)


def open_browser():
    webbrowser.open(f"http://127.0.0.1:{PORT}")


if __name__ == "__main__":
    Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=PORT, debug=False)
