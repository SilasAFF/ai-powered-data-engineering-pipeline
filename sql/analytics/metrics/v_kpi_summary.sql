-- Metrics Layer
-- Core business KPIs aggregated at monthly level
-- This view represents the single source of truth for executive metrics
CREATE OR REPLACE VIEW analytics_dw.v_kpi_summary
AS SELECT date_trunc('month'::text, f.order_date::timestamp with time zone)::date AS month,
    count(DISTINCT f.order_id) AS total_orders,
    sum(f.quantity) AS total_units_sold,
    sum(f.quantity::numeric * p.price) AS total_revenue,
    round(sum(f.quantity::numeric * p.price) / count(DISTINCT f.order_id)::numeric, 2) AS average_order_value
   FROM analytics_dw.fact_sales f
     JOIN analytics_dw.dim_products p ON f.product_id = p.product_id
  GROUP BY (date_trunc('month'::text, f.order_date::timestamp with time zone))
  ORDER BY (date_trunc('month'::text, f.order_date::timestamp with time zone)::date);