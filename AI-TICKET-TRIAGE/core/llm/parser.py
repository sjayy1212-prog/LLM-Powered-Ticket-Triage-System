import json
import re
from loguru import logger
from config.constants import TicketCategory, UrgencyLevel


def parse_triage_response(raw: str) -> dict:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse LLM JSON: {raw[:300]}")
        return _default_result()

    cat = data.get("category", "general").lower().strip()
    valid_cats = [c.value for c in TicketCategory]
    if cat not in valid_cats:
        cat = "general"

    urg = data.get("urgency", "normal").lower().strip()
    valid_urgs = [u.value for u in UrgencyLevel]
    if urg not in valid_urgs:
        urg = "normal"

    conf = data.get("confidence", 0.5)
    if not isinstance(conf, (int, float)) or not (0 <= conf <= 1):
        conf = 0.5

    return {
        "category": cat,
        "urgency": urg,
        "suggested_response": data.get("suggested_response", ""),
        "confidence": round(conf, 3),
        "reasoning": data.get("reasoning", ""),
    }


def _default_result() -> dict:
    return {
        "category": "general",
        "urgency": "normal",
        "suggested_response": "Thank you for contacting us. We have received your request and a team member will follow up shortly.",
        "confidence": 0.0,
        "reasoning": "Fallback - LLM response could not be parsed.",
    }