# Copyright (c) CoReason, Inc.
# This software is released under the Prosperity Public License 3.0.

import pytest
from coreason_etl_oecd_health.models import OecdApiConfig, OecdEndpointConfig
from pydantic import ValidationError


def test_oecd_endpoint_config_valid() -> None:
    """Test valid instantiation of OecdEndpointConfig."""
    config = OecdEndpointConfig(
        dataset_id="OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
        url="https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.0/all",  # type: ignore
        description="Health Expenditure",
    )
    assert config.dataset_id == "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
    assert (
        str(config.url)
        == "https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.0/all"
    )
    assert config.description == "Health Expenditure"


def test_oecd_endpoint_config_invalid_url() -> None:
    """Test OecdEndpointConfig raises validation error on invalid URL."""
    with pytest.raises(ValidationError):
        OecdEndpointConfig(
            dataset_id="TEST",
            url="not_a_url",  # type: ignore
            description="Test Description",
        )


def test_oecd_api_config_valid() -> None:
    """Test valid instantiation of OecdApiConfig."""
    endpoint = OecdEndpointConfig(
        dataset_id="OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
        url="https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.0/all",  # type: ignore
        description="Health Expenditure",
    )
    api_config = OecdApiConfig(
        base_url="https://sdmx.oecd.org/public/rest/data/",  # type: ignore
        endpoints=[endpoint],
    )

    assert str(api_config.base_url) == "https://sdmx.oecd.org/public/rest/data/"
    assert len(api_config.endpoints) == 1
    assert api_config.endpoints[0].dataset_id == "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"


def test_oecd_api_config_invalid_base_url() -> None:
    """Test OecdApiConfig raises validation error on invalid base URL."""
    endpoint = OecdEndpointConfig(
        dataset_id="TEST",
        url="https://example.com/test",  # type: ignore
        description="Test Description",
    )
    with pytest.raises(ValidationError):
        OecdApiConfig(
            base_url="not_a_url",  # type: ignore
            endpoints=[endpoint],
        )


def test_oecd_api_config_missing_endpoints() -> None:
    """Test OecdApiConfig raises validation error if endpoints are missing."""
    with pytest.raises(ValidationError):
        OecdApiConfig(
            base_url="https://sdmx.oecd.org/public/rest/data/",  # type: ignore
        )
