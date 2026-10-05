#!/usr/bin/env python3
"""Gera pt/bancada.html — a bancada de circuitos dentro do material.

A fonte é `bancada/bancada.html`, uma página inteira que anda sozinha. Este
gerador não toca no jogo: só cola a barra das quatro partes no alto, para a
bancada deixar de ser uma página solta. Só biblioteca padrão.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import barra as BARRA  # noqa: E402


def main():
    fonte = open(os.path.join(AQUI, "bancada", "bancada.html"), encoding="utf-8").read()
    for marca in ("</style>", "<main>\n"):
        if fonte.count(marca) != 1:
            sys.stderr.write(f"ABORTADO: esperava UMA ocorrência de {marca!r} na bancada, achei {fonte.count(marca)}\n")
            return 1
    pagina = fonte.replace("</style>", BARRA.CSS + "</style>")
    pagina = pagina.replace("<main>\n", "<main>\n" + BARRA.barra("bancada") + "\n")
    saida = os.path.join(AQUI, "pt", "bancada.html")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print(f"pt/bancada.html: {len(pagina)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
