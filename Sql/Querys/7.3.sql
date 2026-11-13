select c.customer_id, c.customer_name from customers c
left join orders o 
on o.customer_id = c.customer_id
AND o.order_date >= '2026-01-01'
AND o.order_date <  '2027-01-01'
where o.order_key is null
order by c.customer_name