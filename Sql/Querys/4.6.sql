SELECT ship_mode as tipo_envio, round(avg(dias_envio),2) as tiempo_prom_envio from vw_ventas
group by tipo_envio