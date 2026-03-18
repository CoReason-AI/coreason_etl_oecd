# Copyright (c) CoReason, Inc.
# This software is released under the Prosperity Public License 3.0.

from pydantic import BaseModel, Field


class OECDHealthDatasetConfig(BaseModel):
    """Configuration for an OECD Health dataset endpoint."""

    dataset_id: str = Field(..., description="The ID of the dataset to be used internally.")
    sdmx_id: str = Field(..., description="The SDMX identifier for the dataset.")


class OECDHealthConfig(BaseModel):
    """Configuration for the OECD Health data ingestion."""

    base_url: str = Field(
        default="https://sdmx.oecd.org/public/rest/data/",
        description="The base URL for the OECD SDMX REST API.",
    )
    datasets: list[OECDHealthDatasetConfig] = Field(
        default=[
            OECDHealthDatasetConfig(
                dataset_id="health_expenditure", sdmx_id="OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
            ),
            OECDHealthDatasetConfig(
                dataset_id="provider_resources",
                sdmx_id="OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
            ),
            OECDHealthDatasetConfig(
                dataset_id="healthcare_utilisation",
                sdmx_id="OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
            ),
        ],
        description="The list of target datasets to ingest.",
    )
    timeout_seconds: int = Field(default=300, description="Timeout for API requests in seconds.")
    headers: dict[str, str] = Field(
        default={
            "Accept": "text/csv",
            "Accept-Encoding": "gzip",
        },
        description="Mandatory HTTP headers for the OECD API requests.",
    )
