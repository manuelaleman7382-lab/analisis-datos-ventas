select count(*) as pedidos, 
anio as año,
sum(is_returned) as devoluciones,
round(100.0*sum(is_returned)/ count(*),2) as porcentaje_devolucion from vw_pedidos
group by anio order by  anio asc