# PLAN.md

Working plan for the HASS Online Learning Program. This is a living document —
update it as units/lessons are added or the approach changes. Permanent
conventions (design system, code patterns, content rules) live in
`CLAUDE.md`, not here.

## What this is

Interactive HASS lessons for Seaford Secondary College, Years 7–10, built and
maintained by the classroom teacher. Used in-lesson (data projector / student
devices) and set for homework. Hosted on GitHub Pages.

## Architecture

Plain HTML/CSS/JS. No frameworks, no build step, no npm. Every lesson is one
self-contained `.html` file (plus the shared `/assets/css` and `/assets/js`).
Navigation is a strict drill-down:

```
index.html                              (home — pick a year level)
  └── /year{N}/index.html                (year page — pick a unit)
        └── /year{N}/{unit-slug}/index.html   (unit page — pick a lesson)
              └── /year{N}/{unit-slug}/lesson{n}.html  (the lesson)
```

Example: `/year9/geo-interconnections/lesson1.html`.

## Current folder structure (scaffolded, no lesson content yet)

```
index.html
CLAUDE.md
PLAN.md
README.md
assets/
  css/
    main.css        design tokens, layout, typography, tab/reveal/MCQ components
  js/
    lesson.js        shared behaviour: tabs, reveal-locking, paste-disable,
                      MCQ auto-marking, localStorage autosave, download-answers
year7/
  index.html          "units coming soon" placeholder
year8/
  index.html          "units coming soon" placeholder
year9/
  index.html          lists units — currently just Geographies of Interconnections
  geo-interconnections/
    index.html         lists the 5 lessons
    lesson1.html        template shell — awaiting content
    lesson2.html        template shell — awaiting content
    lesson3.html        template shell — awaiting content
    lesson4.html        template shell — awaiting content
    lesson5.html        template shell — awaiting content
year10/
  index.html          "units coming soon" placeholder
```

## First unit

**Year 9 Geography — Geographies of Interconnections (Tourism)**, 5 lessons.
Content supplied by the teacher one lesson at a time. The five `lessonN.html`
files currently contain the standard lesson shell (tabs, predict/investigate/
explain/reveal structure, placeholder MCQ, CER response area) with placeholder
copy marking where real content goes — no real lesson content yet.

## Status

- [x] Repo structure scaffolded
- [x] Design system CSS (palette, fonts, components) in place
- [x] Shared JS behaviour (tabs, reveal-lock, paste-disable, auto-mark,
      autosave, download) in place
- [x] Home → year → unit → lesson navigation wired up
- [ ] Lesson 1 content (Geographies of Interconnections)
- [ ] Lesson 2 content
- [ ] Lesson 3 content
- [ ] Lesson 4 content
- [ ] Lesson 5 content
- [ ] Additional Year 9 Geography units
- [ ] Year 7, 8, 10 units

## Next steps

Build lessons one at a time — teacher supplies content for a lesson, it gets
built into that lesson's HTML file following the pattern in `CLAUDE.md`, then
move to the next lesson. Do not pre-write lesson content speculatively.
