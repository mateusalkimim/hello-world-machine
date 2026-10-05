# -*- coding: utf-8 -*-
"""O mapa da escada, em SVG — gerado, nunca desenhado à mão.

Regras aplicadas, com o parágrafo da norma que as manda (norma-de-diagramas.md
da Hipátia, estado PROPOSTA):

  §1.1  Cruzamento de aresta é o defeito nº 1, e ganha de qualquer outra regra
        desta norma. Este layout tem ZERO cruzamentos, e o `conferir_mapa.py`
        mede isso — nao e promessa, e verificacao.
  §1.2  Direção declarada UMA vez e não misturada: aqui é de baixo para cima.
        O eletroímã é o chão; a máquina é o topo. (A página antiga dizia "de
        baixo para cima" no título e renderizava de cima para baixo.)
  §1.3  Teto de cinco formas, e forma só entra com significado atribuído. Aqui
        usa-se UMA forma para todos os nós: o que distingue é a cor, e o
        argumento da própria §1.3 é que vocabulário menor é menos coisa para o
        leitor decorar antes de ler.
  §1.4  O rótulo mora DENTRO do nó.
  §2    A cor carrega domínio (o regime do degrau), e por isso a CHAVE vai na
        mesma tela — sem ela a cor vira enfeite. A norma é explícita: "cor
        semântica exige a chave na mesma tela".
  §4    SVG com `width:100%` escala pela largura e, em tela baixa, corta os
        dois extremos em silêncio. Daí o `max-height` em vh no CSS, e a medida
        em mais de uma resolução.

O que a cor diz (o regime), e é a tese da escada desenhada:
  física        — ainda é eletricidade e ferro
  combinacional — a saída depende só das entradas DE AGORA
  sequencial    — a saída depende também do que veio ANTES (o degrau que lembra)
  arquitetura   — peças em sequência sob um controlador

A régua horizontal entre o nível 0 e o 1 é a afirmação mais forte do mapa: é
onde o assunto deixa de ser eletricidade e passa a ser lógica. Ela é desenhada
porque é conteúdo, não enfeite.
"""
import degraus as D

# --- geometria --------------------------------------------------------------
LARG, NO_W, NO_H = 1090, 200, 56
FAIXA = {"L": 200, "C": 470, "R": 740}
LINHA = 104          # altura de um nível
NIVEL_TOPO = 7       # o topo da escada; era 5 até 2026-08-27
TOPO  = 196          # y do nível mais alto (abaixo da fronteira de cima)

def y_de(nivel):     # o mais alto no topo, -1 embaixo — §1.2, direção declarada
    return TOPO + (NIVEL_TOPO - nivel) * LINHA

# faixa horizontal de cada degrau, escolhida para não cruzar nenhuma aresta
COLUNA = {
    "eletroima": "C", "rele": "C", "porta": "C",
    "somador": "L", "flipflop": "C", "flipflop_b": "R",   # flipflop vai ao centro em 2026-10-03: o oscilador ocupa a direita no nível 1
    "ula": "L",
    "registrador": "C", "contador": "R", "maquina": "C",
    "assembler": "L", "avaliador": "C", "paradigma": "C",
    "memoria": "C", "compilador": "R",
    "transistor": "L", "oscilador": "R",
}
REGIME = {
    "eletroima": "fisica", "rele": "fisica",
    "porta": "comb", "somador": "comb", "ula": "comb",
    "flipflop": "seq", "flipflop_b": "seq", "contador": "seq",
    "registrador": "seq", "maquina": "arq",
    # o 5º regime entra em 2026-08-27: acima da máquina o assunto deixa de ser
    # circuito e passa a ser LINGUAGEM. A §1.3 limita FORMA a cinco; aqui a
    # forma é uma só, e quem carrega o regime é a cor — que a §2 permite desde
    # que a chave esteja na mesma tela, e está.
    "assembler": "lingua", "avaliador": "lingua", "paradigma": "lingua",
    "memoria": "seq", "compilador": "lingua",
    "transistor": "fisica", "oscilador": "seq",
}

