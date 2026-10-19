import os

from pydantic import BaseModel, Field


class Settings(BaseModel):
    jaeger_base_url: str = Field(
        default_factory=lambda: os.getenv(
            "JAEGER_BASE_URL", os.getenv("JAEGER_URL", "http://localhost:16686")
        ),
        description="Base URL of the Jaeger Query / UI service",
    )
    service_api_version: str = Field(
        default_factory=lambda: os.getenv("SERVICE_API_VERSION", "v3"),
        description="API version for services and operations endpoints",
    )
    request_timeout_seconds: float = Field(
        default_factory=lambda: float(os.getenv("JAEGER_TIMEOUT_SECONDS", "10.0")),
        description="Timeout in seconds for HTTP requests to Jaeger",
    )


settings = Settings()
