"""
Ejecuta las consultas de sql/03_consultas.sql y muestra los resultados.

Uso (desde la raíz del proyecto):
    python Src\\consultar.py        -> todas las consultas
    python Src\\consultar.py 3      -> solo la Q3
"""
import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DB = RAIZ / "data" / "superstore.db"
CONSULTAS = RAIZ / "sql" / "03_consultas.sql"
MAX_FILAS = 15


def formato(valor):
    if valor is None:
        return "-"
    if isinstance(valor, float):
        return f"{valor:,.2f}"
    return str(valor)


def imprimir(columnas, filas):
    filas = [[formato(v) for v in fila] for fila in filas]
    anchos = [max(len(c), *(len(f[i]) for f in filas)) if filas else len(c)
              for i, c in enumerate(columnas)]
    print("  " + " | ".join(c.ljust(a) for c, a in zip(columnas, anchos)))
    print("  " + "-+-".join("-" * a for a in anchos))
    for fila in filas:
        print("  " + " | ".join(v.ljust(a) for v, a in zip(fila, anchos)))


def main():
    if not DB.exists():
        raise SystemExit("No existe la base. Ejecuta primero: python Src\\crear_base.py")
    con = sqlite3.connect(DB)
    bloques = [b.strip() for b in CONSULTAS.read_text(encoding="utf-8").split(";") if b.strip()]
    solo = f"Q{sys.argv[1]}." if len(sys.argv) > 1 else None

    for bloque in bloques:
        titulo = next((l[2:].strip() for l in bloque.splitlines() if l.startswith("-- Q")), "Consulta")
        if solo and not titulo.startswith(solo):
            continue
        cursor = con.execute(bloque)
        columnas = [d[0] for d in cursor.description]
        filas = cursor.fetchall()
        print(f"\n{titulo}  ({len(filas)} filas)")
        imprimir(columnas, filas[:MAX_FILAS])
        if len(filas) > MAX_FILAS:
            print(f"  ... y {len(filas) - MAX_FILAS} filas más")
    con.close()


if __name__ == "__main__":
    main()
