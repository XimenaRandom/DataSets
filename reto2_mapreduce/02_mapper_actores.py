#!/usr/bin/env python3
"""Mapper del Reto 2: emite pares  actor<TAB>show_id  leyendo el CSV limpio por stdin.
Compatible con Python 3.6 en adelante."""
import csv
import io
import sys

# UTF-8 explícito (tildes), compatible con Python 3.6
entrada = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", newline="")
salida = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")

IDX_SHOW_ID = 0
IDX_CAST = 4  # posición por defecto de 'cast' en netflix_clean.csv

for fila in csv.reader(entrada):
    if not fila:
        continue
    # Omitir la cabecera (y detectar la posición real de las columnas)
    if fila[0].strip() == "show_id":
        if "cast" in fila:
            IDX_CAST = fila.index("cast")
        continue
    if len(fila) <= IDX_CAST:
        continue
    show_id = fila[IDX_SHOW_ID].strip()
    cast = fila[IDX_CAST].strip()
    if not show_id or not cast:
        continue
    for actor in cast.split(","):
        actor = actor.strip().replace("\t", " ")
        if actor:  # excluir nombres vacíos
            salida.write("{}\t{}\n".format(actor, show_id))

salida.flush()