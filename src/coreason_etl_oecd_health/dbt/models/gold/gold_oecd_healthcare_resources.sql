-- Copyright (c) CoReason, Inc.
-- Released under the Prosperity Public License 3.0

-- AGENT INSTRUCTION: Unified view summarizing hospital beds, practicing physicians, and medical tech density.
-- Sourced from the HOSP_REAC and KEY_INDIC datasets.

SELECT
    country_code,
    indicator_code,
    unit_of_measure,
    metric_year,
    metric_value,
    status_flag
FROM {{ ref('silver_oecd_health_metrics') }}
WHERE dataset_id IN (
    'OECD.ELS.HD,DSD_HEALTH_REAC_HOSP@DF_HOSP_REAC,1.0',
    'OECD.ELS.HD,DSD_HEALTH_PROC@DF_KEY_INDIC,1.0'
)
ORDER BY
    country_code,
    indicator_code,
    metric_year DESC
