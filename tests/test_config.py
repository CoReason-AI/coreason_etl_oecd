# Copyright (c) CoReason, Inc.
# This software is released under the Prosperity Public License 3.0.

import pytest
from coreason_etl_oecd_health.config import OECDHealthConfig, OECDHealthDatasetConfig
from pydantic import ValidationError


def test_oecd_health_dataset_config_valid() -> None:
    """Test valid OECDHealthDatasetConfig instantiation."""
    config = OECDHealthDatasetConfig(dataset_id="test_id", sdmx_id="test_sdmx_id")
    assert config.dataset_id == "test_id"
    assert config.sdmx_id == "test_sdmx_id"


def test_oecd_health_dataset_config_invalid() -> None:
    """Test invalid OECDHealthDatasetConfig instantiation."""
    with pytest.raises(ValidationError):
        OECDHealthDatasetConfig(dataset_id="test_id")  # type: ignore


def test_oecd_health_config_default() -> None:
    """Test default OECDHealthConfig instantiation."""
    config = OECDHealthConfig()
    assert config.base_url == "https://sdmx.oecd.org/public/rest/data/"
    assert len(config.datasets) == 3
    assert config.datasets[0].dataset_id == "health_expenditure"
    assert config.datasets[0].sdmx_id == "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
    assert config.timeout_seconds == 300
    assert config.headers == {"Accept": "text/csv", "Accept-Encoding": "gzip"}


def test_oecd_health_config_custom() -> None:
    """Test custom OECDHealthConfig instantiation."""
    datasets = [OECDHealthDatasetConfig(dataset_id="custom_id", sdmx_id="custom_sdmx_id")]
    config = OECDHealthConfig(
        base_url="https://custom.url/",
        datasets=datasets,
        timeout_seconds=100,
        headers={"Accept": "application/json"},
    )
    assert config.base_url == "https://custom.url/"
    assert len(config.datasets) == 1
    assert config.datasets[0].dataset_id == "custom_id"
    assert config.datasets[0].sdmx_id == "custom_sdmx_id"
    assert config.timeout_seconds == 100
    assert config.headers == {"Accept": "application/json"}
