select count(*) as pedidos, 
customer_name as nombre,
sum(is_returned) as devoluciones,
round(100.0*sum(is_returned)/ count(*),2) as porcentaje_devolucion from vw_pedidos
group by customer_id, customer_name order by porcentaje_devolucion desc