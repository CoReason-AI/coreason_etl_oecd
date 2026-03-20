-- Copyright (c) CoReason, Inc.
-- Released under the Prosperity Public License 3.0

-- AGENT INSTRUCTION: Denormalized view focusing on healthcare financing metrics.
-- This view pivots and filters specifically for the SHA dataset to ensure continuous time-series.

SELECT
    country_code,
    indicator_code,
    unit_of_measure,
    metric_year,
    metric_value,
    status_flag
FROM {{ ref('silver_oecd_health_metrics') }}
WHERE dataset_id = 'OECD.ELS.HD,DSD_SHA@DF_SHA,1.0'
ORDER BY
    country_code,
    indicator_code,
    metric_year DESC
