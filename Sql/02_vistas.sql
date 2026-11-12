-- =====================================================================
-- Vistas para análisis y para Power BI
--   vw_ventas  : una fila por línea de pedido, con todos los datos descriptivos
--   vw_pedidos : una fila por pedido, con totales
-- =====================================================================

CREATE VIEW vw_ventas AS
SELECT
    i.row_id,
    o.order_key,
    o.order_id,
    o.order_date,
    CAST(strftime('%Y', o.order_date) AS INTEGER)  AS anio,
    CAST(strftime('%m', o.order_date) AS INTEGER)  AS mes,
    strftime('%Y-%m', o.order_date)                AS anio_mes,
    CAST(julianday(o.ship_date) - julianday(o.order_date) AS INTEGER) AS dias_envio,
    o.ship_mode,
    o.is_returned,
    c.customer_id,
    c.customer_name,
    c.segment,
    o.country_region,
    o.state_province,
    o.city,
    o.region,
    r.regional_manager,
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    i.sales,
    i.quantity,
    i.discount,
    i.profit
FROM order_items i
JOIN orders    o ON o.order_key   = i.order_key
JOIN customers c ON c.customer_id = o.customer_id
JOIN products  p ON p.product_id  = i.product_id
JOIN regions   r ON r.region      = o.region;

CREATE VIEW vw_pedidos AS
SELECT
    o.order_key,
    o.order_id,
    o.order_date,
    CAST(strftime('%Y', o.order_date) AS INTEGER)  AS anio,
    CAST(strftime('%m', o.order_date) AS INTEGER)  AS mes,
    CAST(julianday(o.ship_date) - julianday(o.order_date) AS INTEGER) AS dias_envio,
    o.ship_mode,
    o.is_returned,
    c.customer_id,
    c.customer_name,
    c.segment,
    o.region,
    r.regional_manager,
    COUNT(*)           AS lineas,
    SUM(i.quantity)    AS unidades,
    SUM(i.sales)       AS ventas,
    SUM(i.profit)      AS ganancia
FROM orders o
JOIN order_items i ON i.order_key   = o.order_key
JOIN customers   c ON c.customer_id = o.customer_id
JOIN regions     r ON r.region      = o.region
GROUP BY o.order_key, o.order_id, o.order_date, o.ship_date, o.ship_mode, o.is_returned,
         c.customer_id, c.customer_name, c.segment, o.region, r.regional_manager;
