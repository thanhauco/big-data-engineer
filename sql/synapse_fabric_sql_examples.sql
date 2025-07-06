-- Synapse / Fabric pattern: create a curated sales table in a lakehouse-compatible warehouse
CREATE TABLE SalesFact (
    event_id VARCHAR(64),
    customer_id VARCHAR(64),
    order_id VARCHAR(64),
    event_ts TIMESTAMP,
    amount DECIMAL(18,2),
    region VARCHAR(64),
    date_partition DATE
)
WITH (
    DISTRIBUTION = HASH(customer_id),
    CLUSTERED COLUMNSTORE INDEX
);

-- Sample incremental load pattern
INSERT INTO SalesFact (event_id, customer_id, order_id, event_ts, amount, region, date_partition)
SELECT
    event_id,
    customer_id,
    order_id,
    CAST(event_ts AS TIMESTAMP),
    CAST(amount AS DECIMAL(18,2)),
    region,
    CAST(date_partition AS DATE)
FROM
    dbo.RawTelemetry
WHERE
    date_partition = CAST(GETDATE() AS DATE);

-- Aggregation for daily revenue reporting
SELECT
    date_partition,
    region,
    SUM(amount) AS total_revenue,
    COUNT(DISTINCT order_id) AS orders
FROM SalesFact
GROUP BY date_partition, region
ORDER BY date_partition DESC, total_revenue DESC;

-- OneLake / Fabric view pattern
CREATE VIEW vw_daily_sales AS
SELECT
    date_partition,
    region,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value
FROM SalesFact
GROUP BY date_partition, region;
