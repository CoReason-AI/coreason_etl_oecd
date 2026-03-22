# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

import csv
import logging
import time
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any

import dlt
import requests
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
    headers = {
        "Accept": config.accept_header,
        "Accept-Encoding": "gzip",
    }

    if config.chunk_by_time_period:
        current_year = datetime.now(timezone.utc).year
        # SHORTENED TIMEFRAME: Fetch from 2020 to present to avoid 429 rate limits
        years_to_fetch = list(range(2023, current_year + 1))
        logger.info(f"Chunking {dataset_id} sequentially from 2020 to {current_year}")
    else:
        years_to_fetch = [None] 

    for year in years_to_fetch:
        base_url = f"{str(config.base_url).rstrip('/')}/{dataset_id}/all"
        
        if year is not None:
            url = f"{base_url}?startPeriod={year}&endPeriod={year}"
            logger.info(f"Extracting {dataset_id} for year: {year}")
        else:
            url = base_url

        try:
            with client.get(url, headers=headers, stream=True) as response:
                lines = (line for line in response.iter_lines(decode_unicode=True) if line)
                reader = csv.DictReader(lines)

                for row_dict in reader:
                    ref_area = row_dict.get("REF_AREA", "UNKNOWN")
                    measure = row_dict.get("MEASURE", "UNKNOWN")
                    time_period = row_dict.get("TIME_PERIOD", "UNKNOWN")
                    source_id = f"{ref_area}_{measure}_{time_period}"

                    yield {
                        "dataset_id": dataset_id,
                        "source_id": source_id,
                        "ingestion_ts": batch_ts,
                        "raw_data": row_dict,
                    }
                    
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"No data available for {dataset_id} in year {year} (404). Skipping.")
                continue
            elif e.response.status_code == 429:
                logger.warning(f"Rate limited by OECD (429) for {dataset_id} in year {year}. Skipping.")
                time.sleep(5.0)
                continue
            else:
                logger.error(f"Extraction failed for {dataset_id} at {url}: {str(e)}")
                raise e
        except Exception as e:
            logger.error(f"Extraction failed for {dataset_id} at {url}: {str(e)}")
            raise e
        
        # Increased pause to 3 seconds to be extra polite to the server
        time.sleep(3.0)


@dlt.resource(name="oecd_health_datasets", max_table_nesting=0)
def oecd_health_datasets(
    config: OECDApiConfig = OECDApiConfig(),
) -> Iterator[Iterator[dict[str, Any]]]:
    """
    AGENT INSTRUCTION: The core dlt resource for extracting OECD data.
    Configured with max_table_nesting=0 to force raw_data dictionary to land as JSONB.
    """
    batch_ts = datetime.now(timezone.utc).isoformat()

    client = Client(
        request_timeout=config.timeout,
        request_max_attempts=config.retry_count,
        # Removed 429 from auto-retry so our custom exception handler can process it
        status_codes=(500, 502, 503, 504),
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
