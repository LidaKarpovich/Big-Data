CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.predictions
(
    id UInt64,
    prediction Float64
)
ENGINE = MergeTree()
ORDER BY id;
