from pydantic import BaseModel, Field, HttpUrl, field_validator


class OECDHealthConfig(BaseModel):
    """Configuration model for the OECD Health Statistics ETL pipeline."""

    base_endpoint: HttpUrl = Field(
        default=HttpUrl("https://sdmx.oecd.org/public/rest/data/"),
        description="The base endpoint for the OECD SDMX REST API.",
    )
    target_datasets: list[str] = Field(
        default=[
            "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
            "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
            "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
        ],
        description="List of OECD dataset IDs to ingest.",
    )
    timeout: int = Field(
        default=60,
        description="Timeout in seconds for API requests.",
        ge=1,
    )

    @field_validator("target_datasets")
    @classmethod
    def validate_target_datasets(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("target_datasets cannot be empty")
        for dataset in v:
            if not dataset.strip():
                raise ValueError("dataset IDs cannot be empty strings")
        return v
