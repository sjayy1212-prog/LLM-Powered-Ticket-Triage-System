from enum import Enum


class TicketCategory(str, Enum):
    BILLING = "billing"
    REFUND = "refund"
    TECHNICAL = "technical"
    FRAUD = "fraud"
    FEATURE_REQUEST = "feature_request"
    ACCOUNT = "account"
    GENERAL = "general"


class UrgencyLevel(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


TEAM_ROUTING = {
    TicketCategory.BILLING: "Billing Team",
    TicketCategory.REFUND: "Billing Team",
    TicketCategory.TECHNICAL: "Engineering",
    TicketCategory.FRAUD: "Risk & Security",
    TicketCategory.FEATURE_REQUEST: "Product",
    TicketCategory.ACCOUNT: "Customer Success",
    TicketCategory.GENERAL: "General Support",
}

CRITICAL_KEYWORDS = [
    "fraud", "unauthorized", "stolen", "hacked",
    "charged twice", "data breach", "legal action",
    "lawsuit", "compromised", "identity theft",
]

HIGH_PRIORITY_KEYWORDS = [
    "urgent", "asap", "immediately", "not working",
    "down", "outage", "broken", "crashed", "blocked",
    "cannot access", "payment failed",
]