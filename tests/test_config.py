# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

import pytest
from coreason_etl_oecd_health.config import OecdApiConfig, OecdDatasetConfig
from pydantic import ValidationError


def test_oecd_dataset_config_valid() -> None:
    config = OecdDatasetConfig(dataset_id="TEST_ID", description="Test Description")
    assert config.dataset_id == "TEST_ID"
    assert config.description == "Test Description"


def test_oecd_dataset_config_missing_fields() -> None:
    with pytest.raises(ValidationError) as exc_info:
        OecdDatasetConfig()  # type: ignore
    assert "2 validation errors for OecdDatasetConfig" in str(exc_info.value)
    assert "dataset_id" in str(exc_info.value)
    assert "description" in str(exc_info.value)


def test_oecd_api_config_default() -> None:
    config = OecdApiConfig()
    assert str(config.base_url) == "https://sdmx.oecd.org/public/rest/data/"
    assert len(config.datasets) == 3

    dataset_ids = [d.dataset_id for d in config.datasets]
    assert "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0" in dataset_ids
    assert "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0" in dataset_ids
    assert "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0" in dataset_ids


def test_oecd_api_config_custom_url() -> None:
    config = OecdApiConfig(base_url="https://api.example.com/data/")  # type: ignore
    assert str(config.base_url) == "https://api.example.com/data/"


def test_oecd_api_config_invalid_url() -> None:
    with pytest.raises(ValidationError) as exc_info:
        OecdApiConfig(base_url="not-a-url")  # type: ignore
    assert "1 validation error for OecdApiConfig" in str(exc_info.value)
    assert "base_url" in str(exc_info.value)


def test_oecd_api_config_custom_datasets() -> None:
    datasets = [OecdDatasetConfig(dataset_id="CUSTOM_ID", description="Custom Description")]
    config = OecdApiConfig(datasets=datasets)
    assert len(config.datasets) == 1
    assert config.datasets[0].dataset_id == "CUSTOM_ID"
    assert config.datasets[0].description == "Custom Description"
