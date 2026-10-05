#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere TODA citação do repositório contra o livro, caractere a caractere.

Alcança degraus.py (arestas, construções, 2ª testemunha) E conceitos.py (as
passagens que sustentam os quatro campos de cada degrau). A extensão para
conceitos.py entrou em 2026-08-27 junto com os campos: acrescentar 19 passagens
novas a um repositório cuja tese é "citação conferida", sem estendê-las ao
portão, seria furar a própria regra no ato de aplicá-la.

O README deste repositório afirma que toda citação foi verificada contra a
fonte. Afirmação sem instrumento é promessa — e promessa sem recibo é o defeito
que este mapa existe para não ter. Este é o recibo.

Os livros NÃO estão aqui (não são redistribuíveis). Aponte o acervo com:

    ACERVO=/caminho/do/acervo python3 conferir_citacoes.py

Sem acervo o script sai com código 2 e diz que não pôde conferir — ele nunca
devolve "ok" por ausência de prova.

Reticências (…) marcam elisão: cada trecho entre elas é conferido em separado,
que é o que a prática de citação permite. Não se normaliza palavra, ordem nem
pontuação — só espaço em branco e aspas/travessões tipográficos.
"""
import os
import re
import sys
import unicodedata

import degraus as D
import conceitos as CO
import familias as FA

ACERVO = os.environ.get("ACERVO", "")
LIVROS = {"petzold": "petzold-code-2ed/livro.md",
          # SICP dissecado em 2026-08-27 (epub nato-digital, mesma classe A do
          # Petzold). Antes disso as duas citações do SICP saíam como "sem a
          # fonte no acervo" — o portão dizia o que NÃO podia conferir em vez
          # de arredondar para "todas conferem".
          "sicp": "sicp-2ed/livro.md"}          # fonte → caminho no acervo

TIPOG = {"“": '"', "”": '"', "‘": "'", "’": "'",
         "—": "-", "–": "-", "…": "\x00", " ": " "}


def normalizar(s):
    s = unicodedata.normalize("NFC", s)
    for a, b in TIPOG.items():
        s = s.replace(a, b)
    return re.sub(r"[^\S\x00]+", " ", s).strip()


def main():
    if not ACERVO or not os.path.isdir(ACERVO):
        print("acervo ausente — não posso conferir. Use ACERVO=/caminho "
              "(os livros não são redistribuíveis e não vivem neste repo).",
              file=sys.stderr)
        return 2

    fontes = {}
    for f, rel in LIVROS.items():
        p = os.path.join(ACERVO, rel)
        if os.path.exists(p):
            fontes[f] = normalizar(open(p, encoding="utf-8").read())

    campos = []
    for chave, no in CO.CONCEITOS.items():
        for campo, _rot in CO.CAMPOS:
            texto, classe, ref, cit, ratificado = no[campo]
            if not cit:
                continue      # classe "ofício": não alega fonte, nada a conferir
            fonte = "sicp" if "SICP" in (ref or "") else "petzold"
            campos.append((f"campo {chave}.{campo}", fonte, cit))

    for fam in FA.FAMILIAS:
        for en, pt in fam["citacoes"]:
            campos.append((f"família {fam['id']}", fam["fonte"], en))
    itens = (campos
             + [(f"aresta {a[0]}→{a[1]}", a[3], a[5]) for a in D.ARESTAS]
             + [(f"construção {c[1]}", c[3], c[5]) for c in D.CONSTRUCAO]
             + [(f"2ª testemunha {k[0]}→{k[1]}", v[0], v[2])
                for k, v in D.SEGUNDA_TESTEMUNHA.items()])

    ok = mau = sem_fonte = 0
    for nome, fonte, cit in itens:
        if fonte not in fontes:
            sem_fonte += 1
            continue
        # cada trecho entre reticências é conferido em separado
        trechos = [t for t in normalizar(cit).split("\x00") if t.strip()]
        falhou = [t for t in trechos if t not in fontes[fonte]]
        if falhou:
            mau += 1
            print(f"  ✗ {nome}")
            for t in falhou:
                print(f"      não está na fonte: {t[:90]}")
        else:
            ok += 1

    # A ratificação também é MEDIDA, não alegada. A página estampa uma data em
    # cada campo de ofício; se a data não estiver na fonte, a página mente.
    import re as _re
    rat = prop = ruim_data = 0
    for chave, no in CO.CONCEITOS.items():
        for campo, _r in CO.CAMPOS:
            _t, classe, _ref, _c, quando = no[campo]
            if classe != "d":
                continue
            if not quando:
                prop += 1
            elif _re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(quando)):
                rat += 1
            else:
                ruim_data += 1
                print(f"  ✗ {chave}.{campo}: data de ratificação inválida "
                      f"({quando!r}) — sem data legível não há a partir de quando")

    print(f"\n  {ok} conferem · {mau} NÃO conferem · "
          f"{sem_fonte} sem a fonte no acervo")
    print(f"  ofício: {rat} ratificados · {prop} em proposta"
          + (f" · {ruim_data} com data inválida" if ruim_data else ""))
    if ruim_data:
        mau += ruim_data
    if mau:
        print("\n  Uma citação que não confere é uma seta sem warrant. "
              "Conserte ou remova a aresta antes de publicar.", file=sys.stderr)
    return 1 if mau else 0


if __name__ == "__main__":
    sys.exit(main())
