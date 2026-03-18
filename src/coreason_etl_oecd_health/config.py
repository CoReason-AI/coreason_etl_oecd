# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0


from pydantic import BaseModel, Field, HttpUrl


class OecdDatasetConfig(BaseModel):
    dataset_id: str = Field(..., description="The ID of the dataset to be ingested")
    description: str = Field(..., description="Human-readable description of the dataset")


class OecdApiConfig(BaseModel):
    base_url: HttpUrl = Field(
        default=HttpUrl("https://sdmx.oecd.org/public/rest/data/"),
        description="The base endpoint for the OECD SDMX REST API",
    )
    datasets: list[OecdDatasetConfig] = Field(
        default=[
            OecdDatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
                description="Health Expenditure",
            ),
            OecdDatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
                description="Provider Resources",
            ),
            OecdDatasetConfig(
                dataset_id="OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
                description="Healthcare Utilisation",
            ),
        ],
        description="List of target datasets to ingest from the API",
    )
