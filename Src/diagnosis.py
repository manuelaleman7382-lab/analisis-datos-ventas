from pathlib import Path
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "data" / "raw" / "superstore_raw.xls"
hojas = pd.read_excel(ruta, sheet_name=None, engine="xlrd")

orders = hojas["Orders"]
people = hojas["People"]
returns = hojas["Returns"]

print("\n--- 1. Texto con espacios sobrantes ---")
for col in orders.select_dtypes(include=["object", "string"]).columns:
    serie = orders[col].dropna().astype(str)
    n = (serie != serie.str.strip()).sum()
    if n:
        print(f"{col}: {n} valores con espacios al inicio o al final")

print("\n--- 2. Postal Code: tipos mezclados ---")
print(orders["Postal Code"].map(lambda x: type(x).__name__).value_counts())
largo = orders["Postal Code"].astype(str).str.replace(r"\.0$", "", regex=True).str.len()
print("Longitudes:", largo.value_counts().to_dict())

print("\n--- 3. Categorías ---")
for col in ["Ship Mode", "Segment", "Country/Region", "Region", "Category", "Sub-Category"]:
    print(f"\n{col}:")
    print(orders[col].value_counts(dropna=False))

print("\n--- 4. Fechas ---")
print("Rango de pedidos:", orders["Order Date"].min().date(), "->", orders["Order Date"].max().date())
print("Envíos antes del pedido:", (orders["Ship Date"] < orders["Order Date"]).sum())
dias = (orders["Ship Date"] - orders["Order Date"]).dt.days
print("Días de envío (mín, máx):", dias.min(), dias.max())

print("\n--- 5. Rangos numéricos ---")
print(orders[["Sales", "Quantity", "Discount", "Profit"]].describe().round(2))
print("Descuento fuera de [0, 1]:", ((orders["Discount"] < 0) | (orders["Discount"] > 1)).sum())
print("Ventas <= 0:", (orders["Sales"] <= 0).sum(), "| Cantidad <= 0:", (orders["Quantity"] <= 0).sum())
print("Filas con pérdida (Profit < 0):", (orders["Profit"] < 0).sum())

print("\n--- 6. Consistencia de llaves ---")
print("Row ID único:", orders["Row ID"].is_unique)
print("Customer ID con más de un nombre:", (orders.groupby("Customer ID")["Customer Name"].nunique() > 1).sum())
print("Customer ID con más de un segmento:", (orders.groupby("Customer ID")["Segment"].nunique() > 1).sum())
print("Product ID con más de un nombre:", (orders.groupby("Product ID")["Product Name"].nunique() > 1).sum())
print("Product ID con más de una subcategoría:", (orders.groupby("Product ID")["Sub-Category"].nunique() > 1).sum())
print("Order ID con más de un cliente:", (orders.groupby("Order ID")["Customer ID"].nunique() > 1).sum())
print("Order ID con más de una fecha:", (orders.groupby("Order ID")["Order Date"].nunique() > 1).sum())
print("Pedidos únicos:", orders["Order ID"].nunique(), "| Clientes:", orders["Customer ID"].nunique(),
      "| Productos:", orders["Product ID"].nunique())
print("Mismo producto repetido dentro de un pedido:", orders.duplicated(["Order ID", "Product ID"]).sum())

print("\n--- 7. Hojas People y Returns ---")
print("Regiones en Orders sin gerente en People:", set(orders["Region"]) - set(people["Region"]))
print("Order ID repetidos en Returns:", returns["Order ID"].duplicated().sum())
print("Order ID de Returns que no existen en Orders:", (~returns["Order ID"].isin(orders["Order ID"])).sum())
print("Valores de Returned:", returns["Returned"].value_counts().to_dict())