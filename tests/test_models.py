# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

import pytest
from coreason_etl_oecd_health.models import OecdApiConfig, OecdEndpointConfig
from pydantic import ValidationError


def test_oecd_endpoint_config_valid() -> None:
    """Test valid instantiation of OecdEndpointConfig."""
    config = OecdEndpointConfig(
        dataset_id="OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
        description="Health Expenditure",
    )
    assert config.dataset_id == "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
    assert config.description == "Health Expenditure"


def test_oecd_api_config_defaults() -> None:
    """Test valid instantiation of OecdApiConfig with defaults."""
    api_config = OecdApiConfig()

    assert str(api_config.base_url) == "https://sdmx.oecd.org/public/rest/data/"
    assert len(api_config.endpoints) == 3
    assert api_config.endpoints[0].dataset_id == "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
    assert api_config.endpoints[1].dataset_id == "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0"
    assert api_config.endpoints[2].dataset_id == "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0"
    assert api_config.timeout_seconds == 300
    assert api_config.max_retries == 5


def test_oecd_api_config_custom_values() -> None:
    """Test valid instantiation of OecdApiConfig with custom values."""
    endpoint = OecdEndpointConfig(
        dataset_id="CUSTOM",
        description="Custom",
    )
    api_config = OecdApiConfig(
        base_url="https://custom.org/data/",  # type: ignore
        endpoints=[endpoint],
        timeout_seconds=60,
        max_retries=3,
    )

    assert str(api_config.base_url) == "https://custom.org/data/"
    assert len(api_config.endpoints) == 1
    assert api_config.endpoints[0].dataset_id == "CUSTOM"
    assert api_config.timeout_seconds == 60
    assert api_config.max_retries == 3


def test_oecd_api_config_invalid_base_url() -> None:
    """Test OecdApiConfig raises validation error on invalid base URL."""
    with pytest.raises(ValidationError):
        OecdApiConfig(
            base_url="not_a_url",  # type: ignore
        )
