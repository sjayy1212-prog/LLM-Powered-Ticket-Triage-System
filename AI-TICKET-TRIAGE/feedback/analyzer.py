from collections import Counter
from app.db.database import SessionLocal
from app.db import crud
from loguru import logger


def analyze_corrections() -> dict:
    db = SessionLocal()
    try:
        feedback_list = crud.get_all_feedback(db, limit=500)
    finally:
        db.close()

    if not feedback_list:
        return {"message": "No feedback yet"}

    cat_errors = Counter()
    urg_errors = Counter()
    total_with_cat_fix = 0
    total_with_urg_fix = 0

    for fb in feedback_list:
        if fb.corrected_category and fb.corrected_category != fb.original_category:
            cat_errors[(fb.original_category, fb.corrected_category)] += 1
            total_with_cat_fix += 1
        if fb.corrected_urgency and fb.corrected_urgency != fb.original_urgency:
            urg_errors[(fb.original_urgency, fb.corrected_urgency)] += 1
            total_with_urg_fix += 1

    return {
        "total_feedback": len(feedback_list),
        "category_corrections": total_with_cat_fix,
        "urgency_corrections": total_with_urg_fix,
        "top_category_errors": [
            {"from": k[0], "to": k[1], "count": v}
            for k, v in cat_errors.most_common(10)
        ],
        "top_urgency_errors": [
            {"from": k[0], "to": k[1], "count": v}
            for k, v in urg_errors.most_common(10)
        ],
    }


if __name__ == "__main__":
    import json
    result = analyze_corrections()
    print(json.dumps(result, indent=2))