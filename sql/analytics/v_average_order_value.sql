CREATE OR REPLACE VIEW analytics_dw.v_average_order_value
AS SELECT avg(t.order_total) AS average_order_value
   FROM ( SELECT fs.order_id,
            sum(fs.quantity::numeric * p.price) AS order_total
           FROM analytics_dw.fact_sales fs
             JOIN analytics_dw.dim_products p ON fs.product_id = p.product_id
          GROUP BY fs.order_id) t;