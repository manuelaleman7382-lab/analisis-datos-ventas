"""
Crea la base de datos SQLite a partir de los CSV limpios.

Uso (desde la raíz del proyecto):
    python Src\\crear_base.py

Resultado: data/superstore.db (se vuelve a crear desde cero cada vez que se ejecuta).
"""
import csv
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DB = RAIZ / "data" / "superstore.db"
PROCESADOS = RAIZ / "data" / "processed"
SQL = RAIZ / "sql"

# Orden de carga: primero las tablas de las que dependen las demás
ORDEN = ["regions", "customers", "products", "orders", "order_items"]


def leer_csv(ruta):
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        columnas = next(lector)
        filas = [[None if valor == "" else valor for valor in fila] for fila in lector]
    return columnas, filas


def main():
    try:
        if DB.exists():
            DB.unlink()
    except PermissionError:
        raise SystemExit(f"No se pudo reemplazar {DB.name}. Cierra el programa que lo tenga abierto "
                         "(DB Browser, la extensión de SQLite, etc.) y vuelve a intentar.")

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript((SQL / "01_esquema.sql").read_text(encoding="utf-8"))

    for tabla in ORDEN:
        columnas, filas = leer_csv(PROCESADOS / f"{tabla}.csv")
        marcadores = ", ".join("?" * len(columnas))
        con.executemany(f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES ({marcadores})", filas)
        print(f"  {tabla}: {len(filas)} filas cargadas")
    con.commit()

    con.executescript((SQL / "02_vistas.sql").read_text(encoding="utf-8"))

    problemas = con.execute("PRAGMA foreign_key_check").fetchall()
    print("Revisión de llaves foráneas:", "OK" if not problemas else f"{len(problemas)} problemas")
    print("Filas en vw_ventas:", con.execute("SELECT COUNT(*) FROM vw_ventas").fetchone()[0])
    con.close()
    print("Base creada en", DB)


if __name__ == "__main__":
    main()
