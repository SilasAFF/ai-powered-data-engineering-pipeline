CREATE OR REPLACE VIEW analytics_dw.v_total_revenue
AS SELECT sum(fs.quantity::numeric * p.price) AS total_revenue
   FROM analytics_dw.fact_sales fs
     JOIN analytics_dw.dim_products p ON fs.product_id = p.product_id;