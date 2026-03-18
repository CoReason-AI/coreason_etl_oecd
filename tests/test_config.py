# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

import pytest
from coreason_etl_oecd_health.config import OECDApiConfig, OECDDatasetConfig
from pydantic import ValidationError


def test_oecd_dataset_config_valid() -> None:
    config = OECDDatasetConfig(dataset_id="TEST.ID", name="Test Dataset")
    assert config.dataset_id == "TEST.ID"
    assert config.name == "Test Dataset"


def test_oecd_dataset_config_missing_fields() -> None:
    with pytest.raises(ValidationError):
        OECDDatasetConfig()  # type: ignore


def test_oecd_api_config_defaults() -> None:
    config = OECDApiConfig()
    assert str(config.base_url) == "https://sdmx.oecd.org/public/rest/data/"
    assert len(config.datasets) == 3
    assert config.datasets[0].dataset_id == "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
    assert config.datasets[0].name == "Health Expenditure"
    assert config.timeout_seconds == 300
    assert config.max_retries == 5


def test_oecd_api_config_custom_values() -> None:
    custom_datasets = [OECDDatasetConfig(dataset_id="CUSTOM.ID", name="Custom")]
    config = OECDApiConfig(
        base_url="https://custom.api.org/data/",  # type: ignore
        datasets=custom_datasets,
        timeout_seconds=60,
        max_retries=3,
    )
    assert str(config.base_url) == "https://custom.api.org/data/"
    assert len(config.datasets) == 1
    assert config.datasets[0].dataset_id == "CUSTOM.ID"
    assert config.timeout_seconds == 60
    assert config.max_retries == 3


def test_oecd_api_config_invalid_url() -> None:
    with pytest.raises(ValidationError):
        OECDApiConfig(base_url="not-a-url")  # type: ignore
