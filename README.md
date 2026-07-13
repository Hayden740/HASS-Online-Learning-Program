# HASS Online Learning Program

Interactive online HASS lessons for Seaford Secondary College, Years 7–10.
Used in-lesson and for homework. Plain HTML/CSS/JS, no build step, hosted on
GitHub Pages.

See `CLAUDE.md` for the permanent conventions (design system, lesson pattern,
content rules) and `PLAN.md` for current build status and next steps.

## Structure

```
index.html                              home — pick a year level
year{7,8,9,10}/index.html                year page — pick a unit
year{N}/{unit-slug}/index.html            unit page — pick a lesson
year{N}/{unit-slug}/lesson{n}.html         the lesson itself
assets/css/main.css                       shared design system
assets/js/lesson.js                        shared lesson behaviour
```

## Running locally

No build step — just open `index.html` in a browser, or serve the folder
with any static file server, e.g.:

```bash
python3 -m http.server
```

## Current unit

Year 9 Geography — Geographies of Interconnections (Tourism), 5 lessons, in
`/year9/geo-interconnections/`. Structure is scaffolded; lesson content is
being added one lesson at a time.
