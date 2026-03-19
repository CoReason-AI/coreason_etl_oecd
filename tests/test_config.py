# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

import os
from unittest.mock import patch

import pytest
from coreason_etl_oecd_health.config import OECDConfig
from pydantic import ValidationError


def test_oecd_config_default_instantiation() -> None:
    """Test that the configuration instantiates correctly with default values."""
    config = OECDConfig()
    assert str(config.base_endpoint) == "https://sdmx.oecd.org/public/rest/data/"
    assert config.health_expenditure_dataset == "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
    assert config.provider_resources_dataset == "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0"
    assert config.healthcare_utilisation_dataset == "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0"
    assert config.accept_header == "text/csv"
    assert config.max_retries == 3


def test_oecd_config_env_overrides() -> None:
    """Test that environment variables successfully override default configuration values."""
    env_overrides = {
        "OECD_BASE_ENDPOINT": "https://test.oecd.org/public/rest/data/",
        "OECD_HEALTH_EXPENDITURE_DATASET": "TEST_DATASET_1",
        "OECD_PROVIDER_RESOURCES_DATASET": "TEST_DATASET_2",
        "OECD_HEALTHCARE_UTILISATION_DATASET": "TEST_DATASET_3",
        "OECD_ACCEPT_HEADER": "application/json",
        "OECD_MAX_RETRIES": "5",
    }
    with patch.dict(os.environ, env_overrides, clear=True):
        config = OECDConfig()
        assert str(config.base_endpoint) == "https://test.oecd.org/public/rest/data/"
        assert config.health_expenditure_dataset == "TEST_DATASET_1"
        assert config.provider_resources_dataset == "TEST_DATASET_2"
        assert config.healthcare_utilisation_dataset == "TEST_DATASET_3"
        assert config.accept_header == "application/json"
        assert config.max_retries == 5


def test_oecd_config_invalid_url() -> None:
    """Test that an invalid URL for base_endpoint raises a validation error."""
    env_overrides = {"OECD_BASE_ENDPOINT": "not-a-valid-url"}
    with patch.dict(os.environ, env_overrides, clear=True):
        with pytest.raises(ValidationError) as exc_info:
            OECDConfig()
        assert "url" in str(exc_info.value).lower()


def test_oecd_config_invalid_max_retries() -> None:
    """Test that a non-integer for max_retries raises a validation error."""
    env_overrides = {"OECD_MAX_RETRIES": "not-a-number"}
    with patch.dict(os.environ, env_overrides, clear=True):
        with pytest.raises(ValidationError) as exc_info:
            OECDConfig()
        assert "integer" in str(exc_info.value).lower()
