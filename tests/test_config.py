"""
Copyright (c) CoReason, Inc.
This software is released under the Prosperity Public License 3.0.
"""

import pytest
from pydantic import ValidationError

from coreason_etl_oecd_health.config import DatasetConfig, OECDConfig


def test_dataset_config_valid() -> None:
    """Test valid DatasetConfig."""
    config = DatasetConfig(dataset_id="TEST.DATASET", description="A test dataset")
    assert config.dataset_id == "TEST.DATASET"
    assert config.description == "A test dataset"


def test_dataset_config_invalid() -> None:
    """Test DatasetConfig with missing fields."""
    with pytest.raises(ValidationError):
        DatasetConfig(dataset_id="TEST.DATASET")  # type: ignore

    with pytest.raises(ValidationError):
        DatasetConfig(description="A test dataset")  # type: ignore


def test_oecd_config_defaults() -> None:
    """Test OECDConfig default values match BRD/FRD."""
    config = OECDConfig()

    # Assert base endpoint
    assert str(config.base_endpoint) == "https://sdmx.oecd.org/public/rest/data/"

    # Assert correct datasets are pre-configured
    assert len(config.datasets) == 3
    dataset_ids = [d.dataset_id for d in config.datasets]
    assert "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0" in dataset_ids
    assert "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0" in dataset_ids
    assert "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0" in dataset_ids


def test_oecd_config_custom() -> None:
    """Test OECDConfig with custom values."""
    custom_datasets = [DatasetConfig(dataset_id="CUSTOM", description="Custom Dataset")]
    config = OECDConfig(base_endpoint="https://example.com/api/", datasets=custom_datasets)  # type: ignore

    assert str(config.base_endpoint) == "https://example.com/api/"
    assert len(config.datasets) == 1
    assert config.datasets[0].dataset_id == "CUSTOM"
    assert config.datasets[0].description == "Custom Dataset"


def test_oecd_config_invalid_url() -> None:
    """Test OECDConfig with invalid URL."""
    with pytest.raises(ValidationError):
        OECDConfig(base_endpoint="not-a-url")  # type: ignore
