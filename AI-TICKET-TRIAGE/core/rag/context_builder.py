from core.rag.retriever import retrieve_similar_tickets, retrieve_policy_context


def build_context(ticket_text: str) -> str:
    sections = []

    similar = retrieve_similar_tickets(ticket_text, k=3)
    if similar:
        lines = []
        for i, t in enumerate(similar, 1):
            lines.append(
                f"  {i}. [{t.get('category', '?')}] (urgency: {t.get('urgency', '?')})\n"
                f"     Text: {t.get('text', '')[:200]}\n"
                f"     Response: {t.get('response', '')[:200]}"
            )
        sections.append("SIMILAR PAST TICKETS:\n" + "\n".join(lines))

    policies = retrieve_policy_context(ticket_text, k=2)
    if policies:
        lines = []
        for p in policies:
            lines.append(f"  [{p.get('title', 'Policy')}]: {p.get('text', '')[:400]}")
        sections.append("RELEVANT COMPANY POLICIES:\n" + "\n".join(lines))

    if not sections:
        return "No similar tickets or policies found in knowledge base."

    return "\n\n".join(sections)