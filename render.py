"""Renders a lesson JSON object into a self-contained HTML page."""

import html
import json


def _esc(text) -> str:
    return html.escape(str(text)) if text is not None else ""


def _list_items(items) -> str:
    return "\n".join(f"<li>{_esc(item)}</li>" for item in items or [])


def _vocab(entries) -> str:
    rows = []
    for e in entries or []:
        rows.append(
            f"<dt>{_esc(e.get('term'))}</dt><dd>{_esc(e.get('definition'))}</dd>"
        )
    return "\n".join(rows)


def _sources(entries) -> str:
    cards = []
    for e in entries or []:
        cards.append(f"""
        <li class="source-card">
          <a href="{_esc(e.get('url'))}" target="_blank" rel="noopener noreferrer">{_esc(e.get('title'))}</a>
          <span class="publisher">{_esc(e.get('publisher'))}</span>
          <p>{_esc(e.get('summary'))}</p>
        </li>""")
    return "\n".join(cards)


def _sequence(steps) -> str:
    blocks = []
    for i, s in enumerate(steps or [], start=1):
        duration = s.get("duration_minutes")
        duration_html = f'<span class="duration">{_esc(duration)} min</span>' if duration else ""
        blocks.append(f"""
        <div class="step">
          <h3>{i}. {_esc(s.get('step_title'))} {duration_html}</h3>
          <p>{_esc(s.get('instructions'))}</p>
          {"<p class='student-task'><strong>Your task:</strong> " + _esc(s.get('student_task')) + "</p>" if s.get('student_task') else ""}
        </div>""")
    return "\n".join(blocks)


def _questions(items) -> str:
    blocks = []
    for i, q in enumerate(items or [], start=1):
        options_html = ""
        if q.get("type") == "multiple_choice" and q.get("options"):
            options_html = "<ul class='options'>" + "".join(
                f"<li>{_esc(o)}</li>" for o in q["options"]
            ) + "</ul>"
        blocks.append(f"""
        <div class="question">
          <p><strong>Q{i}.</strong> {_esc(q.get('question'))}</p>
          {options_html}
          <details>
            <summary>Show answer</summary>
            <p>{_esc(q.get('answer'))}</p>
          </details>
        </div>""")
    return "\n".join(blocks)


def _descriptors(items) -> str:
    return "\n".join(
        f"<li><code>{_esc(d.get('code'))}</code> {_esc(d.get('text'))}</li>"
        for d in items or []
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{
    --bg: #ffffff; --fg: #1b1f24; --muted: #5b6572; --accent: #1e6f5c;
    --card-bg: #f4f6f5; --border: #e0e4e2;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #14171a; --fg: #e8ecef; --muted: #9aa5ad; --accent: #4fbf9f;
      --card-bg: #1d2226; --border: #2b3136; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    background: var(--bg); color: var(--fg); font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
    max-width: 860px; margin: 0 auto; padding: 2rem 1.25rem 4rem; line-height: 1.55;
  }}
  header {{ border-bottom: 3px solid var(--accent); padding-bottom: 1rem; margin-bottom: 1.5rem; }}
  h1 {{ margin: 0 0 .25rem; font-size: 1.6rem; }}
  .meta {{ color: var(--muted); font-size: .9rem; }}
  h2 {{ margin-top: 2.25rem; border-left: 4px solid var(--accent); padding-left: .6rem; }}
  section {{ margin-bottom: 1.5rem; }}
  .step {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: .75rem; }}
  .step h3 {{ margin-top: 0; display: flex; justify-content: space-between; align-items: baseline; }}
  .duration {{ font-size: .8rem; color: var(--muted); font-weight: normal; }}
  .student-task {{ background: var(--bg); border-left: 3px solid var(--accent); padding: .5rem .75rem; border-radius: 4px; }}
  ul.sources {{ list-style: none; padding: 0; }}
  .source-card {{ border: 1px solid var(--border); border-radius: 8px; padding: .75rem 1rem; margin-bottom: .6rem; }}
  .source-card a {{ font-weight: 600; color: var(--accent); }}
  .source-card .publisher {{ display: block; font-size: .8rem; color: var(--muted); margin: .15rem 0 .4rem; }}
  dl {{ display: grid; grid-template-columns: max-content 1fr; gap: .3rem 1rem; }}
  dt {{ font-weight: 600; }}
  dd {{ margin: 0; color: var(--muted); }}
  .question {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: .9rem 1rem; margin-bottom: .6rem; }}
  .options {{ margin: .4rem 0; }}
  details summary {{ cursor: pointer; color: var(--accent); font-weight: 600; }}
  .badge-row {{ display: flex; flex-wrap: wrap; gap: .4rem; margin: .5rem 0 0; }}
  .badge {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 999px; padding: .15rem .7rem; font-size: .78rem; color: var(--muted); }}
  code {{ background: var(--card-bg); padding: .1rem .35rem; border-radius: 4px; font-size: .85em; }}
  footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border); color: var(--muted); font-size: .8rem; }}
