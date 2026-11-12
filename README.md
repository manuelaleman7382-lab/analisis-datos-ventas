ANÁLISIS DE VENTAS SUPERSTORE: EXCEL -> SQL -> POWER BI

Proyecto de análisis de datos que recorre un flujo complejo: comienza en un archivo excel con datos de ventas, lo limpia y valida con Python (pandas), lo organiza en una base de datos SQL relacional para trabajarlo en SQLite con distintas consultas y presenta los resultados en un tablero de POWER BI

--------------- OBJETIVO -------------------- 
Responder a preguntas de negocios relacionadas con la cadena de ventas y dejar el proceso documentado en este repositorio Git

*¿Cómo evolucionan las ventas, la ganancia y el margen a lo largo del tiempo?
*¿Qué productos y subcategorías generan ganancia y cuáles generan perdidas?
*¿Cómo afectan los descuentos a la rentabilidad?
*Qué regiones, clientes y modos de envío tienen mejor desempeño?
*¿Qué porcentaje de pedidos se devuelven y donde?


-----------------QUERYS------------------------

1. Evolución de ventas, ganancias y margen

Objetivo: Analizar cómo ha evolucionado el negocio a lo largo del tiempo.

ID	Requisito	Resultado esperado
1.1	Agrupar las ventas por año y mes.	Ventas totales mensuales.
1.2	Calcular las ganancias totales por mes.	Ganancia mensual.
1.3	Calcular el margen de ganancia por mes.	Margen porcentual mensual.
1.4	Comparar las ventas y ganancias entre años.	Desempeño anual.
1.5	Identificar los 5 meses con mayores ventas.	Ranking de meses.

Pistas para resolverlo:

Utilizar funciones de fecha.
Utilizar funciones de agregación.
Calcular el margen como ganancia total / ventas totales * 100.
Considerar el orden cronológico de los resultados.
2. Productos y subcategorías rentables

Objetivo: Identificar qué productos generan valor y cuáles representan pérdidas.

ID	Requisito	Resultado esperado
2.1	Obtener las ventas y ganancias totales por categoría.	Rentabilidad por categoría.
2.2	Obtener ventas, ganancias y margen por subcategoría.	Ranking de subcategorías.
2.3	Identificar productos cuya ganancia acumulada sea negativa.	Productos que generan pérdidas.
2.4	Identificar los 10 productos con mayor ganancia.	Top 10 productos rentables.
2.5	Identificar los 10 productos con mayores pérdidas.	Productos menos rentables.
2.6	Calcular las unidades vendidas por producto.	Volumen de ventas por producto.

Pistas para resolverlo:

Agrupar por categoría, subcategoría o producto.
Utilizar SUM() para ventas, ganancias y unidades.
Investigar la diferencia entre WHERE y HAVING.
Utilizar ordenamiento ascendente o descendente.
Limitar los resultados para obtener rankings.
3. Impacto de los descuentos en la rentabilidad

Objetivo: Descubrir si los descuentos ayudan a vender más o perjudican las ganancias.

ID	Requisito	Resultado esperado
3.1	Agrupar los registros por nivel de descuento.	Ventas y ganancias por descuento.
3.2	Calcular el margen de ganancia para cada nivel de descuento.	Rentabilidad por descuento.
3.3	Comparar los descuentos y ganancias por categoría.	Categorías más afectadas.
3.4	Identificar productos con descuentos y ganancias negativas.	Productos problemáticos.
3.5	Identificar qué nivel de descuento tiene mayor ganancia promedio.	Descuento más rentable.

Pistas para resolverlo:

Investigar cómo funciona CASE WHEN.
Utilizar AVG() y SUM().
Crear rangos de descuentos: 0%, 1-10%, 11-20%, 21-30%, etc.
Diferenciar entre ganancia promedio por registro y ganancia total.
4. Desempeño de regiones, clientes y modos de envío

Objetivo: Identificar las áreas geográficas, clientes y métodos logísticos con mejores resultados.

ID	Requisito	Resultado esperado
4.1	Calcular ventas y ganancias por región.	Ranking de regiones.
4.2	Identificar los 10 estados con mayores ganancias.	Estados más rentables.
4.3	Identificar los 10 clientes con mayores ventas.	Clientes principales.
4.4	Identificar clientes que generan pérdidas.	Clientes no rentables.
4.5	Comparar las ganancias por modo de envío.	Rentabilidad logística.
4.6	Calcular el tiempo promedio entre la fecha del pedido y la fecha de envío.	Tiempo de envío por modalidad.

Pistas para resolverlo:

Utilizar GROUP BY.
Investigar COUNT(DISTINCT ...) para contar pedidos únicos.
Calcular la diferencia entre dos fechas.
Considerar que un cliente puede realizar múltiples pedidos.
5. Análisis de devoluciones

Objetivo: Identificar qué porcentaje de pedidos se devuelve y dónde ocurre con mayor frecuencia.

