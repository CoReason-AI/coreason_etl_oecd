# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

import os
from unittest import mock

import pytest
from coreason_etl_oecd_health.config import OECDApiConfig
from pydantic import ValidationError


def test_oecd_api_config_defaults() -> None:
    """Test that the OECDApiConfig model sets the correct default values."""
    config = OECDApiConfig()

    # Asserting basic defaults
    assert str(config.base_url) == "https://sdmx.oecd.org/public/rest/data/"
    assert config.accept_header == "text/csv"
    assert config.timeout == 30
    assert config.retry_count == 5
    assert config.chunk_by_time_period is True

    # Deterministic sorting check for datasets
    expected_datasets = (
        "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
        "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
        "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
    )
    assert config.target_datasets == expected_datasets


def test_oecd_api_config_env_overrides() -> None:
    """Test that environment variables can override the default configurations."""
    env_vars = {
        "OECD_BASE_URL": "https://custom.oecd.endpoint/rest/",
        "OECD_ACCEPT_HEADER": "application/json",
        "OECD_TIMEOUT": "60",
        "OECD_RETRY_COUNT": "10",
        "OECD_CHUNK_BY_TIME_PERIOD": "false",
        "OECD_TARGET_DATASETS": '["DATASET1", "DATASET2"]',
    }

    with mock.patch.dict(os.environ, env_vars, clear=True):
        config = OECDApiConfig()
        assert str(config.base_url) == "https://custom.oecd.endpoint/rest/"
        assert config.accept_header == "application/json"
        assert config.timeout == 60
        assert config.retry_count == 10
        assert config.chunk_by_time_period is False
        assert config.target_datasets == ("DATASET1", "DATASET2")


def test_oecd_api_config_timeout_validation() -> None:
    """Test that timeout cannot be set to less than 30 seconds."""
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 30"):
        OECDApiConfig(timeout=29)

    # Valid timeout should succeed
    config = OECDApiConfig(timeout=31)
    assert config.timeout == 31


def test_oecd_api_config_retry_count_validation() -> None:
    """Test that retry_count cannot be set to a negative integer."""
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        OECDApiConfig(retry_count=-1)

    # Valid retry count should succeed
    config = OECDApiConfig(retry_count=0)
    assert config.retry_count == 0


def test_oecd_api_config_deterministic_sorting() -> None:
    """Test that any tuple of target_datasets provided is deterministically sorted."""
    unordered_datasets = ("Z_DATASET", "A_DATASET", "M_DATASET")
    config = OECDApiConfig(target_datasets=unordered_datasets)
    assert config.target_datasets == ("A_DATASET", "M_DATASET", "Z_DATASET")
