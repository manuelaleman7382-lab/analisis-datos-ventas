select customers.customer_name as cliente,
count(DISTINCT order_items.order_key) as pedidos,
min(orders.order_date) as primer_pedido, 
max(orders.order_date) as ultimo_pedido,
round(sum(order_items.sales),2) as ventas_totales
from order_items
join orders on order_items.order_key = orders.order_key
join customers on customers.customer_id = orders.customer_id
group by customers.customer_id