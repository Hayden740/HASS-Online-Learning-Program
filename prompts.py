"""Prompt construction for the lesson-generation agent."""

TRUSTED_DOMAIN_HINT = """
Strongly prefer sourcing material from reputable, age-appropriate, and
freely-accessible sites, for example: government and statutory bodies
(.gov.au, abs.gov.au, csiro.au, ga.gov.au, bom.gov.au, mdba.gov.au,
environment.gov.au), international bodies (fao.org, un.org, worldbank.org,
noaa.gov, nasa.gov), respected education/media outlets (abc.net.au including
ABC Education, natgeo.com/education, bbc.co.uk/bitesize), universities
(.edu.au), and NGOs with a strong reputation for accuracy (e.g. UNICEF,
WWF, Red Cross). Avoid paywalled articles, forums, unverified blogs, opinion
pieces presented as fact, and anything not suitable for a 14-15 year old
audience. Every factual claim sourced from the web must be attributed with a
title, publisher and URL in the final output.
"""

SYSTEM_PROMPT = f"""You are a curriculum designer and researcher who builds
online HASS (Humanities and Social Sciences) lessons for Year 7-10 students
in South Australian schools, which follow the Australian Curriculum v9.

You are working on Year 9 Geography. You have access to a web_search tool -
use it to find current, accurate, age-appropriate source material before
writing the lesson. Do not rely solely on prior knowledge for facts, figures,
or case studies; verify them via search and cite them.

{TRUSTED_DOMAIN_HINT}

Write for a mixed-ability Year 9 class (typically 14-15 years old). Use
plain, direct language, define technical terms the first time they appear,
and make the lesson usable for independent online/remote study as well as
in a classroom.

When you have finished researching, call the `emit_lesson` tool exactly once
with the complete, final lesson content as structured JSON. Do not include
any other commentary in your final turn.
"""

LESSON_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "year_level": {"type": "string"},
        "subject": {"type": "string"},
        "unit": {"type": "string"},
        "content_descriptors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["code", "text"],
            },
        },
        "estimated_duration_minutes": {"type": "integer"},
        "learning_intentions": {"type": "array", "items": {"type": "string"}},
        "success_criteria": {"type": "array", "items": {"type": "string"}},
        "key_vocabulary": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "term": {"type": "string"},
                    "definition": {"type": "string"},
                },
                "required": ["term", "definition"],
            },
        },
        "starter_activity": {"type": "string"},
        "sourced_materials": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "publisher": {"type": "string"},
                    "url": {"type": "string"},
                    "summary": {
                        "type": "string",
                        "description": "1-3 sentence summary of what this source contributes and why it's used, written for students",
                    },
                },
                "required": ["title", "publisher", "url", "summary"],
            },
        },
        "lesson_sequence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "step_title": {"type": "string"},
                    "duration_minutes": {"type": "integer"},
                    "instructions": {"type": "string"},
                    "student_task": {"type": "string"},
                },
                "required": ["step_title", "instructions"],
            },
        },
        "differentiation": {
            "type": "object",
            "properties": {
                "support": {"type": "string"},
                "extension": {"type": "string"},
            },
        },
        "formative_assessment": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "type": {"type": "string", "enum": ["multiple_choice", "short_answer"]},
                    "options": {"type": "array", "items": {"type": "string"}},
                    "answer": {"type": "string"},
                },
                "required": ["question", "type", "answer"],
            },
        },
        "exit_ticket": {"type": "string"},
        "teacher_notes": {"type": "string"},
    },
    "required": [
        "title",
        "year_level",
        "subject",
        "content_descriptors",
        "learning_intentions",
        "success_criteria",
        "sourced_materials",
        "lesson_sequence",
        "formative_assessment",
    ],
}


def build_user_prompt(topic: str, unit_title: str, unit_focus: str, descriptors, duration: int) -> str:
    descriptor_lines = "\n".join(f"- [{d['code']}] {d['text']}" for d in descriptors)
    return f"""Build one complete online lesson on the following topic:

Topic: {topic}
Unit: {unit_title} -- {unit_focus}
Target duration: {duration} minutes

Relevant content descriptors to draw on (use the ones that genuinely fit;
you don't need to force every single one in):
{descriptor_lines}

Research current, real sources before writing. Include at least 3 distinct
sourced materials with working URLs. Then call emit_lesson with the finished
lesson."""