# As seis FAMÍLIAS (2026-10-03): o que cada peça faz com o número. A cor do
# nó passa a dizer a família; o regime (combinacional × sequencial) continua
# existindo como propriedade do degrau, mas deixa de ser a chave do mapa.
FAMILIA = {
    "eletroima": "transistores", "rele": "transistores", "transistor": "transistores",
    "porta": "portas",
    "somador": "somadores", "ula": "somadores",
    "flipflop": "registradores", "flipflop_b": "registradores", "contador": "registradores",
    "registrador": "registradores", "memoria": "registradores",
    "maquina": "instrucoes", "assembler": "instrucoes", "avaliador": "instrucoes",
    "paradigma": "instrucoes", "compilador": "instrucoes",
    "oscilador": "relogio",
}
COR_FAMILIA = {
    "transistores": ("#3a2418", "#c1704f", "#e6b499"),
    "portas":       ("#14263f", "#5b8fc9", "#bcd4ec"),
    "somadores":    ("#1a2a4a", "#7fa3dc", "#cfe0f5"),
    "registradores":("#10312e", "#4fb3a5", "#a8e0d7"),
    "instrucoes":   ("#2a1836", "#a883c9", "#dcc9ec"),
    "relogio":      ("#33280f", "#c9a266", "#f0dcb4"),
}
NOME_FAMILIA = {
    "transistores": "transistores — ligam e desligam",
    "portas":       "portas lógicas — decidem",
    "somadores":    "somadores — fazem conta",
    "registradores":"registradores — guardam número",
    "instrucoes":   "instruções — mandam",
    "relogio":      "relógio — marca o tempo",
}
COR = {
    "fisica": ("#3a2418", "#c1704f", "#e6b499"),
    "comb":   ("#14263f", "#5b8fc9", "#bcd4ec"),
    "seq":    ("#10312e", "#4fb3a5", "#a8e0d7"),
    "arq":    ("#33280f", "#c9a266", "#f0dcb4"),
    "lingua": ("#2a1836", "#a883c9", "#dcc9ec"),
}
NOME_REGIME = {
    "fisica": "física — ainda é eletricidade e ferro",
    "comb":   "combinacional — a saída depende só das entradas de agora",
    "seq":    "sequencial — a saída depende também do que veio antes",
    "arq":    "arquitetura — peças em sequência, sob um controlador",
    "lingua": "linguagem — acima da máquina, o assunto é significado",
}

# fronteira: o que se sabe que existe e ninguém leu. Desenhada, não escondida.
# O compilador saiu daqui em 2026-08-27: virou degrau. Sobram os dois que
# seguem sem sustentação, e o mapa continua mostrando que a estrada não acaba.
FRONTEIRA_CIMA = [
    ("sistema operacional", "L"), ("instrução", "C"),
]
FRONTEIRA_ULA  = ("ULA", "L")          # acima do somador
FRONTEIRA_RAM  = ("memória (RAM)", "C") # ao lado do registrador... ver abaixo
FRONTEIRA_BAIXO = ("corrente e ferro", "C")

def _no(x, y, rot, nivel, regime, alvo):
    fundo, borda, texto = COR_FAMILIA[regime]   # desde 2026-10-03 o 'regime' do nó é a FAMÍLIA
    x0, y0 = x - NO_W // 2, y - NO_H // 2
    linhas = _quebrar(rot)
    dy = -5 if len(linhas) > 1 else 5
    tspans = "".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else 17}">{l}</tspan>'
        for i, l in enumerate(linhas))
    return f'''<a href="#{alvo}" class="no">
<rect x="{x0}" y="{y0}" width="{NO_W}" height="{NO_H}" rx="7"
      fill="{fundo}" stroke="{borda}" stroke-width="1.6"/>
<text x="{x}" y="{y + dy}" text-anchor="middle" fill="{texto}"
      font-family="Cormorant,Georgia,serif" font-size="17.5">{tspans}</text>
<text x="{x0 + 9}" y="{y0 + 15}" fill="{borda}" font-family="Inter,sans-serif"
      font-size="10" opacity=".75">{nivel}</text>
</a>'''

def _fantasma(x, y, rot):
    x0, y0 = x - NO_W // 2, y - 21
    return (f'<rect x="{x0}" y="{y0}" width="{NO_W}" height="42" rx="7" '
            f'fill="none" stroke="#33465f" stroke-width="1.3" '
            f'stroke-dasharray="5 4"/>'
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" fill="#6b7a90" '
            f'font-family="Inter,sans-serif" font-size="12.5">{rot}</text>')

def _quebrar(rot):
    if len(rot) <= 22: return [rot]
    p = rot.split()
    meio = len(rot) // 2; melhor, corte = 1e9, 1
    for i in range(1, len(p)):
        d = abs(len(" ".join(p[:i])) - meio)
        if d < melhor: melhor, corte = d, i
    return [" ".join(p[:corte]), " ".join(p[corte:])]

