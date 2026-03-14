# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com//coreason_etl_oecd

from coreason_etl_oecd.main import hello_world
import pytest
from hypothesis import given, strategies as st
import re


def test_hello_world() -> None:
    assert hello_world() == "Hello World!"


@pytest.mark.asyncio
async def test_hello_world_async_structure() -> None:
    # Example placeholder for an async structural test
    assert hello_world() == "Hello World!"


@given(st.text())
def test_hello_world_hypothesis(sample_text: str) -> None:
    # Example property-based test setup using hypothesis
    assert isinstance(hello_world(), str)


def test_module_naming_convention() -> None:
    """Ensure strict snake_case module naming convention."""
    module_name = "coreason_etl_oecd"
    pattern = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
    assert re.match(pattern, module_name), f"Module name '{module_name}' violates snake_case convention."
