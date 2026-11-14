#!/usr/bin/env python3
"""Reducer del Reto 2: cuenta show_id DISTINTOS por actor.
Entrada (agrupada por actor por Hadoop): actor<TAB>show_id
Salida: actor<TAB>cantidad_titulos
Compatible con Python 3.6 en adelante."""
import io
import sys

entrada = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
salida = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")

actor_actual = None
ids = set()

for linea in entrada:
    linea = linea.rstrip("\n")
    if not linea:
        continue
    actor, _, show_id = linea.partition("\t")
    if actor != actor_actual:
        if actor_actual is not None:
            salida.write("{}\t{}\n".format(actor_actual, len(ids)))
        actor_actual = actor
        ids = set()
    ids.add(show_id)

if actor_actual is not None:
    salida.write("{}\t{}\n".format(actor_actual, len(ids)))

salida.flush()