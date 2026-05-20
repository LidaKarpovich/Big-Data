CREATE TABLE analytics.events
(
    timestamp DateTime,
    user_id UInt32,
    feature1 Float64,
    feature2 Float64,
    target Float64
)
ENGINE = MergeTree()
ORDER BY (timestamp, user_id);
