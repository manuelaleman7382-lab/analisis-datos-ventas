from pathlib import Path
import pandas as pd
import os

os.system("cls" if os.name == "nt" else "clear")

RAIZ = Path(__file__).resolve().parent.parent
ruta = RAIZ / "data" / "raw" / "superstore_raw.xls"

hojas = pd.read_excel(ruta, sheet_name=None, engine="xlrd")

for nombre, df in hojas.items():
    print("=" * 60)
    print(f"HOJA: {nombre}  |  filas: {df.shape[0]}  columnas: {df.shape[1]}")
    print("\nTipos de dato:")
    print(df.dtypes)
    print("\nPrimeras filas:")
    print(df.head())
    print("\nValores nulos por columna:")
    print(df.isna().sum()[df.isna().sum() > 0])
    print("\nFilas duplicadas:", df.duplicated().sum())