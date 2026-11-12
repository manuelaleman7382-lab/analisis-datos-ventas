select CASE
when discount = 0 then 'Sin descuento'
when discount > 0 and discount <= 0.1 then '1-10%'
when discount > 0.1 and discount <= 0.2 then '10-20%'
when discount > 0.2 and discount <= 0.3 then '20-30%'
when discount > 0.3 and discount <= 0.4 then '30-40%'
when discount > 0.4 and discount <= 0.5 then '40-50%'
when discount > 0.5 and discount <= 0.6 then '50-60%'
when discount > 0.6 and discount <= 0.7 then '60-70%'
when discount > 0.7 and discount <= 0.8 then '70-80%'
when discount > 0.8 and discount <= 0.9 then '80-90%'
when discount > 0.9 and discount <= 1 then '90-100%'

end as descuento,
round((sum(profit)/sum(sales))*100.0,2) as margen
from vw_ventas
group by discount