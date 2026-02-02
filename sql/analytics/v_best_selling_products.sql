CREATE OR REPLACE VIEW analytics_dw.v_best_selling_products
AS SELECT dp.product_id,
    dp.title,
    sum(fs.quantity) AS total_units_sold
   FROM analytics_dw.fact_sales fs
     JOIN analytics_dw.dim_products dp ON fs.product_id = dp.product_id
  GROUP BY dp.product_id, dp.title
  ORDER BY (sum(fs.quantity)) DESC;