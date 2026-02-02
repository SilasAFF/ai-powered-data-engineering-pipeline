CREATE OR REPLACE VIEW analytics_dw.v_daily_revenue
AS SELECT fs.order_date,
    sum(fs.quantity::numeric * p.price) AS daily_revenue
   FROM analytics_dw.fact_sales fs
     JOIN analytics_dw.dim_products p ON fs.product_id = p.product_id
  GROUP BY fs.order_date
  ORDER BY fs.order_date;