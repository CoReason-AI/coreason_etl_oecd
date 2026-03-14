import pytest
from pydantic import HttpUrl, ValidationError

from coreason_etl_oecd.config import OECDHealthConfig


def test_oecd_health_config_default_instantiation() -> None:
    """Test that the configuration can be instantiated with default values."""
    config = OECDHealthConfig()

    assert str(config.base_endpoint) == "https://sdmx.oecd.org/public/rest/data/"
    assert config.target_datasets == [
        "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
        "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
        "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
    ]
    assert config.timeout == 60


def test_oecd_health_config_custom_instantiation() -> None:
    """Test that the configuration can be instantiated with custom values."""
    custom_endpoint = "https://custom.endpoint.org/api/"
    custom_datasets = ["DATASET_1", "DATASET_2"]
    custom_timeout = 120

    config = OECDHealthConfig(
        base_endpoint=HttpUrl(custom_endpoint),
        target_datasets=custom_datasets,
        timeout=custom_timeout,
    )

    assert str(config.base_endpoint) == custom_endpoint
    assert config.target_datasets == custom_datasets
    assert config.timeout == custom_timeout


def test_oecd_health_config_invalid_base_endpoint() -> None:
    """Test that invalid URLs are rejected for the base endpoint."""
    with pytest.raises(ValidationError) as exc_info:
        OECDHealthConfig(base_endpoint="not-a-valid-url")

    assert "base_endpoint" in str(exc_info.value)
    assert "Input should be a valid URL" in str(exc_info.value)


def test_oecd_health_config_empty_target_datasets() -> None:
    """Test that empty target_datasets list is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        OECDHealthConfig(target_datasets=[])

    assert "target_datasets cannot be empty" in str(exc_info.value)


def test_oecd_health_config_empty_string_target_datasets() -> None:
    """Test that empty strings inside target_datasets are rejected."""
    with pytest.raises(ValidationError) as exc_info:
        OECDHealthConfig(target_datasets=["DATASET_1", "", "DATASET_2"])

    assert "dataset IDs cannot be empty strings" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info2:
        OECDHealthConfig(target_datasets=["DATASET_1", "   ", "DATASET_2"])

    assert "dataset IDs cannot be empty strings" in str(exc_info2.value)


def test_oecd_health_config_invalid_timeout() -> None:
    """Test that invalid timeouts are rejected."""
    with pytest.raises(ValidationError) as exc_info:
        OECDHealthConfig(timeout=0)

    assert "Input should be greater than or equal to 1" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info2:
        OECDHealthConfig(timeout=-5)

    assert "Input should be greater than or equal to 1" in str(exc_info2.value)
