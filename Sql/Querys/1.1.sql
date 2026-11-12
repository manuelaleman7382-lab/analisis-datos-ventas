select count(*) as ventas_totales_mensuales, substr(order_date,1,7) as año_mes from vw_ventas
group by substr(order_date, 1, 4), substr(order_date, 1,7)