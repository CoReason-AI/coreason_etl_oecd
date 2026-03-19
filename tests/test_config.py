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
    assert config.target_datasets == (
        "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
        "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
        "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
    )
    assert config.accept_header == "text/csv"
    assert config.max_retries == 3


def test_oecd_config_env_overrides() -> None:
    """Test that environment variables successfully override default configuration values."""
    env_overrides = {
        "OECD_BASE_ENDPOINT": "https://test.oecd.org/public/rest/data/",
        "OECD_TARGET_DATASETS": '["TEST_DATASET_1", "TEST_DATASET_2"]',
        "OECD_ACCEPT_HEADER": "application/json",
        "OECD_MAX_RETRIES": "5",
    }
    with patch.dict(os.environ, env_overrides, clear=True):
        config = OECDConfig()
        assert str(config.base_endpoint) == "https://test.oecd.org/public/rest/data/"
        assert config.target_datasets == ("TEST_DATASET_1", "TEST_DATASET_2")
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


def test_oecd_config_extra_env_ignored() -> None:
    """Test that extra environment variables with the OECD_ prefix are ignored."""
    env_overrides = {"OECD_UNKNOWN_FIELD": "some_value"}
    with patch.dict(os.environ, env_overrides, clear=True):
        config = OECDConfig()
        assert not hasattr(config, "unknown_field")


def test_oecd_config_case_insensitivity() -> None:
    """Test that environment variables are matched case-insensitively."""
    env_overrides = {
        "oecd_base_endpoint": "https://lower.case.org/data/",
        "OeCd_MaX_rEtRiEs": "10",
    }
    with patch.dict(os.environ, env_overrides, clear=True):
        config = OECDConfig()
        assert str(config.base_endpoint) == "https://lower.case.org/data/"
        assert config.max_retries == 10


def test_oecd_config_empty_strings_allowed() -> None:
    """Test that empty string environment variables are accepted for string fields."""
    env_overrides = {
        "OECD_TARGET_DATASETS": "[]",
        "OECD_ACCEPT_HEADER": "",
    }
    with patch.dict(os.environ, env_overrides, clear=True):
        config = OECDConfig()
        assert config.target_datasets == ()
        assert config.accept_header == ""


def test_oecd_config_table_naming_convention() -> None:
    """Test dynamic table generation adheres to the medallion naming rules."""
    config = OECDConfig()

    dataset = "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"

    bronze_table = config.get_table_name("Bronze", dataset)
    assert bronze_table == "coreason_etl_oecd_health_bronze_oecd_els_hd_dsd_sha_df_sha_1_0"

    silver_table = config.get_table_name("SILVER", "my_custom_file")
    assert silver_table == "coreason_etl_oecd_health_silver_my_custom_file"

    gold_table = config.get_table_name("gold", "oecd_finances")
    assert gold_table == "coreason_etl_oecd_health_gold_oecd_finances"


def test_oecd_config_invalid_layer() -> None:
    """Test an invalid medallion layer throws a value error."""
    config = OECDConfig()
    with pytest.raises(ValueError) as exc_info:
        config.get_table_name("platinum", "my_file")
    assert "invalid medallion layer" in str(exc_info.value).lower()
