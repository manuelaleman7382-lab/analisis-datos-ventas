select product_name as producto, sum(profit) as ganancia from vw_ventas
group by product_id order by ganancia desc limit 10