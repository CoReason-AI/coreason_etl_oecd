# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

from pydantic import BaseModel, Field, HttpUrl


class OECDDatasetConfig(BaseModel):
    dataset_id: str = Field(..., description="The OECD SDMX dataset ID")
    name: str = Field(..., description="Human-readable name of the dataset")


class OECDApiConfig(BaseModel):
    base_url: HttpUrl = Field(
        default=HttpUrl("https://sdmx.oecd.org/public/rest/data/"),
        description="The base REST API endpoint for OECD SDMX",
    )
    datasets: list[OECDDatasetConfig] = Field(
        default=[
            OECDDatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
                name="Health Expenditure",
            ),
            OECDDatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
                name="Provider Resources",
            ),
            OECDDatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
                name="Healthcare Utilisation",
            ),
        ],
        description="Target OECD datasets to ingest",
    )
    timeout_seconds: int = Field(default=300, description="HTTP request timeout in seconds")
    max_retries: int = Field(default=5, description="Maximum number of HTTP retries")
