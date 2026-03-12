import json
from pathlib import Path
from loguru import logger
from core.vectorstore.store import vector_store


def index_sample_tickets():
    path = Path("data/sample_tickets.json")
    tickets = json.loads(path.read_text())
    texts, metas = [], []
    for i, t in enumerate(tickets):
        texts.append(t["text"])
        metas.append({
            "type": "ticket",
            "text": t["text"],
            "category": t["category"],
            "urgency": t["urgency"],
            "response": t["response"],
            "id": f"sample_{i}",
        })
    logger.info(f"Indexing {len(texts)} sample tickets...")
    vector_store.add_batch(texts, metas)


def index_policy_docs():
    policy_dir = Path("data/policies")
    if not policy_dir.exists():
        logger.warning("No policies directory found, skipping.")
        return
    for md_file in policy_dir.glob("*.md"):
        text = md_file.read_text()
        meta = {
            "type": "policy",
            "title": md_file.stem.replace("_", " ").title(),
            "text": text,
            "source": str(md_file),
        }
        vector_store.add(text, meta)
        logger.info(f"Indexed policy: {md_file.name}")


if __name__ == "__main__":
    index_sample_tickets()
    index_policy_docs()
    vector_store.save()
    logger.info("Vector store seeded and saved.")