# Copyright (c) CoReason, Inc.
# This software is released under the Prosperity Public License 3.0.

import pytest
from coreason_etl_oecd_health.config import OECDApiConfig, OECDDatasetConfig
from pydantic import ValidationError


def test_oecd_dataset_config_defaults() -> None:
    """Test that OECDDatasetConfig has the correct default version."""
    config = OECDDatasetConfig(id="test_id", description="test description")
    assert config.id == "test_id"
    assert config.description == "test description"
    assert config.version == "1.0"


def test_oecd_dataset_config_custom_version() -> None:
    """Test that OECDDatasetConfig accepts a custom version."""
    config = OECDDatasetConfig(id="test_id", description="test description", version="2.0")
    assert config.version == "2.0"


def test_oecd_dataset_config_missing_required() -> None:
    """Test that OECDDatasetConfig requires id and description."""
    with pytest.raises(ValidationError):
        OECDDatasetConfig(description="test")  # type: ignore

    with pytest.raises(ValidationError):
        OECDDatasetConfig(id="test")  # type: ignore


def test_oecd_api_config_defaults() -> None:
    """Test that OECDApiConfig has the correct defaults for base_url and datasets."""
    config = OECDApiConfig()
    assert str(config.base_url) == "https://sdmx.oecd.org/public/rest/data/"
    assert len(config.datasets) == 3

    # Check datasets defaults
    assert config.datasets[0].id == "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
    assert config.datasets[0].description == "Health Expenditure"
    assert config.datasets[0].version == "1.0"

    assert config.datasets[1].id == "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0"
    assert config.datasets[1].description == "Provider Resources"
    assert config.datasets[1].version == "1.0"

    assert config.datasets[2].id == "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0"
    assert config.datasets[2].description == "Healthcare Utilisation"
    assert config.datasets[2].version == "1.0"


def test_oecd_api_config_custom_values() -> None:
    """Test that OECDApiConfig accepts custom base_url and datasets."""
    custom_dataset = OECDDatasetConfig(id="custom_id", description="custom desc")
    config = OECDApiConfig(
        base_url="https://test.api.com/data/",  # type: ignore
        datasets=[custom_dataset],
    )
    assert str(config.base_url) == "https://test.api.com/data/"
    assert len(config.datasets) == 1
    assert config.datasets[0].id == "custom_id"
