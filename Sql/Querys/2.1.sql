select round(sum(sales),2) as ventas, round(sum(profit),2) as ganancias, category as categoria from vw_ventas
group by category 