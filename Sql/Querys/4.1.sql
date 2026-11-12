select region, round(sum(sales),2) as ventas, round(sum(profit),2) as ganacias from vw_ventas
group by region 