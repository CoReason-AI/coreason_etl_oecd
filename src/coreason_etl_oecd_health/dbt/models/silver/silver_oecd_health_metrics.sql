-- Copyright (c) CoReason, Inc.
-- Released under the Prosperity Public License 3.0

-- AGENT INSTRUCTION: Identity Resolution must generate a UUIDv5 from a fixed namespace and the composite source_id.
-- AGENT INSTRUCTION: Standardize OBS_STATUS values into a readable status_flag.
-- AGENT INSTRUCTION: Extract strictly typed fields from the JSONB raw_data column.

WITH raw_metrics AS (
    SELECT
        source_id,
        dataset_id,
        ingestion_ts,
        raw_data,
        -- Dual ID Mandate pushed to SQL
        uuid_generate_v5('6ba7b810-9dad-11d1-80b4-00c04fd430c8'::uuid, source_id) AS coreason_id,
        md5(raw_data::text) AS content_hash,

        -- JSONB extraction
        raw_data->>'REF_AREA' AS country_code,
        raw_data->>'MEASURE' AS indicator_code,
        raw_data->>'UNIT_MEASURE' AS unit_of_measure,
        CAST(raw_data->>'TIME_PERIOD' AS INTEGER) AS metric_year,
        CAST(raw_data->>'OBS_VALUE' AS FLOAT) AS metric_value,
        raw_data->>'OBS_STATUS' AS obs_status
    FROM {{ source('coreason_etl_oecd_health', 'oecd_health_datasets') }}
),

standardized_metrics AS (
    SELECT
        coreason_id,
        dataset_id,
        country_code,
        indicator_code,
        unit_of_measure,
        metric_year,
        metric_value,
        -- Clean OBS_STATUS flags via SQL CASE statement
        CASE
            WHEN obs_status = 'E' THEN 'Estimated'
            WHEN obs_status = 'B' THEN 'Break in Time Series'
            WHEN obs_status = 'P' THEN 'Provisional'
            ELSE 'Actual'
        END AS status_flag,
        content_hash,
        ingestion_ts
    FROM raw_metrics
)

SELECT * FROM standardized_metrics
