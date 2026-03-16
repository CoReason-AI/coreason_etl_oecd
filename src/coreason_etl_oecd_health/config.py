# Copyright (c) CoReason, Inc.
# This software is released under the Prosperity Public License 3.0.

from pydantic import BaseModel, Field, HttpUrl


class OECDDatasetConfig(BaseModel):
    """Configuration for a specific OECD dataset."""

    id: str = Field(..., description="The SDMX dataset identifier.")
    description: str = Field(..., description="A human-readable description of the dataset.")
    version: str = Field(default="1.0", description="The dataset version.")


class OECDApiConfig(BaseModel):
    """Configuration for the OECD SDMX API."""

    base_url: HttpUrl = Field(
        default=HttpUrl("https://sdmx.oecd.org/public/rest/data/"),
        description="The base endpoint for the OECD SDMX REST API.",
    )
    datasets: list[OECDDatasetConfig] = Field(
        default_factory=lambda: [
            OECDDatasetConfig(
                id="OECD.ELS.HD,DSD_SHA@DF_SHA",
                description="Health Expenditure",
            ),
            OECDDatasetConfig(
                id="OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC",
                description="Provider Resources",
            ),
            OECDDatasetConfig(
                id="OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC",
                description="Healthcare Utilisation",
            ),
        ],
        description="List of target datasets to ingest.",
    )
