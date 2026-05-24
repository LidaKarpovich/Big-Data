CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.events (
    id UInt64,
    x1 Float64,
    x2 Float64,
    x3 Float64,
    label Float64
)
ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS analytics.ml_results (
    ts DateTime,
    accuracy Float64,
    rows_processed UInt64
)
ENGINE = MergeTree()
ORDER BY ts;
