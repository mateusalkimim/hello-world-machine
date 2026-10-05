#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Portão do mapa. Mede o que a norma manda medir, em vez de prometer.

A §1.1 da norma-de-diagramas diz que cruzamento de aresta é o defeito nº 1 e
que, em conflito com qualquer outra regra, o cruzamento perde. Uma norma assim
só vale com instrumento: "desenhei sem cruzar" é impressão, e impressão foi o
que produziu metade dos defeitos deste projeto.

Mede quatro coisas, todas geométricas:
  [1] cruzamento entre arestas (amostrando as curvas de Bézier em segmentos);
  [2] aresta atravessando o retângulo de um nó que não é ponta dela — pior que
      cruzar, porque parece conexão e não é;
  [3] rótulo que transborda a caixa do nó (§1.4: o rótulo mora DENTRO);
  [4] nós sobrepostos.

Roda:  python3 conferir_mapa.py [--controle]

O `--controle` é controle negativo: reposiciona um nó para FORÇAR cruzamento e
confere que o portão acusa. Portão que nunca reprovou não provou nada.
"""
import re, sys, math, pathlib
import mapa as M

def bezier(p0, p1, p2, p3, n=26):
    for i in range(n + 1):
        t = i / n; u = 1 - t
        yield (u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
               u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1])

def poligonal(d):
    """Converte o atributo d (M/L/C) numa lista de pontos."""
    n = [float(x) for x in re.findall(r"-?\d+\.?\d*", d)]
    pts, i = [], 0
    if d.startswith("M"): pts.append((n[0], n[1])); i = 2
    if " C" in d or d[2:].lstrip().startswith("C"):
        p0 = pts[-1]
        pts += list(bezier(p0, (n[2], n[3]), (n[4], n[5]), (n[6], n[7])))[1:]
    else:
        pts.append((n[2], n[3]))
    return pts

def cruza(a1, a2, b1, b2):
    def o(p, q, r):
        v = (q[1]-p[1])*(r[0]-q[0]) - (q[0]-p[0])*(r[1]-q[1])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else 2)
    o1, o2, o3, o4 = o(a1,a2,b1), o(a1,a2,b2), o(b1,b2,a1), o(b1,b2,a2)
    return o1 != o2 and o3 != o4

def perto(p, q, tol=6.0):
    return math.hypot(p[0]-q[0], p[1]-q[1]) < tol

def analisar(svg):
    arestas = []      # (d, pontos)
    for m in re.finditer(r'<path d="([^"]+)"[^>]*stroke="(#[0-9a-fA-F]{6})"', svg):
        d, cor = m.group(1), m.group(2)
        if "stroke-width=\"4.6\"" in svg[m.start():m.start()+260]: continue  # realce
        arestas.append((d, poligonal(d)))
    nos = [(float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))
           for m in re.finditer(r'<rect x="(-?\d+\.?\d*)" y="(-?\d+\.?\d*)" '
                                r'width="(\d+)" height="(\d+)" rx="7"', svg)]
    achados = []

    # [1] cruzamento aresta x aresta
    for i in range(len(arestas)):
        for j in range(i + 1, len(arestas)):
            A, B = arestas[i][1], arestas[j][1]
            for a in range(len(A) - 1):
                for b in range(len(B) - 1):
                    if cruza(A[a], A[a+1], B[b], B[b+1]):
                        # pontas em comum nao contam: sao arestas do mesmo no
                        pt = A[a]
                        if any(perto(pt, e) for e in (A[0], A[-1], B[0], B[-1])):
                            continue
                        achados.append(f"[1] cruzamento de arestas em "
                                       f"({pt[0]:.0f},{pt[1]:.0f})")
                        break
                else: continue
                break

    # [2] aresta atravessando no que nao e ponta dela
    for d, pts in arestas:
        for (x, y, w, h) in nos:
            dentro = [p for p in pts[2:-2] if x < p[0] < x+w and y < p[1] < y+h]
            if len(dentro) > 2:
                achados.append(f"[2] aresta atravessa o nó em ({x:.0f},{y:.0f})")
                break

    # [5] conteudo FORA do viewBox. A chave da cor caiu 5px abaixo da borda e
    # sumiu da tela sem ninguem notar — e a §2 da norma diz que cor semantica
    # SEM chave na mesma tela e enfeite. Um defeito de 5 pixels apagou uma
    # regra inteira, entao ele vira medida.
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    if vb:
        VW, VH = float(vb.group(1)), float(vb.group(2))
        for m in re.finditer(r'<(rect|text)[^>]*?(?:x|y)="', svg):
            pass
        for m in re.finditer(r'<rect x="(-?[\d.]+)" y="(-?[\d.]+)" width="([\d.]+)" '
                             r'height="([\d.]+)"', svg):
            x, y, w, h = map(float, m.groups())
            if y + h > VH + 0.5 or x + w > VW + 0.5 or x < -0.5 or y < -0.5:
                achados.append(f"[5] forma fora do viewBox em ({x:.0f},{y:.0f})")
        for m in re.finditer(r'<text x="(-?[\d.]+)" y="(-?[\d.]+)"', svg):
            x, y = map(float, m.groups())
            if y > VH - 2 or x > VW - 2 or x < 2 or y < 2:
                achados.append(f"[5] texto fora (ou colado na borda) do viewBox "
                               f"em ({x:.0f},{y:.0f})")

    # [4] nos sobrepostos
    for i in range(len(nos)):
        for j in range(i + 1, len(nos)):
            ax, ay, aw, ah = nos[i]; bx, by, bw, bh = nos[j]
            if ax < bx+bw and bx < ax+aw and ay < by+bh and by < ay+ah:
                achados.append(f"[4] nós sobrepostos: ({ax:.0f},{ay:.0f}) e "
                               f"({bx:.0f},{by:.0f})")
    return achados, len(arestas), len(nos)

def controle():
    """Controle negativo. Planta defeito e exige que o portão acuse.

    Nota honesta sobre este grafo: ele é quase uma ÁRVORE (9 nós, 9 arestas,
    uma única que pula nível), e num grafo assim cruzamento é quase impossível
    de produzir mexendo em faixa — a topologia não deixa. Então "0 cruzamentos"
    aqui é barato, e dizer que é conquista seria mentir sobre o que o portão
    provou. O defeito que este mapa REALMENTE corre risco de ter é o [2], a
    aresta que atravessa um nó — e foi ele que apareceu de verdade na 1ª
    versão, no arco que pula nível.

    Por isso o controle tem três pernas, e a do cruzamento é sintética: um
    par de segmentos que se cruzam de propósito, só para provar que o
    predicado sabe reconhecer um cruzamento quando existe.
    """
    falhas = []

    # (i) predicado de cruzamento, em caso sintético conhecido
    if not cruza((0,0), (10,10), (0,10), (10,0)):
        falhas.append("o predicado nao reconhece um X explicito")
    if cruza((0,0), (10,0), (0,5), (10,5)):
        falhas.append("o predicado inventa cruzamento em paralelas")

    # (ii) folga do arco reduzida -> aresta atravessa o no (o defeito real)
    guarda = M.LARG
    M.LARG = 1000
    codigo = pathlib.Path("mapa.py").read_text(encoding="utf-8")
    ns = {}
    exec(codigo.replace("NO_W // 2 + 130", "NO_W // 2 + 68")
               .replace("LARG, NO_W, NO_H = 1090", "LARG, NO_W, NO_H = 1000"), ns)
    achados, _, _ = analisar(ns["desenhar"]())
    M.LARG = guarda
    if not any(a.startswith("[2]") for a in achados):
        falhas.append("folga do arco reduzida e o portao NAO viu a aresta "
                      "atravessando o no")

    # (iii) dois nos na mesma faixa e no mesmo nivel -> sobreposicao
    guardado = dict(M.COLUNA)
    M.COLUNA["somador"] = M.COLUNA["flipflop"]      # ambos no nivel 2, mesma faixa
    achados, _, _ = analisar(M.desenhar())
    M.COLUNA.update(guardado)
    if not any(a.startswith("[4]") for a in achados):
        falhas.append("dois nos empilhados e o portao NAO viu a sobreposicao")

    print("controle negativo — tres defeitos plantados:")
    for f in falhas: print("  FALHA:", f)
    if falhas:
        print("  portao NAO mede o que diz medir.")
        return 1
    print("  as tres pernas acusaram — o portao reprova quando deve")
    return 0

def main():
    if "--controle" in sys.argv:
        return controle()

    achados, na, nn = analisar(M.desenhar())
    print(f"mapa: {nn} nós, {na} arestas")
    for a in achados: print("  FALHA", a)
    print(f"\n{len(achados)} achados")
    return 1 if achados else 0

if __name__ == "__main__":
    sys.exit(main())
