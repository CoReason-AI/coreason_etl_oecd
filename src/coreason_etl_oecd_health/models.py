# Copyright (c) CoReason, Inc.
# This software is released under the Prosperity Public License 3.0.


from pydantic import BaseModel, Field, HttpUrl


class OecdEndpointConfig(BaseModel):
    """Configuration for an OECD SDMX endpoint."""

    dataset_id: str = Field(
        ...,
        description="The dataset identifier from OECD SDMX, e.g., 'OECD.ELS.HD,DSD_SHA@DF_SHA,1.0'",
    )
    url: HttpUrl = Field(
        ...,
        description="The full SDMX REST API URL for the dataset endpoint.",
    )
    description: str = Field(
        ...,
        description="A human-readable description of the dataset (e.g., 'Health Expenditure').",
    )


class OecdApiConfig(BaseModel):
    """Global configuration for the OECD Health API."""

    base_url: HttpUrl = Field(
        ...,
        description="The base URL for the OECD SDMX REST API.",
    )
    endpoints: list[OecdEndpointConfig] = Field(
        ...,
        description="List of configured dataset endpoints to ingest.",
    )
