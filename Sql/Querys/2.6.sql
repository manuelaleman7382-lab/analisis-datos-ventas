select product_name, sum(quantity) as volumen_venta from vw_ventas
group by product_id