</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <div class="meta">{subject} &middot; {year_level} &middot; {unit} &middot; ~{duration} min</div>
  <div class="badge-row">{descriptor_badges}</div>
</header>

<section>
  <h2>Learning intentions</h2>
  <ul>{learning_intentions}</ul>
</section>

<section>
  <h2>Success criteria</h2>
  <ul>{success_criteria}</ul>
</section>

<section>
  <h2>Content descriptors covered</h2>
  <ul>{descriptors}</ul>
</section>

{key_vocab_section}

{starter_section}

<section>
  <h2>Lesson sequence</h2>
  {sequence}
</section>

<section>
  <h2>Sources used in this lesson</h2>
  <ul class="sources">{sources}</ul>
</section>

{differentiation_section}

<section>
  <h2>Check your understanding</h2>
  {questions}
</section>

{exit_ticket_section}

{teacher_notes_section}

<footer>
  Generated with a Claude-based lesson-research agent for South Australian Year 7-10 HASS.
  Review all sourced material and answers before classroom use.
</footer>
</body>
</html>
"""


def render_lesson_html(lesson: dict) -> str:
    descriptor_badges = "".join(
        f"<span class='badge'>{_esc(d.get('code'))}</span>"
        for d in lesson.get("content_descriptors", [])
    )

    key_vocab_section = ""
    if lesson.get("key_vocabulary"):
        key_vocab_section = f"""<section>
  <h2>Key vocabulary</h2>
  <dl>{_vocab(lesson.get('key_vocabulary'))}</dl>
</section>"""

    starter_section = ""
    if lesson.get("starter_activity"):
        starter_section = f"""<section>
  <h2>Starter activity</h2>
  <p>{_esc(lesson.get('starter_activity'))}</p>
</section>"""

    differentiation_section = ""
    diff = lesson.get("differentiation") or {}
    if diff.get("support") or diff.get("extension"):
        differentiation_section = f"""<section>
  <h2>Differentiation</h2>
  {"<p><strong>Support:</strong> " + _esc(diff.get('support')) + "</p>" if diff.get('support') else ""}
  {"<p><strong>Extension:</strong> " + _esc(diff.get('extension')) + "</p>" if diff.get('extension') else ""}
</section>"""

    exit_ticket_section = ""
    if lesson.get("exit_ticket"):
        exit_ticket_section = f"""<section>
  <h2>Exit ticket</h2>
  <p>{_esc(lesson.get('exit_ticket'))}</p>
</section>"""

    teacher_notes_section = ""
    if lesson.get("teacher_notes"):
        teacher_notes_section = f"""<section>
  <h2>Teacher notes</h2>
  <p>{_esc(lesson.get('teacher_notes'))}</p>
</section>"""

    return TEMPLATE.format(
        title=_esc(lesson.get("title", "Untitled lesson")),
        subject=_esc(lesson.get("subject", "HASS")),
        year_level=_esc(lesson.get("year_level", "")),
        unit=_esc(lesson.get("unit", "")),
        duration=_esc(lesson.get("estimated_duration_minutes", "?")),
        descriptor_badges=descriptor_badges,
        learning_intentions=_list_items(lesson.get("learning_intentions")),
        success_criteria=_list_items(lesson.get("success_criteria")),
        descriptors=_descriptors(lesson.get("content_descriptors")),
        key_vocab_section=key_vocab_section,
        starter_section=starter_section,
        sequence=_sequence(lesson.get("lesson_sequence")),
        sources=_sources(lesson.get("sourced_materials")),
        differentiation_section=differentiation_section,
        questions=_questions(lesson.get("formative_assessment")),
        exit_ticket_section=exit_ticket_section,
        teacher_notes_section=teacher_notes_section,
    )


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as f:
        lesson = json.load(f)
    print(render_lesson_html(lesson))
