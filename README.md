# coreason_etl_oecd

A robust ETL pipeline for ingesting and normalizing OECD Health Statistics

[![CI/CD](https://github.com//coreason_etl_oecd/actions/workflows/ci-cd.yml/badge.svg)](https://github.com//coreason_etl_oecd/actions/workflows/ci-cd.yml)
[![PyPI](https://img.shields.io/pypi/v/coreason_etl_oecd.svg)](https://pypi.org/project/coreason_etl_oecd/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/coreason_etl_oecd.svg)](https://pypi.org/project/coreason_etl_oecd/)
[![License](https://img.shields.io/github/license//coreason_etl_oecd)](https://github.com//coreason_etl_oecd/blob/main/LICENSE)
[![Codecov](https://codecov.io/gh//coreason_etl_oecd/branch/main/graph/badge.svg)](https://codecov.io/gh//coreason_etl_oecd)
[![Downloads](https://static.pepy.tech/badge/coreason_etl_oecd)](https://pepy.tech/project/coreason_etl_oecd)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Getting Started

### Prerequisites

- Python 3.14+
- uv

### Installation

1.  Clone the repository:
    ```sh
    git clone https://github.com//coreason_etl_oecd.git
    cd coreason_etl_oecd
    ```
2.  Install dependencies:
    ```sh
    uv sync --all-extras --dev
    ```

### Usage

-   Run the linter:
    ```sh
    uv run pre-commit run --all-files
    ```
-   Run the tests:
    ```sh
    uv run pytest
    ```
