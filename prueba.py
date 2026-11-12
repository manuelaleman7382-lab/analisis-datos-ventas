from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent
ruta = RAIZ / "data" / "raw" / "superstore_raw.xls"
print("Buscando en:", ruta, "| existe:", ruta.exists())

hojas = pd.read_excel(ruta, sheet_name=None, engine="xlrd")
for nombre, tabla in hojas.items():
    print(nombre, tabla.shape)