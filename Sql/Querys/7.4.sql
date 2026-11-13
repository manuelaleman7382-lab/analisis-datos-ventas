SELECT p.category AS categoria,
       ROUND(SUM(CASE WHEN o.is_returned = 1 THEN i.sales ELSE 0 END), 2) AS ventas_devueltas,
       ROUND(SUM(i.sales), 2)                                             AS ventas_totales,
       ROUND(100.0 * SUM(CASE WHEN o.is_returned = 1 THEN i.sales ELSE 0 END)
             / SUM(i.sales), 2)                                           AS porcentaje_devuelto
FROM order_items i
JOIN products p ON p.product_id = i.product_id
JOIN orders   o ON o.order_key  = i.order_key
GROUP BY p.category
ORDER BY porcentaje_devuelto DESC;