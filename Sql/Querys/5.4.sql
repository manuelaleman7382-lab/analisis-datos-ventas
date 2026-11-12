select count(*), region from vw_pedidos
where is_returned = 1 group by region order by count(*) desc