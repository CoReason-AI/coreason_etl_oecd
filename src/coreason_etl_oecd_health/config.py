# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OECDApiConfig(BaseSettings):
    """Configuration for the OECD SDMX REST API extraction."""

    base_url: HttpUrl = Field(
        default=HttpUrl("https://sdmx.oecd.org/public/rest/data/"),
        description="The base endpoint for the OECD SDMX REST API.",
    )

    # Target Datasets
    target_datasets: tuple[str, ...] = Field(
        default=(
            "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
            "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
            "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
        ),
        description="List of target OECD SDMX Dataset IDs to extract.",
    )

    # Expected response format
    accept_header: str = Field(
        default="text/csv",
        description="The accept header to force CSV returns.",
    )

    # Required parameters to defend against 504 Gateway Timeouts on large SDMX datasets
    timeout: int = Field(
        default=30,
        ge=30,
        description="HTTP request timeout in seconds. Defends against slow OECD API responses.",
    )

    retry_count: int = Field(
        default=5,
        ge=0,
        description="Maximum number of retries for external HTTP requests.",
    )

    chunk_by_time_period: bool = Field(
        default=True,
        description="Enforce chunking by TIME_PERIOD to prevent 504 Gateway Timeouts.",
    )

    # Deterministic sorting for dataset IDs
    @field_validator("target_datasets", mode="after")
    @classmethod
    def sort_target_datasets(cls, v: tuple[str, ...]) -> tuple[str, ...]:
        """
        AGENT INSTRUCTION: Ensure deterministic sorting of target datasets
        to guarantee consistent hashing and predictable extraction order.
        """
        return tuple(sorted(v))

    model_config = SettingsConfigDict(
        env_prefix="OECD_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
