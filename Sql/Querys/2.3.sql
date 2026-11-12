select product_name as productos_con_perdida, round(sum(profit),2) as perdida from vw_ventas
group by product_id having perdida < 0 order by perdida desc