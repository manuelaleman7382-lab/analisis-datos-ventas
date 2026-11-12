select ship_mode as tipo_envio, round(sum(profit),2) as ganancias_por_envio from vw_ventas
group by ship_mode order by round(sum(profit),2) 