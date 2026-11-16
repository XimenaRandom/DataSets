"""Reúne las partes descargadas de HDFS (part-*) en mapreduce_actores.csv."""
import glob
import os
import sys

import pandas as pd

carpeta = sys.argv[1] if len(sys.argv) > 1 else "resultado_hdfs"
salida = sys.argv[2] if len(sys.argv) > 2 else "mapreduce_actores.csv"

partes = sorted(glob.glob(os.path.join(carpeta, "part-*")))
if not partes:
    sys.exit(f"No se encontraron archivos part-* en '{carpeta}'")

# keep_default_na=False: evita que un actor llamado 'NA' o 'None' se vuelva nulo
df = pd.concat(
    (pd.read_csv(p, sep="\t", header=None, names=["actor", "cantidad_titulos"],
                 encoding="utf-8", keep_default_na=False, dtype={"actor": str})
     for p in partes),
    ignore_index=True,
)

# Por si un actor llegó en varias partes: se suma (con 1 reducer no ocurre)
df = df.groupby("actor", as_index=False)["cantidad_titulos"].sum()
df = df.sort_values(["cantidad_titulos", "actor"], ascending=[False, True]).reset_index(drop=True)
df.to_csv(salida, index=False, encoding="utf-8")

print(f"Partes leídas: {len(partes)}")
print(f"Actores (filas) en {salida}: {len(df)}")
print("\nTabla 2 - Diez primeros actores:")
top = df.head(10).copy()
top.insert(0, "Posición", range(1, len(top) + 1))
print(top.to_string(index=False))
