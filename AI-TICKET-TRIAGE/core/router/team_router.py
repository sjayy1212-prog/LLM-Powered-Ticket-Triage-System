from config.constants import TicketCategory, UrgencyLevel, TEAM_ROUTING, CRITICAL_KEYWORDS, HIGH_PRIORITY_KEYWORDS


def route_to_team(category: str) -> str:
    try:
        cat_enum = TicketCategory(category)
        return TEAM_ROUTING.get(cat_enum, "General Support")
    except ValueError:
        return "General Support"


def apply_urgency_overrides(text: str, llm_urgency: str) -> str:
    text_lower = text.lower()

    for kw in CRITICAL_KEYWORDS:
        if kw in text_lower:
            return UrgencyLevel.CRITICAL.value

    if llm_urgency in (UrgencyLevel.CRITICAL.value, UrgencyLevel.HIGH.value):
        return llm_urgency

    for kw in HIGH_PRIORITY_KEYWORDS:
        if kw in text_lower:
            return UrgencyLevel.HIGH.value

    return llm_urgency