def _aresta(de, para, lida=True, dupla=False):
    """Sobe do topo do nó de baixo até a base do nó de cima."""
    x1, y1 = FAIXA[COLUNA[de]], y_de(_niv(de)) - NO_H // 2
    x2, y2 = FAIXA[COLUNA[para]], y_de(_niv(para)) + NO_H // 2
    cor = "#6fbf6a" if lida else "#33465f"
    tra = '' if lida else ' stroke-dasharray="5 4"'
    if abs(_niv(para) - _niv(de)) > 1 and x1 != x2 and not _passa_livre(de, para, x1, y1, x2, y2):
        # A que pula nível: arco por FORA. A folga NÃO é chutada — é a borda
        # direita do nó mais largo desta faixa mais uma margem, senão o arco
        # raspa a caixa de quem está no meio do caminho. Foi o que aconteceu
        # na 1ª versão, e quem viu foi o conferir_mapa.py, não eu.
        # (2026-10-03: o arco só é usado quando a curva em S passaria por
        # DENTRO de um nó; se o vão entre as colunas está livre, a curva em S
        # serve, e não cruza as verticais da coluna de destino.)
        cx = max(x1, x2) + NO_W // 2 + 130
        d = f"M{x1},{y1} C{cx},{y1 - 30} {cx},{y2 + 30} {x2},{y2}"
    elif x1 == x2:
        d = f"M{x1},{y1} L{x2},{y2}"
    else:
        my = (y1 + y2) / 2
        d = f"M{x1},{y1} C{x1},{my} {x2},{my} {x2},{y2}"
    saida = (f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="1.7"{tra} '
             f'marker-end="url(#ponta{"" if lida else "F"})"/>')
    if dupla:  # segunda testemunha: duas fontes independentes sustentam a seta
        saida += (f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="4.6" '
                  f'opacity=".22"/>')
    return saida

def _passa_livre(de, para, x1, y1, x2, y2, folga=6):
    """A curva em S entre dois nós que pulam nível passa por dentro de algum
    outro nó? Amostra a curva e mede contra as caixas."""
    my = (y1 + y2) / 2
    for k in COLUNA:
        if k in (de, para) or k not in _NIV:
            continue
        cx, cy = FAIXA[COLUNA[k]], y_de(_niv(k))
        x0, xa = cx - NO_W // 2 - folga, cx + NO_W // 2 + folga
        y0, ya = cy - NO_H // 2 - folga, cy + NO_H // 2 + folga
        for i in range(1, 40):
            t = i / 40
            x = (1-t)**3*x1 + 3*(1-t)**2*t*x1 + 3*(1-t)*t**2*x2 + t**3*x2
            y = (1-t)**3*y1 + 3*(1-t)**2*t*my + 3*(1-t)*t**2*my + t**3*y2
            if x0 <= x <= xa and y0 <= y <= ya:
                return False
    return True

_NIV = {d[0]: d[2] for d in D.DEGRAUS}
_ROT = {d[0]: d[1] for d in D.DEGRAUS}
def _niv(k): return _NIV[k]


def _arestas_desenhadas():
    fora = getattr(D, "FORA_DO_MAPA", set())
    return [a for a in D.ARESTAS if (a[0], a[1]) not in fora]

