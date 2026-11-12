select round(sum(sales),2) as ventas, round(sum(profit),2) as ganancias, round((sum(profit)/sum(sales))*100.0,2) as margen, sub_category as categoria from vw_ventas
group by sub_category