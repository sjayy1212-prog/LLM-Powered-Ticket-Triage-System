import json
import time
from pathlib import Path
from sklearn.metrics import classification_report
from loguru import logger
from core.pipeline import run_triage


def load_test_data(path: str = "data/sample_tickets.json") -> list[dict]:
    return json.loads(Path(path).read_text())


def run_batch_eval(test_data: list[dict]) -> dict:
    y_true_cat, y_pred_cat = [], []
    y_true_urg, y_pred_urg = [], []
    latencies = []
    confidences = []

    for item in test_data:
        start = time.perf_counter()
        result = run_triage(subject=None, body=item["text"])
        elapsed = (time.perf_counter() - start) * 1000

        y_true_cat.append(item["category"])
        y_pred_cat.append(result["category"])
        y_true_urg.append(item["urgency"])
        y_pred_urg.append(result["urgency"])
        latencies.append(elapsed)
        confidences.append(result["confidence"])

        logger.info(
            f"  [{item['category']} -> {result['category']}] "
            f"[{item['urgency']} -> {result['urgency']}] "
            f"conf={result['confidence']:.2f} time={elapsed:.0f}ms"
        )

    cat_report = classification_report(y_true_cat, y_pred_cat, output_dict=True, zero_division=0)
    urg_report = classification_report(y_true_urg, y_pred_urg, output_dict=True, zero_division=0)

    return {
        "category_accuracy": cat_report["accuracy"],
        "urgency_accuracy": urg_report["accuracy"],
        "avg_latency_ms": sum(latencies) / len(latencies),
        "avg_confidence": sum(confidences) / len(confidences),
        "total_evaluated": len(test_data),
    }


if __name__ == "__main__":
    data = load_test_data()
    logger.info(f"Running evaluation on {len(data)} tickets...")
    results = run_batch_eval(data)
    logger.info(f"Category Accuracy: {results['category_accuracy']:.1%}")
    logger.info(f"Urgency Accuracy:  {results['urgency_accuracy']:.1%}")
    logger.info(f"Avg Confidence:    {results['avg_confidence']:.2f}")
    logger.info(f"Avg Latency:       {results['avg_latency_ms']:.0f}ms")