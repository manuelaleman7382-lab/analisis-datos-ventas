select sum(sales) as ventas_ranking, substr(order_date, 1,7) as año_mes from vw_ventas
group by anio, mes order by ventas desc limit 5