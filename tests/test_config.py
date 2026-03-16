# Copyright (c) 2026 CoReason, Inc.
# This software is released under the Prosperity Public License 3.0.
# For full license details, see the LICENSE file in the project root.

from coreason_etl_oecd_health.config import OECDHealthConfig


def test_oecd_health_config_defaults() -> None:
    """Test that the default configuration is initialized correctly."""
    config = OECDHealthConfig()

    # Asserting default base endpoint
    assert config.base_endpoint == "https://sdmx.oecd.org/public/rest/data/"

    # Asserting default target datasets
    expected_datasets = [
        "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
        "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
        "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
    ]
    assert config.target_datasets == expected_datasets

    # Asserting required headers and chunking logic
    assert config.accept_header == "text/csv"
    assert config.chunk_by == "TIME_PERIOD"


def test_oecd_health_config_custom_values() -> None:
    """Test that custom configuration values can be provided."""
    custom_config = OECDHealthConfig(
        base_endpoint="https://custom.api.org/data/",
        target_datasets=["CUSTOM_DATASET"],
        accept_header="application/json",
        chunk_by="COUNTRY",
    )

    assert custom_config.base_endpoint == "https://custom.api.org/data/"
    assert custom_config.target_datasets == ["CUSTOM_DATASET"]
    assert custom_config.accept_header == "application/json"
    assert custom_config.chunk_by == "COUNTRY"
