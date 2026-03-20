# Copyright (c) CoReason, Inc.
# Released under the Prosperity Public License 3.0

import json
import logging
import subprocess
import sys
from pathlib import Path

import dlt

from coreason_etl_oecd_health.config import OECDApiConfig
from coreason_etl_oecd_health.dlt.ingest import coreason_oecd_health_pipeline


class JsonFormatter(logging.Formatter):
    """
    AGENT INSTRUCTION: JSON structured logging for Observability.
    Enforces inclusion of standard attributes for logging aggregators.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
        }
        if hasattr(record, "ingestion_batch_id"):
            log_record["ingestion_batch_id"] = record.ingestion_batch_id
        if hasattr(record, "dataset"):
            log_record["dataset"] = record.dataset

        return json.dumps(log_record)


def configure_logger() -> logging.Logger:
    """Configure a structured JSON logger for the pipeline."""
    logger = logging.getLogger("coreason_etl")
    logger.setLevel(logging.INFO)

    # Avoid duplicating handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger


def run_pipeline() -> None:
    """
    Orchestrates the CoReason OECD Health Data Medallion Pipeline.
    Runs the dlt ingestion, logs metrics, and triggers dbt transformation.
    """
    config = OECDApiConfig()
    logger = configure_logger()
    batch_id = f"batch_{config.get_table_name('Bronze', 'run')}"

    extra = {"ingestion_batch_id": batch_id, "dataset": "all"}
    logger.info("Initializing OECD Health Pipeline.", extra=extra)

    # 1. Run dlt extraction
    try:
        pipeline = dlt.pipeline(
            pipeline_name="coreason_oecd_health",
            destination="postgres",
            dataset_name=config.bronze_schema,
        )

        load_info = pipeline.run(coreason_oecd_health_pipeline(config))
        logger.info(f"dlt load completed: {load_info}", extra=extra)

        # Log rows loaded for Observability Mandate
        for package in load_info.load_packages:
            for job in package.jobs["completed_jobs"]:
                if job.job_file_info.table_name == "oecd_health_datasets":
                    logger.info(
                        f"Rows successfully loaded into Bronze: {job.job_file_info.file_size}",
                        extra=extra,
                    )

    except Exception as e:
        logger.error(f"dlt extraction failed: {str(e)}", extra=extra)
        raise

    # 2. Run dbt transformation (Silver -> Gold)
    dbt_project_dir = Path(__file__).parent / "dbt"
    logger.info(f"Triggering dbt run in {dbt_project_dir}", extra=extra)

    try:
        # Run dbt using the subprocess module for isolated execution
        subprocess.run(
            ["dbt", "run", "--project-dir", str(dbt_project_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info("dbt transformations completed successfully.", extra=extra)
    except subprocess.CalledProcessError as e:
        logger.error(f"dbt run failed. stdout: {e.stdout}, stderr: {e.stderr}", extra=extra)
        raise


if __name__ == "__main__":  # pragma: no cover
    run_pipeline()
