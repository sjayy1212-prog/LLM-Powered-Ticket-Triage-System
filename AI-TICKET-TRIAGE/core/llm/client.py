from openai import OpenAI
from loguru import logger
from config.settings import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


def call_llm(system_prompt: str, user_prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=800,
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        logger.debug(f"LLM response ({resp.usage.total_tokens} tokens): {content[:200]}")
        return content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise