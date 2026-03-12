import time
from loguru import logger
from core.preprocessing.cleaner import clean_ticket_text, combine_subject_body
from core.rag.context_builder import build_context
from core.llm.client import call_llm
from core.llm.prompts import TRIAGE_SYSTEM_PROMPT, build_triage_user_prompt
from core.llm.parser import parse_triage_response
from core.router.team_router import route_to_team, apply_urgency_overrides
from config.settings import get_settings


def run_triage(subject: str | None, body: str) -> dict:
    start = time.perf_counter()

    raw_text = combine_subject_body(subject, body)
    clean_text = clean_ticket_text(raw_text)
    logger.info(f"Processing ticket ({len(clean_text)} chars)")

    context = build_context(clean_text)
    logger.debug(f"RAG context length: {len(context)} chars")

    user_prompt = build_triage_user_prompt(clean_text, context)
    raw_response = call_llm(TRIAGE_SYSTEM_PROMPT, user_prompt)

    parsed = parse_triage_response(raw_response)

    final_urgency = apply_urgency_overrides(clean_text, parsed["urgency"])
    if final_urgency != parsed["urgency"]:
        logger.info(f"Urgency overridden: {parsed['urgency']} -> {final_urgency}")
    parsed["urgency"] = final_urgency

    team = route_to_team(parsed["category"])

    elapsed_ms = (time.perf_counter() - start) * 1000

    result = {
        **parsed,
        "assigned_team": team,
        "processing_time_ms": round(elapsed_ms, 1),
        "model_used": get_settings().llm_model,
    }

    logger.info(
        f"Triage complete: category={result['category']}, "
        f"urgency={result['urgency']}, team={team}, "
        f"confidence={result['confidence']}, time={elapsed_ms:.0f}ms"
    )
    return result