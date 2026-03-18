# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

from pydantic import BaseModel, Field, HttpUrl


class OecdEndpointConfig(BaseModel):
    """Configuration for an OECD SDMX endpoint."""

    dataset_id: str = Field(
        ...,
        description="The dataset identifier from OECD SDMX, e.g., 'OECD.ELS.HD,DSD_SHA@DF_SHA,1.0'",
    )
    description: str = Field(
        ...,
        description="A human-readable description of the dataset (e.g., 'Health Expenditure').",
    )


class OecdApiConfig(BaseModel):
    """Global configuration for the OECD Health API."""

    base_url: HttpUrl = Field(
        default=HttpUrl("https://sdmx.oecd.org/public/rest/data/"),
        description="The base REST API endpoint for OECD SDMX",
    )
    endpoints: list[OecdEndpointConfig] = Field(
        default=[
            OecdEndpointConfig(
                dataset_id="OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
                description="Health Expenditure",
            ),
            OecdEndpointConfig(
                dataset_id="OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
                description="Provider Resources",
            ),
            OecdEndpointConfig(
                dataset_id="OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
                description="Healthcare Utilisation",
            ),
        ],
        description="Target OECD datasets to ingest",
    )
    timeout_seconds: int = Field(default=300, description="HTTP request timeout in seconds")
    max_retries: int = Field(default=5, description="Maximum number of HTTP retries")
