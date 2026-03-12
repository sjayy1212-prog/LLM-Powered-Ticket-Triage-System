from core.vectorstore.store import vector_store


def retrieve_similar_tickets(query: str, k: int = 3) -> list[dict]:
    results = vector_store.search(query, k=k)
    return [r for r in results if r.get("type") == "ticket"]


def retrieve_policy_context(query: str, k: int = 2) -> list[dict]:
    results = vector_store.search(query, k=k)
    return [r for r in results if r.get("type") == "policy"]