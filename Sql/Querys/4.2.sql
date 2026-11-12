select state_province as estado, round(sum(profit),2) as ganacias from vw_ventas
group by state_province order by round(sum(profit),2) desc limit 10