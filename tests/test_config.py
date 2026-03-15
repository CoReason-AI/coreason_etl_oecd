import pytest
from pydantic import ValidationError

from coreason_etl_oecd_health.config import OecdApiConfig


def test_config_defaults() -> None:
    config = OecdApiConfig()
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
    assert config.chunk_by_year is True
    assert config.start_year == 2000
    assert config.end_year == 2026


def test_config_override() -> None:
    config = OecdApiConfig(
        base_url="https://api.example.com/",
        datasets=["test.dataset"],
        headers={"Accept": "application/json"},
        timeout=120,
        chunk_by_year=False,
        start_year=2010,
        end_year=2024,
    )
    assert str(config.base_url) == "https://api.example.com/"
    assert config.datasets == ["test.dataset"]
    assert config.headers == {"Accept": "application/json"}
    assert config.timeout == 120
    assert config.chunk_by_year is False
    assert config.start_year == 2010
    assert config.end_year == 2024


def test_config_invalid_url() -> None:
    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(base_url="invalid_url")
    assert "base_url" in str(exc.value)


def test_config_invalid_datasets() -> None:
    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(datasets="not a list")
    assert "datasets" in str(exc.value)


def test_config_invalid_headers() -> None:
    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(headers="not a dict")
    assert "headers" in str(exc.value)


def test_config_invalid_timeout() -> None:
    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(timeout=0)
    assert "timeout" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(timeout=-1)
    assert "timeout" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(timeout="not an int")
    assert "timeout" in str(exc.value)


def test_config_invalid_chunk_by_year() -> None:
    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(chunk_by_year="not a bool")
    assert "chunk_by_year" in str(exc.value)


def test_config_invalid_start_year() -> None:
    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(start_year="not an int")
    assert "start_year" in str(exc.value)


def test_config_invalid_end_year() -> None:
    with pytest.raises(ValidationError) as exc:
        OecdApiConfig(end_year="not an int")
    assert "end_year" in str(exc.value)
