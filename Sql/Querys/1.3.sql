select round(sum(profit)/sum(sales)*100.0,2) as margen , substr(order_date,1,7) as año_mes from vw_ventas
group by substr(order_date, 1, 4), substr(order_date, 1,7)