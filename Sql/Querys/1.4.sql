select sum(sales) as ventas, sum(profit) as ganancias, substr(order_date,1,7) as año_mes from vw_ventas
group by anio, mes