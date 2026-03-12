from openai import OpenAI
from config.settings import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


def get_embedding(text: str) -> list[float]:
    resp = client.embeddings.create(
        model=settings.embedding_model,
        input=text,
    )
    return resp.data[0].embedding


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    return [item.embedding for item in resp.data]