def desenhar():
    ybase_chave = y_de(min(d[2] for d in D.DEGRAUS)) + NO_H // 2 + 40
    alt = ybase_chave + 46   # a chave TERMINA dentro do quadro
    p = []
    p.append(f'<svg viewBox="0 0 {LARG} {alt}" xmlns="http://www.w3.org/2000/svg" '
             f'role="img" aria-label="Mapa da escada de abstrações, do eletroímã '
             f'à máquina de registradores">')
    p.append('''<defs>
<marker id="ponta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6"
        markerHeight="6" orient="auto-start-reverse">
  <path d="M0,1 L9,5 L0,9 z" fill="#6fbf6a"/></marker>
<marker id="pontaF" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6"
        markerHeight="6" orient="auto-start-reverse">
  <path d="M0,1 L9,5 L0,9 z" fill="#33465f"/></marker>
</defs>''')

    # --- a régua: onde o assunto deixa de ser eletricidade -------------------
    yr = (y_de(1) + y_de(0)) / 2
    p.append(f'<line x1="46" y1="{yr}" x2="{LARG-46}" y2="{yr}" stroke="#c9a266" '
             f'stroke-width="1" stroke-dasharray="2 5" opacity=".65"/>')
    p.append(f'<text x="{LARG-50}" y="{yr-9}" text-anchor="end" fill="#c9a266" '
             f'font-family="Inter,sans-serif" font-size="11.5" opacity=".9">'
             f'daqui para cima o assunto é lógica, não eletricidade</text>')

    # a 2ª régua: acima da máquina o assunto deixa de ser circuito
    yr2 = (y_de(6) + y_de(5)) / 2
    p.append(f'<line x1="46" y1="{yr2}" x2="{LARG-46}" y2="{yr2}" stroke="#a883c9" '
             f'stroke-width="1" stroke-dasharray="2 5" opacity=".55"/>')
    p.append(f'<text x="{LARG-50}" y="{yr2-9}" text-anchor="end" fill="#a883c9" '
             f'font-family="Inter,sans-serif" font-size="11.5" opacity=".9">'
             f'daqui para cima o assunto é linguagem, não circuito</text>')

    # --- fronteira de cima: a estrada continua ------------------------------
    for rot, col in FRONTEIRA_CIMA:
        p.append(_fantasma(FAIXA[col], 74, rot))
    p.append(f'<text x="50" y="30" fill="#6b7a90" font-family="Inter,sans-serif" '
             f'font-size="11.5">não lido — a estrada continua, e o mapa não '
             f'esconde isso</text>')
    # NAO fixar o nivel aqui: quando a escada cresceu de 5 para 7, esta linha
    # continuou apontando para o nivel 5 e as setas da fronteira passaram a
    # ATRAVESSAR os dois degraus novos. Quem viu foi o conferir_mapa.py.
    _topo = max(d[2] for d in D.DEGRAUS)
    _kt = [d[0] for d in D.DEGRAUS if d[2] == _topo][0]
    xm, ym = FAIXA[COLUNA[_kt]], y_de(_topo) - NO_H // 2
    for col in ("L", "C", "R"):
        xd, yd = FAIXA[col], 74 + 21 + 8
        d = (f"M{xm},{ym} L{xd},{yd}" if col == "C"
             else f"M{xm},{ym} C{xm},{ym-40} {xd},{yd+44} {xd},{yd}")
        p.append(f'<path d="{d}" fill="none" stroke="#33465f" stroke-width="1.4" '
                 f'stroke-dasharray="5 4" marker-end="url(#pontaF)"/>')
    # ULA sobre o somador, RAM sobre o registrador: as duas pontas que a
    # bibliografia sustenta e ninguém abriu
    # A ULA saiu daqui: virou degrau em 2026-08-27. E o "corrente e ferro" saiu
    # porque a leitura mostrou que aquela aresta JÁ ESTAVA no repositório — a
    # linha estava sobrando na lista, não faltando no mapa.

    # --- arestas lidas ------------------------------------------------------
    vistas, dupla = set(), set(D.SEGUNDA_TESTEMUNHA)
    for a in _arestas_desenhadas():
        if (a[0], a[1]) in vistas: continue
        vistas.add((a[0], a[1]))
        p.append(_aresta(a[0], a[1], lida=True, dupla=(a[0], a[1]) in dupla))

    # --- nós ----------------------------------------------------------------
    for k, rot, niv, _diz in D.DEGRAUS:
        p.append(_no(FAIXA[COLUNA[k]], y_de(niv), rot, f"nível {niv}",
                     FAMILIA[k], k))

    # --- a chave, na MESMA tela (§2) ---------------------------------------
    ybase = ybase_chave
    p.append(f'<text x="50" y="{ybase}" fill="#5b6b86" '
             f'font-family="Inter,sans-serif" font-size="11.5">a cor diz a família · a seta cheia: de que a peça é feita · a tracejada: o que ainda está fora da escada</text>')
    x = 50
    usados = [f for f in ("transistores", "portas", "somadores", "registradores", "instrucoes", "relogio")
              if f in {FAMILIA[d[0]] for d in D.DEGRAUS}]
    for reg in usados:
        fundo, borda, _t = COR_FAMILIA[reg]
        p.append(f'<rect x="{x}" y="{ybase+13}" width="13" height="13" rx="3" '
                 f'fill="{fundo}" stroke="{borda}" stroke-width="1.4"/>')
        p.append(f'<text x="{x+19}" y="{ybase+24}" fill="#8a94a4" '
                 f'font-family="Inter,sans-serif" font-size="11">'
                 f'{NOME_FAMILIA[reg].split(" — ")[0]}</text>')
        x += 26 + len(NOME_FAMILIA[reg].split(" — ")[0]) * 6.4
    p.append("</svg>")
    return "\n".join(x for x in p if x)


if __name__ == "__main__":
    print(desenhar()[:400])
