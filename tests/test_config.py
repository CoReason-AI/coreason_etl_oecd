import pytest
from pydantic import ValidationError

from coreason_etl_oecd_health.config import OECDHealthConfig


def test_config_defaults() -> None:
    config = OECDHealthConfig()
    assert str(config.base_url) == "https://sdmx.oecd.org/public/rest/data/"
    assert config.datasets == [
        "OECD.ELS.HD,DSD_SHA@DF_SHA,1.0",
        "OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0",
        "OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0",
    ]
    assert config.headers == {
        "Accept": "text/csv",
        "Accept-Encoding": "gzip",
    }
    assert config.timeout == 60


def test_config_override() -> None:
    config = OECDHealthConfig(
        base_url="https://api.example.com/",
        datasets=["test.dataset"],
        headers={"Accept": "application/json"},
        timeout=120,
    )
    assert str(config.base_url) == "https://api.example.com/"
    assert config.datasets == ["test.dataset"]
    assert config.headers == {"Accept": "application/json"}
    assert config.timeout == 120


def test_config_invalid_url() -> None:
    with pytest.raises(ValidationError) as exc:
        OECDHealthConfig(base_url="invalid_url")
    assert "base_url" in str(exc.value)


def test_config_invalid_datasets() -> None:
    with pytest.raises(ValidationError) as exc:
        OECDHealthConfig(datasets="not a list")
    assert "datasets" in str(exc.value)


def test_config_invalid_headers() -> None:
    with pytest.raises(ValidationError) as exc:
        OECDHealthConfig(headers="not a dict")
    assert "headers" in str(exc.value)


def test_config_invalid_timeout() -> None:
    with pytest.raises(ValidationError) as exc:
        OECDHealthConfig(timeout=0)
    assert "timeout" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        OECDHealthConfig(timeout=-1)
    assert "timeout" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        OECDHealthConfig(timeout="not an int")
    assert "timeout" in str(exc.value)
