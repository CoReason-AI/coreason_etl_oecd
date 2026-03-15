# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com//coreason_etl_oecd


from coreason_etl_oecd_health.utils.logger import logger


def test_logger_initialization() -> None:
    """Test that the logger is initialized correctly and creates the log directory."""
    from unittest import mock

    from coreason_etl_oecd_health.utils.logger import init_logger

    with mock.patch("coreason_etl_oecd_health.utils.logger.Path") as mock_path_cls:
        # Create a mock instance
        mock_log_path = mock.Mock()
        mock_log_path.exists.return_value = False

        # Make the mocked Path class return our mock instance
        mock_path_cls.return_value = mock_log_path

        # Mock logger.add and logger.remove to avoid any actual side effects
        with (
            mock.patch("coreason_etl_oecd_health.utils.logger.logger.add"),
            mock.patch("coreason_etl_oecd_health.utils.logger.logger.remove"),
        ):
            # Call the initialization function directly
            init_logger()

            # Assert mkdir was called
            mock_log_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)


def test_logger_exports() -> None:
    """Test that logger is exported."""
    assert logger is not None
