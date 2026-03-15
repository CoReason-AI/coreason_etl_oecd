# Copyright (c) 2026 CoReason, Inc.
# This software is released under the Prosperity Public License 3.0.
# For full license details, see the LICENSE file in the project root.

from pydantic import BaseModel, Field


class OECDHealthConfig(BaseModel):
    """Configuration for the OECD Health Statistics extraction."""

    base_endpoint: str = Field(
        default="https://sdmx.oecd.org/public/rest/data/",
        description="The base SDMX REST API endpoint for OECD.",
    )

    target_datasets: list[str] = Field(
        default=[
            "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
            "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
            "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
        ],
        description="List of target datasets to extract from OECD.",
    )

    accept_header: str = Field(
        default="text/csv", description="The Accept header to force CSV format returns."
    )

    chunk_by: str = Field(
        default="TIME_PERIOD",
        description="The dimension to chunk requests by to avoid Gateway Timeouts.",
    )
