select customer_name as cliente, round(sum(profit),2) as ganancias_cliente from vw_ventas
group by customer_id order by round(sum(profit),2) ASC limit 10