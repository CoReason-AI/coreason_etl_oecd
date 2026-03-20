# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

import csv
import logging
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any

import dlt
from dlt.sources.helpers.requests import Client

from coreason_etl_oecd_health.config import OECDApiConfig

logger = logging.getLogger(__name__)


def stream_oecd_dataset(
    dataset_id: str,
    client: Client,
    config: OECDApiConfig,
    batch_ts: str,
) -> Iterator[dict[str, Any]]:
    """
    AGENT INSTRUCTION: Yield dictionaries properly formatted for the Medallion pipeline.
    Must use requests.get(stream=True) and response.iter_lines(decode_unicode=True)
    to protect memory from massive OECD CSV files.
    """
    # Force CSV returns & compress the payload over the wire
    headers = {
        "Accept": config.accept_header,
        "Accept-Encoding": "gzip",
    }

    # Optional chunking suffix /all vs specific time periods.
    # For now, default to /all to demonstrate memory-safe extraction.
    # Advanced TIME_PERIOD chunking logic can be integrated into URL builder.
    url = f"{str(config.base_url).rstrip('/')}/{dataset_id}/all"

    logger.info(f"Starting memory-safe streaming for {dataset_id} via {url}")

    with client.get(url, headers=headers, stream=True) as response:
        # Client raises automatically based on raise_for_status=True default
        # memory-safe CSV parsing
        lines = (line for line in response.iter_lines(decode_unicode=True) if line)
        reader = csv.DictReader(lines)

        for row_dict in reader:
            # Create a composite source ID: <REF_AREA>_<MEASURE>_<TIME_PERIOD>
            ref_area = row_dict.get("REF_AREA", "UNKNOWN")
            measure = row_dict.get("MEASURE", "UNKNOWN")
            time_period = row_dict.get("TIME_PERIOD", "UNKNOWN")
            source_id = f"{ref_area}_{measure}_{time_period}"

            # Format strictly matching the mandate
            yield {
                "dataset_id": dataset_id,
                "source_id": source_id,
                "ingestion_ts": batch_ts,
                "raw_data": row_dict,
            }


@dlt.resource(name="oecd_health_datasets", max_table_nesting=0)
def oecd_health_datasets(
    config: OECDApiConfig = OECDApiConfig(),
) -> Iterator[Iterator[dict[str, Any]]]:
    """
    AGENT INSTRUCTION: The core dlt resource for extracting OECD data.
    Configured with max_table_nesting=0 to force raw_data dictionary to land as JSONB.
    """
    batch_ts = datetime.now(timezone.utc).isoformat()

    # Use dlt's built-in resilient requests client
    client = Client(
        request_timeout=config.timeout,
        request_max_attempts=config.retry_count,
        status_codes=(429, 500, 502, 503, 504),
        raise_for_status=True,
    )

    for dataset_id in config.target_datasets:
        yield stream_oecd_dataset(dataset_id, client, config, batch_ts)


@dlt.source(name="coreason_oecd_health_pipeline")
def coreason_oecd_health_pipeline(
    config: OECDApiConfig = OECDApiConfig(),
) -> Any:
    """The dlt source definition containing the oecd_health_datasets resource."""
    return oecd_health_datasets(config)
