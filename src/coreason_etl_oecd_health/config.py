"""
Copyright (c) CoReason, Inc.
This software is released under the Prosperity Public License 3.0.
"""

from pydantic import BaseModel, Field, HttpUrl


class DatasetConfig(BaseModel):
    """Configuration for an individual OECD SDMX dataset."""

    dataset_id: str = Field(..., description="The SDMX identifier for the dataset")
    description: str = Field(..., description="A human-readable description of the dataset")


class OECDConfig(BaseModel):
    """Global configuration for the OECD Health Statistics ingestion pipeline."""

    base_endpoint: HttpUrl = Field(
        default=HttpUrl("https://sdmx.oecd.org/public/rest/data/"),
        description="The base URL for the OECD SDMX REST API",
    )
    datasets: list[DatasetConfig] = Field(
        default=[
            DatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
                description="Health Expenditure",
            ),
            DatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
                description="Provider Resources",
            ),
            DatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
                description="Healthcare Utilisation",
            ),
        ],
        description="List of datasets to be ingested",
    )
