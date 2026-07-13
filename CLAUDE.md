# CLAUDE.md

Permanent conventions for the HASS Online Learning Program. This file is the
source of truth for how this project is built — read it before making
changes. `PLAN.md` tracks current status and what's next; this file records
the rules that don't change lesson to lesson.

## What this is

Interactive online HASS lessons for Seaford Secondary College, Years 7–10.
Used in-lesson and for homework. Hosted on GitHub Pages. Built and maintained
by the classroom teacher, one lesson at a time.

## Architecture

- Plain HTML/CSS/JS only. **No frameworks, no build tools, no npm, no
  bundlers.** Everything must run by opening the file in a browser or via
  GitHub Pages with zero build step.
- Each lesson is **one self-contained HTML file**. It may link to the shared
  `/assets/css/main.css` and `/assets/js/lesson.js`, but should not depend on
  anything else external (except Google Fonts and plain-link YouTube URLs).
- Navigation is a strict drill-down, never skipped:
  `index.html` (home, lists year levels) → `/year{N}/index.html` (lists
  units) → `/year{N}/{unit-slug}/index.html` (lists lessons) →
  `/year{N}/{unit-slug}/lesson{n}.html`.
- One folder per unit, e.g. `/year9/geo-interconnections/`. Unit slugs are
  lowercase-kebab-case and descriptive, not curriculum codes.
- Lesson files are named `lesson1.html`, `lesson2.html`, etc. within their
  unit folder.
- Must work on laptops and phones — every page and every lesson component is
  responsive.

## Design system — "Seaford 2025" palette

| Role | Colour | Hex |
|---|---|---|
| Primary | Teal | `#013148` |
| Accent | Lime | `#BDD675` |
| Accent | Coral | `#F46E63` |
| Accent | Pink | `#F38C9F` |
| Accent | Sky | `#C0E7F8` |
| Accent | Sage | `#7AC698` |

- Fonts via Google Fonts: **DM Serif Display** for headings, **Inter** for
  body text. Both loaded in every page's `<head>`.
- Headings use a **left accent bar with a pale wash background** — never a
  solid fill. E.g. a lime-washed box with a solid lime bar on the left edge,
  teal text. This is the signature look; don't replace it with solid-colour
  banners or cards.
- Colour usage: coral = incorrect/needs another look, lime = correct/success,
  sky/sage/pink = section or tab differentiation, teal = primary text/chrome.
- All shared design tokens (CSS custom properties) and components live in
  `/assets/css/main.css`. Don't hardcode colours or fonts in individual
  lesson files — use the shared classes/variables so a palette change is a
  one-file edit.

## Lesson pattern

Every lesson follows the same interaction pattern, implemented via the shared
`/assets/js/lesson.js`:

1. **Tabbed sections** — a lesson is broken into tabs (e.g. Predict,
   Investigate, Explain, Reveal), not one long scroll.
2. **Predict → Investigate → Explain (CER) → Reveal** structure:
   - *Predict*: a quick prediction/prior-knowledge prompt before the content.
   - *Investigate*: the source material/activity for that lesson section.
   - *Explain*: a Claim–Evidence–Reasoning (CER) written response.
   - *Reveal*: model answer / teacher commentary, **locked until the student
     has interacted** with the preceding step (e.g. submitted a prediction or
     written a CER response) — reveals must never be visible by default or
     freely skippable.
3. **CER textareas have paste disabled** (`onpaste="return false"` or
   equivalent) — students must type their own reasoning.
4. **Multiple choice is auto-marked**, with lime styling for correct and
   coral styling for incorrect feedback, using the shared pale-wash-with-bar
   treatment.
5. **All student responses auto-save to `localStorage`** as they're entered,
   keyed uniquely per lesson/field so answers persist across visits/devices-
   is not required (per-browser only) but must survive refresh/reopen.
6. Every lesson has a **"Download my answers"** button that exports the
   student's saved responses (e.g. as a `.txt` or `.json` file) so they can
   submit or keep a copy.
7. **YouTube is linked, never embedded.** Use plain `<a>` links to YouTube
   URLs — no `<iframe>` embeds. The school firewall blocks embedded YouTube.

## Content rules

- **Aboriginal and Torres Strait Islander content must be substantive and
  specifically attributed** — name the actual peoples/Country/community
  relevant to the content, never generic or token references. Do not
  homogenise diverse Aboriginal and Torres Strait Islander peoples,
  perspectives or Countries into a single undifferentiated reference.
- **Australian spelling throughout** (organise, colour, analyse, program vs.
  programme per Australian convention, etc.) — in content, UI copy, and code
  comments/strings that are user-facing.
- **Every interactive element must be answerable from the lesson's own
  content.** Predictions, CER responses and MCQs must be groundable in what's
  provided in that lesson (readings, sources, videos linked) — never require
  outside research or general knowledge the lesson didn't supply.

## Building lessons

Structure comes first; lesson content is built **one lesson at a time**,
supplied by the teacher. Don't pre-write or invent lesson content ahead of
being given it — scaffold the shell (tabs, predict/investigate/explain/
reveal, MCQ/CER components wired to the shared JS) and wait for real content
before filling it in. See `PLAN.md` for current build status.

## Current unit

Year 9 Geography — **Geographies of Interconnections (Tourism)**, 5 lessons,
in `/year9/geo-interconnections/`.
