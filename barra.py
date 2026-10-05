#!/usr/bin/env python3
"""A barra das quatro partes: a mesma em toda página, com a atual marcada.

O material tem quatro páginas e nenhuma pode ser beco sem saída: os degraus
(a história de Olá, Mundo!), a placa (a mesma história rodando), a escada (as
peças de que a máquina é feita) e a bancada (montar as peças com a mão). Os
quatro geradores chamam `barra(atual)` e colam `CSS` na folha de estilo; a
barra não usa variável de cor de ninguém, só a cor do texto da página, para
valer igual nas três peles.
"""
import html

PARTES = [
    ("degraus", "index.html", "os degraus"),
    ("placa", "placa.html", "a placa"),
    ("escada", "escada.html", "a escada"),
    ("bancada", "bancada.html", "a bancada"),
]

CSS = """
.partes{display:flex;flex-wrap:wrap;gap:.2rem 1.1rem;font-size:.85rem;line-height:1.4;padding:0 0 .4rem;margin:0;border-bottom:1px solid rgba(128,128,128,.3)}
.partes a{color:inherit;opacity:.62;text-decoration:none;padding:.15rem 0;border-bottom:2px solid transparent}
.partes a:hover{opacity:1;text-decoration:underline}
.partes a[aria-current]{opacity:1;font-weight:600;border-bottom-color:currentColor}
"""


def barra(atual):
    if atual not in [p[0] for p in PARTES]:
        raise SystemExit(f"ABORTADO: barra('{atual}'): parte desconhecida")
    elos = []
    for chave, arquivo, nome in PARTES:
        marca = ' aria-current="page"' if chave == atual else ""
        elos.append(f'<a href="{arquivo}"{marca}>{html.escape(nome)}</a>')
    return '<nav class="partes" aria-label="As quatro partes">' + "".join(elos) + "</nav>"
