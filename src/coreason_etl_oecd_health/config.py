# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class OECDConfig(BaseSettings):
    """Configuration for the OECD SDMX REST API extraction."""

    base_endpoint: HttpUrl = Field(
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

    # The maximum number of retry attempts for HTTP requests
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for external HTTP requests.",
    )

    model_config = SettingsConfigDict(
        env_prefix="OECD_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
