select count(order_id) as pedidos_devueltos from vw_pedidos
where is_returned = 1
