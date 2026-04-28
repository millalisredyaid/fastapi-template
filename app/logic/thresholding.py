from dataclasses import dataclass

from app.core.config import ANOMALY_THRESHOLD, HIGH_THRESHOLD, MEDIUM_THRESHOLD
from app.schemas.response import SeverityLevel


@dataclass(frozen=True)
class ThresholdConfig:
    anomaly_threshold: float = ANOMALY_THRESHOLD
    medium_threshold: float = MEDIUM_THRESHOLD
    high_threshold: float = HIGH_THRESHOLD


@dataclass(frozen=True)
class ThresholdDecision:
    threshold: float
    is_anomaly: bool
    severity: SeverityLevel


DEFAULT_THRESHOLD_CONFIG = ThresholdConfig()


def get_threshold_config() -> ThresholdConfig:
    return DEFAULT_THRESHOLD_CONFIG


def is_anomaly(score: float, config: ThresholdConfig | None = None) -> bool:
    config = config or get_threshold_config()
    return score < config.anomaly_threshold


def determine_severity(
    score: float,
    config: ThresholdConfig | None = None,
) -> SeverityLevel:
    config = config or get_threshold_config()

    if score < config.high_threshold:
        return SeverityLevel.high
    if score < config.medium_threshold:
        return SeverityLevel.medium
    return SeverityLevel.low


def evaluate_thresholds(
    score: float,
    config: ThresholdConfig | None = None,
) -> ThresholdDecision:
    config = config or get_threshold_config()

    return ThresholdDecision(
        threshold=config.anomaly_threshold,
        is_anomaly=is_anomaly(score, config),
        severity=determine_severity(score, config),
    )
