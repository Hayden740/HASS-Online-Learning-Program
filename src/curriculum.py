"""
Reference data for Year 9 Geography, Australian Curriculum v9 (HASS).

South Australian government and Catholic/independent schools teach the
Australian Curriculum v9 for Years 7-10 HASS (there is no separate SA-specific
syllabus for these year levels, unlike SACE at Years 11-12).

Year 9 Geography is organised into two units under "Geographical Knowledge
and Understanding", plus a "Geographical Inquiry and Skills" strand that
applies across both units.

IMPORTANT: The codes and wording below were compiled from training knowledge
and public search-result snippets, NOT scraped live from
https://v9.australiancurriculum.edu.au (that site returns 403 to automated
fetches). Treat CONTENT_DESCRIPTORS as a convenient starting checklist, not
the source of truth -- spot-check codes against the official site or your
school's curriculum documents before reporting against them formally.
"""

UNITS = {
    "biomes-and-food-security": {
        "title": "Biomes and food security",
        "focus": (
            "The biomes of the world, their alteration and significance as a "
            "source of food and fibre, and the environmental challenges and "
            "constraints on expanding food production in the future."
        ),
    },
    "geographies-of-interconnections": {
        "title": "Geographies of interconnections",
        "focus": (
            "How the movement of people, goods, services, ideas, capital and "
            "information has led to expanding networks of connections and "
            "complex interdependencies between places, and the effects of "
            "this interconnection on people and places."
        ),
    },
}

CONTENT_DESCRIPTORS = [
    {
        "code": "AC9HG9K01",
        "unit": "biomes-and-food-security",
        "text": "The distribution and characteristics of biomes as regions with distinctive climates, soils, vegetation and other environmental factors",
    },
    {
        "code": "AC9HG9K02",
        "unit": "biomes-and-food-security",
        "text": "The human alteration of biomes to produce food, industrial materials and fibres, and the use of continents, biotechnology and fishing grounds",
    },
    {
        "code": "AC9HG9K03",
        "unit": "biomes-and-food-security",
        "text": "The effects of biome alteration on food production, and on the biotic environment, including deforestation, land clearing, soil and water degradation, and loss of biodiversity",
    },
    {
        "code": "AC9HG9K04",
        "unit": "biomes-and-food-security",
        "text": "The challenges to food production, including land and water degradation, competing land uses, and climate change, and the food security implications for Australia and the world",
    },
    {
        "code": "AC9HG9K05",
        "unit": "geographies-of-interconnections",
        "text": "The concept of interconnection and how it explains the way people and places are connected to each other through the movement of people, goods, services, ideas, capital and information",
    },
    {
        "code": "AC9HG9K06",
        "unit": "geographies-of-interconnections",
        "text": "The effects of production and consumption of goods on places and environments throughout the world, and the ways people can respond as consumers, citizens and workers",
    },
    {
        "code": "AC9HG9K07",
        "unit": "geographies-of-interconnections",
        "text": "The effects of the alteration or removal of vegetation in an ecosystem on places, environments and human wellbeing, and the interconnections between people, places, environments and their impacts",
    },
    {
        "code": "AC9HG9S01",
        "unit": "skills",
        "text": "Develop geographically significant questions and propose an action plan for an investigation",
    },
    {
        "code": "AC9HG9S02",
        "unit": "skills",
        "text": "Collect, select, record and organise relevant geographical data and information from primary and secondary sources, using ethical protocols",
    },
    {
        "code": "AC9HG9S03",
        "unit": "skills",
        "text": "Represent and analyse spatial patterns, trends and relationships using maps, statistics, graphs and visual representations",
    },
    {
        "code": "AC9HG9S04",
        "unit": "skills",
        "text": "Analyse geographical data and other information to propose explanations for patterns, trends, relationships and anomalies",
    },
    {
        "code": "AC9HG9S05",
        "unit": "skills",
        "text": "Evaluate multiple perspectives and draw reasoned conclusions, and propose action in response to a geographical challenge",
    },
]


def descriptors_for_unit(unit_key: str):
    return [d for d in CONTENT_DESCRIPTORS if d["unit"] in (unit_key, "skills")]


def find_descriptor(code: str):
    for d in CONTENT_DESCRIPTORS:
        if d["code"].lower() == code.lower():
            return d
    return None


def format_checklist() -> str:
    lines = []
    for key, unit in UNITS.items():
        lines.append(f"\n{unit['title']} ({key})")
        lines.append(f"  {unit['focus']}")
        for d in descriptors_for_unit(key):
            if d["unit"] == "skills":
                continue
            lines.append(f"    [{d['code']}] {d['text']}")
    lines.append("\nGeographical Inquiry and Skills (applies to both units)")
    for d in CONTENT_DESCRIPTORS:
        if d["unit"] == "skills":
            lines.append(f"    [{d['code']}] {d['text']}")
    return "\n".join(lines)