Tablas necesarias:

Orders o Superstore: información de los pedidos y ventas.
Returns: información de los pedidos devueltos.
ID	Requisito	Resultado esperado
5.1	Calcular el número total de pedidos.	Total de pedidos únicos.
5.2	Calcular el número de pedidos devueltos.	Pedidos devueltos.
5.3	Calcular el porcentaje general de devoluciones.	Tasa de devolución.
5.4	Calcular las devoluciones por región.	Regiones con más devoluciones.
5.5	Calcular las devoluciones por categoría y subcategoría.	Productos más devueltos.
5.6	Identificar clientes con mayor porcentaje de devoluciones.	Clientes con más devoluciones.
5.7	Comparar el porcentaje de devoluciones entre años.	Evolución de devoluciones.

Pistas para resolverlo:

Utilizar JOIN.
Investigar la diferencia entre INNER JOIN y LEFT JOIN.
Relacionar ambas tablas utilizando el identificador del pedido (Order ID).
Tener cuidado con los pedidos que contienen múltiples productos.
Utilizar COUNT(DISTINCT ...) para evitar contar pedidos repetidos.
6. Retos adicionales

Objetivo: Profundizar en el análisis y practicar conceptos SQL de nivel avanzado.

ID	Reto	Habilidad SQL
6.1	Identificar los productos que generan muchas ventas, pero poca ganancia.	Agregaciones y filtros
6.2	Encontrar los clientes que compraron más de 10 veces.	HAVING
6.3	Identificar los estados donde las ventas crecen año tras año.	Subconsultas o CTE
6.4	Encontrar la categoría más rentable de cada región.	Window Functions
6.5	Calcular el porcentaje que representa cada categoría sobre las ventas totales.	Subconsultas
6.6	Identificar los meses con ventas superiores al promedio mensual.	CTE y subconsultas
6.7	Crear un ranking de productos por ganancia dentro de cada categoría.	RANK() o ROW_NUMBER()
7. Seguimiento del proyecto

Utilizar esta lista para llevar el control de los ejercicios completados.

1. Evolución temporal
1.1 Ventas mensuales.
1.2 Ganancias mensuales.
1.3 Margen mensual.
1.4 Comparación anual.
1.5 Top 5 meses.
2. Productos
2.1 Rentabilidad por categoría.
2.2 Rentabilidad por subcategoría.
2.3 Productos con pérdidas.
2.4 Top 10 productos rentables.
2.5 Top 10 productos con pérdidas.
2.6 Unidades por producto.
3. Descuentos
3.1 Ventas por descuento.
3.2 Margen por descuento.
3.3 Descuentos por categoría.
3.4 Productos con pérdidas y descuentos.
3.5 Descuento más rentable.
4. Desempeño comercial
4.1 Regiones.
4.2 Estados.
4.3 Clientes principales.
4.4 Clientes con pérdidas.
4.5 Modos de envío.
4.6 Tiempo de envío.
5. Devoluciones
5.1 Pedidos totales.
5.2 Pedidos devueltos.
5.3 Porcentaje de devoluciones.
5.4 Devoluciones por región.
5.5 Devoluciones por categoría.
5.6 Devoluciones por cliente.
5.7 Evolución anual.
6. Retos avanzados
6.1 Productos con muchas ventas y poca ganancia.
6.2 Clientes con más de 10 pedidos.
6.3 Crecimiento de ventas por estado.
6.4 Categoría más rentable por región.
6.5 Participación de cada categoría en las ventas.
6.6 Meses por encima del promedio.
6.7 Ranking de productos por categoría.
8. Objetivos de aprendizaje

Al finalizar este proyecto se espera dominar los siguientes conceptos:

SQL básico:

SELECT
FROM
WHERE
ORDER BY
DISTINCT
LIMIT / TOP

Funciones de agregación:

SUM()
AVG()
COUNT()
MIN()
MAX()

SQL intermedio:

GROUP BY
HAVING
CASE WHEN
INNER JOIN
LEFT JOIN
Funciones de fecha

SQL avanzado:

Subconsultas
CTE (Common Table Expressions)
Window Functions
RANK()
ROW_NUMBER()
PARTITION BY
9. Resultado esperado del proyecto

Al completar todos los ejercicios, se deberá contar con un análisis de negocio que permita responder:

¿Las ventas y ganancias están creciendo con el tiempo?
¿Qué productos y subcategorías son más rentables?
¿Los descuentos están afectando negativamente los márgenes?
¿Qué regiones y clientes generan mayor valor?
¿Qué modos de envío ofrecen mejores resultados?
¿Qué porcentaje de pedidos se devuelve y cuáles son las áreas más afectadas?

Meta final: Desarrollar habilidades de SQL aplicadas a problemas reales de negocio y generar información que pueda utilizarse posteriormente en un dashboard de Business Intelligence.