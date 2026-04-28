from datetime import datetime, timezone

from pydantic import BaseModel, Field


class LogFeatures(BaseModel):
    """Optional numeric features used by the analysis pipeline."""

    request_rate_1m: int = Field(default=0, ge=0)
    error_rate_1m: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )
    payload_size_bytes: int = Field(default=0, ge=0)
    response_time_ms: int = Field(default=0, ge=0)
    path_depth: int = Field(default=0, ge=0)


class AnalyzeRequest(BaseModel):
    """
    Input payload for the analysis API.

    `features` is optional on purpose:
    - for now, it can be used for internal testing and prototyping
    - later, the server can derive features inside
      services/feature_engineering.py
    """

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    client_ip: str = Field(..., example="192.168.1.1")
    endpoint: str = Field(..., example="/api/v1/login")
    method: str = Field(default="POST", example="POST")
    status_code: int | None = Field(
        default=None,
        ge=100,
        le=599,
        example=401,
    )
    user_agent: str | None = Field(
        default=None,
        example="Mozilla/5.0",
    )
    features: LogFeatures | None = None

    @property
    def path(self) -> str:
        return self.endpoint
