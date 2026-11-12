select customer_name as cliente, round(sum(sales),2) as venta_cliente from vw_ventas
group by customer_id order by round(sum(sales),2) desc limit 10