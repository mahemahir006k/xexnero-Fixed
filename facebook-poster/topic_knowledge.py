from pathlib import Path
from cache_store import get as cache_get, set as cache_set


KNOWLEDGE_FILE = "company_text.txt"


def load_company_knowledge():

    cached = cache_get("company", "company_text")
    if cached is not None:
        return cached

    path = Path(KNOWLEDGE_FILE)

    if not path.exists():
        raise FileNotFoundError(
            f"{KNOWLEDGE_FILE} not found."
        )

    value = path.read_text(encoding="utf-8")
    cache_set("company", "company_text", value)
    return value


def get_topic_knowledge(topic):

    knowledge = load_company_knowledge()

    topic_keywords = {

    "SEO": [
        "seo",
        "search engine optimization",
        "google ranking",
        "organic traffic",
        "keyword research",
        "on-page",
        "technical seo",
        "backlink"
    ],

    "Local SEO": [
        "local seo",
        "google business profile",
        "google maps",
        "local search",
        "near me",
        "local ranking"
    ],

    "Google Ads": [
        "google ads",
        "ppc",
        "paid search",
        "pay per click",
        "search ads",
        "display ads",
        "shopping ads",
        "youtube ads"
    ],

    "Social Media Marketing": [
        "social media",
        "facebook",
        "instagram",
        "linkedin",
        "social media marketing",
        "reels",
        "stories",
        "engagement"
    ],

    "Website Development": [
        "website",
        "web development",
        "web design",
        "e-commerce",
        "mobile-first",
        "core web vitals",
        "responsive",
        "hosting"
    ],

    "Branding": [
        "branding",
        "brand identity",
        "logo",
        "brand strategy",
        "visual identity",
        "brand guidelines"
    ],

    "Content Marketing": [
        "content marketing",
        "content writing",
        "seo content",
        "blog",
        "copywriting",
        "landing page",
        "content strategy"
    ],

    "Digital Marketing": [
        "digital marketing",
        "online marketing",
        "lead generation",
        "conversion",
        "digital growth"
    ]
}

    keywords = topic_keywords.get(
        topic,
        [topic.lower()]
    )

    sections = knowledge.split("\n\n")

    relevant_sections = []

    for section in sections:

        section_lower = section.lower()

        if any(
            keyword.lower() in section_lower
            for keyword in keywords
        ):
            relevant_sections.append(section)

    if not relevant_sections:

        return knowledge[:8000]

    return "\n\n".join(
        relevant_sections
    )