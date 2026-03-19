# coreason-etl-oecd-health

A robust ETL pipeline for ingesting, normalizing, and serving the OECD Health Statistics database.

This project implements a Type A pipeline according to the CoReason Data Engineering Standard.

## Prerequisites

- Python 3.11+
- uv

## Setup

1.  Clone the repository:
    ```sh
    git clone <repo-url>
    cd coreason-etl-oecd-health
    ```
2.  Install dependencies:
    ```sh
    uv pip install -e '.[dev]'
    ```

## Development

-   Run the tests:
    ```sh
    uv run pytest
    ```
-   Run linting:
    ```sh
    uv run ruff format .
    uv run ruff check --fix .
    uv run pre-commit run --all-files
    ```
