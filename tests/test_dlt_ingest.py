# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

from datetime import datetime, timezone

import pytest
import requests
import requests_mock
from coreason_etl_oecd_health.config import OECDApiConfig
from coreason_etl_oecd_health.dlt.ingest import (
    coreason_oecd_health_pipeline,
    get_resilient_session,
    oecd_health_datasets,
    stream_oecd_dataset,
)


@pytest.fixture
def mock_config() -> OECDApiConfig:
    return OECDApiConfig(
        target_datasets=("TEST_DATASET",),
        base_url="https://test.oecd.org/public/rest/data/",  # type: ignore
        timeout=30,
        retry_count=1,
    )


@pytest.fixture
def sample_csv_data() -> str:
    # A tiny chunk of a fake SDMX CSV stream
    return "REF_AREA,MEASURE,TIME_PERIOD,OBS_VALUE\nUS,EXP,2020,10.5\nUK,EXP,2021,12.3\n"


def test_get_resilient_session(mock_config: OECDApiConfig) -> None:
    """Test that the session is configured with the correct retry strategy."""
    session = get_resilient_session(mock_config)
    adapter = session.get_adapter("https://")

    assert getattr(adapter, "max_retries").total == mock_config.retry_count
    assert list(getattr(adapter, "max_retries").status_forcelist) == [429, 500, 502, 503, 504]


def test_stream_oecd_dataset_success(
    requests_mock: requests_mock.Mocker,
    mock_config: OECDApiConfig,
    sample_csv_data: str,
) -> None:
    """Test memory-safe CSV streaming and Medallion formatting."""
    dataset_id = "TEST_DATASET"
    batch_ts = datetime.now(timezone.utc).isoformat()
    session = get_resilient_session(mock_config)

    # Mock the streaming endpoint
    url = f"{str(mock_config.base_url).rstrip('/')}/{dataset_id}/all"
    requests_mock.get(
        url,
        text=sample_csv_data,
        status_code=200,
        headers={"Content-Type": "text/csv"},
    )

    # Consume the generator
    results = list(stream_oecd_dataset(dataset_id, session, mock_config, batch_ts))

    assert len(results) == 2

    # Verify exact formatting dictionary structure mandate
    assert results[0]["dataset_id"] == "TEST_DATASET"
    assert results[0]["source_id"] == "US_EXP_2020"
    assert results[0]["ingestion_ts"] == batch_ts
    assert results[0]["raw_data"] == {
        "REF_AREA": "US",
        "MEASURE": "EXP",
        "TIME_PERIOD": "2020",
        "OBS_VALUE": "10.5",
    }

    assert results[1]["source_id"] == "UK_EXP_2021"


def test_stream_oecd_dataset_missing_keys(
    requests_mock: requests_mock.Mocker,
    mock_config: OECDApiConfig,
) -> None:
    """Test composite source_id handles missing columns gracefully."""
    dataset_id = "TEST_DATASET"
    batch_ts = "2024-01-01T00:00:00Z"
    session = get_resilient_session(mock_config)

    url = f"{str(mock_config.base_url).rstrip('/')}/{dataset_id}/all"

    # Missing REF_AREA, MEASURE, and TIME_PERIOD
    csv_missing_keys = "OTHER_COL\n123\n"

    requests_mock.get(url, text=csv_missing_keys, status_code=200)

    results = list(stream_oecd_dataset(dataset_id, session, mock_config, batch_ts))

    assert len(results) == 1
    assert results[0]["source_id"] == "UNKNOWN_UNKNOWN_UNKNOWN"


def test_stream_oecd_dataset_http_error(
    requests_mock: requests_mock.Mocker,
    mock_config: OECDApiConfig,
) -> None:
    """Test that HTTP errors are raised correctly."""
    dataset_id = "TEST_DATASET"
    session = get_resilient_session(mock_config)

    url = f"{str(mock_config.base_url).rstrip('/')}/{dataset_id}/all"

    # Mock a 404 Not Found error
    requests_mock.get(url, status_code=404)

    with pytest.raises(requests.exceptions.HTTPError):
        list(stream_oecd_dataset(dataset_id, session, mock_config, "2024-01-01T00:00:00Z"))


def test_dlt_resource_generation(
    requests_mock: requests_mock.Mocker,
    mock_config: OECDApiConfig,
    sample_csv_data: str,
) -> None:
    """Test the overarching dlt resource and pipeline source definitions."""
    url = f"{str(mock_config.base_url).rstrip('/')}/TEST_DATASET/all"
    requests_mock.get(url, text=sample_csv_data, status_code=200)

    # Test the resource directly
    resource = oecd_health_datasets(mock_config)

    # The resource flattens the generators when iterated, so it yields the dicts directly
    records = list(resource)
    assert len(records) == 2
    assert records[0]["dataset_id"] == "TEST_DATASET"

    # Test the pipeline source wraps the resource correctly
    source = coreason_oecd_health_pipeline(mock_config)

    # The source is a dlt list of resources, and we should be able to access our resource
    assert "oecd_health_datasets" in source.resources
    assert source.resources["oecd_health_datasets"].max_table_nesting == 0
