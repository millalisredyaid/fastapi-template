import logging

from fastapi import APIRouter

from app.logic.thresholding import evaluate_thresholds
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse, RecommendedAction

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=AnalyzeResponse)
async def analyze_log(request: AnalyzeRequest):
    logger.info(
        "Analyze request received: client_ip=%s endpoint=%s",
        request.client_ip,
        request.endpoint,
    )

    # Placeholder score for now.
    # Later this will be replaced by model inference
    # from services/inference.py.
    dummy_score = -0.22

    decision = evaluate_thresholds(dummy_score)
    triggered_rules = (
        ["threshold_violation"] if decision.is_anomaly else []
    )

    return AnalyzeResponse(
        is_anomaly=decision.is_anomaly,
        anomaly_score=dummy_score,
        threshold=decision.threshold,
        severity=decision.severity,
        action=(
            RecommendedAction.alert
            if decision.is_anomaly
            else RecommendedAction.allow
        ),
        triggered_rules=triggered_rules,
        received_path=request.path,
        details=(
            f"Analysis completed for endpoint={request.endpoint}, "
            f"score={dummy_score}"
        ),
    )
