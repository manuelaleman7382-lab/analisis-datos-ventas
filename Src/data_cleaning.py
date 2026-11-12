from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "data" / "raw" / "superstore_raw.xls"
SALIDA = RAIZ / "data" / "processed"

COLUMNAS_TEXTO = ["order_id", "ship_mode", "customer_id", "customer_name", "segment",
                  "country_region", "city", "state_province", "region", "product_id",
                  "category", "sub_category", "product_name"]
ATRIBUTOS_PEDIDO = ["order_id", "customer_id", "order_date", "ship_date", "ship_mode",
                    "country_region", "city", "state_province", "postal_code", "region"]


def nombre_snake(columna):
    return (columna.strip().lower().replace("/", "_").replace("-", "_").replace(" ", "_"))


def limpiar_texto(serie):
    """Quita espacios al inicio y al final y colapsa espacios repetidos."""
    return serie.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)


def limpiar(hojas):
    reporte = []
    orders = hojas["Orders"].copy()
    orders.columns = [nombre_snake(c) for c in orders.columns]
    n_filas = len(orders)

    # 1) Texto homogéneo
    for col in COLUMNAS_TEXTO:
        orders[col] = limpiar_texto(orders[col])

    # 2) Código postal como texto. EE. UU. = 5 dígitos (se recupera el cero inicial perdido);
    #    Canadá se deja tal cual, porque es alfanumérico.
    cp = (orders["postal_code"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True))
    es_eeuu = orders["country_region"] == "United States"
    recuperados = (es_eeuu & (cp.str.len() < 5)).sum()
    orders["postal_code"] = cp.where(~es_eeuu, cp.str.zfill(5)).str.upper()
    reporte.append(f"Códigos postales de EE. UU. completados con ceros a la izquierda: {recuperados}")

    # 3) Fechas
    for col in ["order_date", "ship_date"]:
        orders[col] = pd.to_datetime(orders[col])
    hoy = pd.Timestamp.today().normalize()
    futuros = (orders["order_date"] > hoy).sum()
    reporte.append(f"Filas con fecha de pedido posterior a hoy (se conservan): {futuros}")

    # 4) Productos: un nombre por product_id (el más frecuente; si empatan, el más reciente)
    frecuencia = (orders.groupby(["product_id", "product_name"])
                  .agg(veces=("row_id", "count"), ultima=("order_date", "max")).reset_index())
    varios = frecuencia.groupby("product_id")["product_name"].transform("nunique") > 1
    revision_productos = frecuencia[varios].sort_values(["product_id", "veces"], ascending=[True, False])
    frecuencia = frecuencia.sort_values(["product_id", "veces", "ultima"], ascending=[True, False, False])
    nombres = frecuencia.drop_duplicates("product_id")[["product_id", "product_name"]]
    atributos = orders.drop_duplicates("product_id")[["product_id", "category", "sub_category"]]
    products = nombres.merge(atributos, on="product_id").sort_values("product_id").reset_index(drop=True)
    reporte.append(f"Productos con más de un nombre unificados: {revision_productos['product_id'].nunique()}")

    # 5) Clientes
    customers = (orders.drop_duplicates("customer_id")[["customer_id", "customer_name", "segment"]]
                 .sort_values("customer_id").reset_index(drop=True))

    # 6) Pedidos: llave sustituta por (order_id, customer_id), porque algunos order_id
    #    aparecen con dos clientes distintos.
    pares = (orders[["order_id", "customer_id"]].drop_duplicates()
             .sort_values(["order_id", "customer_id"]).reset_index(drop=True))
    pares["order_key"] = pares.index + 1
    orders = orders.merge(pares, on=["order_id", "customer_id"], how="left")
    reporte.append(f"Order ID compartidos por más de un cliente: {len(pares) - pares['order_id'].nunique()}")

    for col in ATRIBUTOS_PEDIDO:
        if col in ("order_id", "customer_id"):
            continue
        conflictos = (orders.groupby("order_key")[col].nunique() > 1).sum()
        if conflictos:
            reporte.append(f"AVISO: {conflictos} pedidos con más de un valor en '{col}' (se usa el de la primera fila)")

    pedidos = (orders.sort_values("row_id").drop_duplicates("order_key")
               [["order_key"] + ATRIBUTOS_PEDIDO].sort_values("order_key").reset_index(drop=True))

    # 7) Devoluciones: se convierten en una marca dentro de pedidos
    devueltos = set(limpiar_texto(hojas["Returns"]["Order ID"]))
    pedidos["is_returned"] = pedidos["order_id"].isin(devueltos).astype(int)
    reporte.append(f"Pedidos marcados como devueltos: {pedidos['is_returned'].sum()}")

    # 8) Líneas de pedido
    order_items = (orders[["row_id", "order_key", "product_id", "sales", "quantity", "discount", "profit"]]
                   .sort_values("row_id").reset_index(drop=True))
    repetidos = orders.duplicated(["order_key", "product_id"]).sum()
    reporte.append(f"Líneas con el mismo producto repetido dentro de un pedido (se conservan): {repetidos}")

    # 9) Regiones y gerentes
    regions = hojas["People"].copy()
    regions.columns = [nombre_snake(c) for c in regions.columns]
    for col in regions.columns:
        regions[col] = limpiar_texto(regions[col])

    # 10) Controles de integridad
    assert len(order_items) == n_filas, "Se perdieron o duplicaron líneas"
    assert order_items["row_id"].is_unique
    assert pedidos["order_key"].is_unique
    assert customers["customer_id"].is_unique
    assert products["product_id"].is_unique
    assert order_items["order_key"].isin(pedidos["order_key"]).all()
    assert order_items["product_id"].isin(products["product_id"]).all()
    assert pedidos["customer_id"].isin(customers["customer_id"]).all()
    assert pedidos["region"].isin(regions["region"]).all()
    reporte.append("Controles de integridad: OK")

    for col in ["order_date", "ship_date"]:
        pedidos[col] = pedidos[col].dt.strftime("%Y-%m-%d")

    tablas = {"customers": customers, "products": products, "regions": regions,
              "orders": pedidos, "order_items": order_items}
    return tablas, revision_productos, reporte


def main():
    hojas = pd.read_excel(ENTRADA, sheet_name=None, engine="xlrd")
    tablas, revision_productos, reporte = limpiar(hojas)

    SALIDA.mkdir(parents=True, exist_ok=True)
    for nombre, tabla in tablas.items():
        tabla.to_csv(SALIDA / f"{nombre}.csv", index=False, encoding="utf-8")
    revision_productos.to_csv(SALIDA / "revision_productos_con_varios_nombres.csv",
                              index=False, encoding="utf-8")

    print("REPORTE DE LIMPIEZA")
    for linea in reporte:
        print(" -", linea)
    print("\nArchivos escritos en", SALIDA)
    for nombre, tabla in tablas.items():
        print(f"  {nombre}.csv: {len(tabla)} filas, {tabla.shape[1]} columnas")


if __name__ == "__main__":
    main()