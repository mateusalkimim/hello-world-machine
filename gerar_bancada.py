#!/usr/bin/env python3
"""Gera pt/bancada.html — a bancada de circuitos dentro do material.

A fonte é `bancada/bancada.html`, uma página inteira que anda sozinha, e ela
fica como chegou. Este gerador não toca no jogo: cola a barra das quatro
partes no alto e veste a página com a pele das outras três
(`bancada/pele-itaca.css`: cores, fontes, cabeçalho). Cada troca é conferida
pela contagem: se a fonte mudar e a marca sumir, aborta em vez de gerar uma
página meio vestida. Só biblioteca padrão.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import barra as BARRA  # noqa: E402

FONTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500'
          '&family=Inter:wght@400;500;600&family=Spline+Sans+Mono:wght@400;500&display=swap">')
REDESENHAR = "buildPalette();buildParts();buildTrilha();draw();"

# (marca na fonte, quantas vezes ela tem de aparecer, o que entra no lugar)
TROCAS = [
    # as fontes da casa no lugar da fonte da bancada
    ('<link rel="preconnect" href="https://fonts.googleapis.com">\n', 1, ""),
    ('<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">', 1, FONTES),
    ('"IBM Plex Sans"', 7, '"Inter"'),
    # a tinta escura fixa do desenho passa a ser o azul-noite da casa
    ("#1B1F24", 7, "#0a1424"),
    # o cabeçalho no molde das outras páginas
    ("  <h1>Bancada de circuitos</h1>\n",
     1, '  <div><p class="eyebrow">hello-world-machine · bancada</p><h1>Bancada de circuitos</h1></div>\n'),
    # os rótulos das peças são desenhados antes de a fonte chegar: redesenha quando ela chega
    ('addEventListener("change",()=>{' + REDESENHAR + "}); }\n",
     1, 'addEventListener("change",()=>{' + REDESENHAR + "}); }\n"
        "if(document.fonts&&document.fonts.ready){ document.fonts.ready.then(()=>{" + REDESENHAR + "}); }\n"),
]


def main():
    fonte = open(os.path.join(AQUI, "bancada", "bancada.html"), encoding="utf-8").read()
    pele = open(os.path.join(AQUI, "bancada", "pele-itaca.css"), encoding="utf-8").read()
    pagina = fonte
    for marca, vezes, novo in TROCAS + [("</style>", 1, None), ("<main>\n", 1, None)]:
        if fonte.count(marca) != vezes:
            sys.stderr.write(f"ABORTADO: esperava {vezes} ocorrência(s) de {marca[:60]!r} na bancada, achei {fonte.count(marca)}\n")
            return 1
        if novo is not None:
            pagina = pagina.replace(marca, novo)
    pagina = pagina.replace("</style>", pele + BARRA.CSS + "</style>")
    pagina = pagina.replace("<main>\n", "<main>\n" + BARRA.barra("bancada") + "\n")
    saida = os.path.join(AQUI, "pt", "bancada.html")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print(f"pt/bancada.html: {len(pagina)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
