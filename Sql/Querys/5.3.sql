select round(100.0*sum(is_returned)/count(order_id),2) from vw_pedidos
