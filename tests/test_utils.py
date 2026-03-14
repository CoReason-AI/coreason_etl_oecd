# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com//coreason_etl_oecd

from pathlib import Path

from coreason_etl_oecd.utils.logger import logger


def test_logger_initialization(tmp_path: Path) -> None:
    """Test that the logger is initialized correctly and creates the log directory."""
    import importlib
    import shutil

    import coreason_etl_oecd.utils.logger

    # Point to tmp directory and ensure it doesn't exist
    log_dir = tmp_path / "logs"
    if log_dir.exists():
        shutil.rmtree(log_dir)

    # Test directory creation directly by removing the logs directory
    # and importing/reloading the logger module

    # Close any existing logger handlers so Windows can delete the file
    from loguru import logger

    logger.remove()

    # Ensure logs dir does not exist before reload
    logs_dir = Path("logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)

    # Reloading will execute the module level code, which creates the dir
    importlib.reload(coreason_etl_oecd.utils.logger)

    assert logs_dir.exists()
    assert logs_dir.is_dir()


def test_logger_exports() -> None:
    """Test that logger is exported."""
    assert logger is not None
