select count(DISTINCT order_key ) as devoluciones, category as categoria, sub_category as subcategoria from vw_ventas
where is_returned = 1 group by category, sub_category