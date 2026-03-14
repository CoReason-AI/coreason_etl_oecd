from pydantic import BaseModel, Field, HttpUrl


class OECDHealthConfig(BaseModel):
    """Configuration for OECD Health Statistics ingestion."""

    base_url: HttpUrl = Field(
        default=HttpUrl("https://sdmx.oecd.org/public/rest/data/"),
        description="The base SDMX REST API endpoint.",
    )

    datasets: list[str] = Field(
        default=[
            "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
            "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
            "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
        ],
        description="List of target dataset identifiers to ingest.",
    )

    headers: dict[str, str] = Field(
        default={
            "Accept": "text/csv",
            "Accept-Encoding": "gzip",
        },
        description="HTTP headers required for the API requests.",
    )

    timeout: int = Field(
        default=60,
        description="Timeout in seconds for API requests.",
        ge=1,
    )
