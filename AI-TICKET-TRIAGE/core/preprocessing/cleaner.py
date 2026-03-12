import re


def clean_ticket_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[!]{2,}", "!", text)
    text = re.sub(r"[?]{2,}", "?", text)
    for marker in ["--", "Sent from my", "Best regards", "Kind regards"]:
        idx = text.find(marker)
        if idx > 50:
            text = text[:idx].strip()
    return text


def combine_subject_body(subject: str | None, body: str) -> str:
    if subject:
        return f"Subject: {subject}\n\n{body}"
    return body