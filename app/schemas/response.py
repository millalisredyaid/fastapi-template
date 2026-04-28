from enum import Enum

from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class RecommendedAction(str, Enum):
    allow = "allow"
    alert = "alert"
    block = "block"


class AnalyzeResponse(BaseModel):
    """Final response returned by the analysis API."""
    is_anomaly: bool
    anomaly_score: float
    threshold: float
    severity: SeverityLevel
    action: RecommendedAction
    triggered_rules: list[str] = Field(default_factory=list)
    received_path: str | None = None
    details: str | None = None
