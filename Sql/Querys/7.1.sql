select round(sum(order_items.sales),2) as ventas,
round(sum(order_items.profit),2) as ganancia,
products.category as categoria,
regions.regional_manager as manager from order_items
join orders on orders.order_key = order_items.order_key 
join regions on regions.region = orders.region
join products on products.product_id = order_items.product_id
group by manager, categoria