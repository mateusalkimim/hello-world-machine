#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera pt/placa.html — Olá, Mundo! visto na placa.

A página carrega a máquina e o montador do navegador (maquina/*.js), monta o
programa, roda, e entrega o traço ao tocador (placa.js). A pele vem de
pele.css, inline, como em pt/index.html. Só biblioteca padrão.
"""
import html
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import barra as BARRA  # noqa: E402


def main():
    css = open(os.path.join(AQUI, "pele.css"), encoding="utf-8").read() + BARRA.CSS
    import json
    pasta = os.path.join(AQUI, "maquina", "programas")
    programas = []
    for nome in ("ola-mundo", "eco"):
        asm = open(os.path.join(pasta, nome + ".asm"), encoding="utf-8").read().replace("</script", "<\\/script")
        attrs = f'data-programa="{nome}"'
        rp = os.path.join(pasta, nome + ".roteiro.json")
        if os.path.exists(rp):
            roteiro = json.load(open(rp, encoding="utf-8"))
            attrs += f" data-roteiro='{json.dumps(roteiro)}' data-max=\"400\""
        programas.append(f'<script type="text/plain" {attrs}>{asm}</script>')
    blocos_programas = "\n".join(programas)
    extra = """
.placa-wrap{display:grid;gap:1rem}
.quadro{background:var(--card);border:1px solid var(--linha);padding:.6rem;min-width:0;overflow-x:auto}
canvas#placa{display:block;height:auto}
.controles{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center}
.controles button{font:inherit;font-size:.85rem;color:var(--azul);background:none;border:1px solid var(--linha);border-radius:3px;padding:.45rem .8rem;cursor:pointer}
.controles button:hover{border-color:var(--bronze)}
.controles button:focus-visible,.controles input:focus-visible,.controles select:focus-visible{outline:2px solid var(--bronze);outline-offset:2px}
.controles input[type=range]{flex:1 1 12rem;min-width:8rem}
.controles select{font:inherit;font-size:.85rem;color:var(--ink);background:var(--card);border:1px solid var(--linha);border-radius:3px;padding:.35rem}
.controles label{font-size:.82rem;color:var(--ink2);display:flex;gap:.35rem;align-items:center}
.controles input#teclado{font:inherit;font-size:.9rem;color:var(--ink);background:var(--card);border:1px solid var(--bronze);border-radius:3px;padding:.45rem .7rem;flex:1 1 16rem;min-width:10rem}
.estado{display:grid;gap:.25rem;font-size:.9rem;color:var(--ink2)}
.estado #pos{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--bronze);font-weight:600}
.estado #nota{font-family:var(--it-serif);font-size:1.1rem;color:var(--ink)}
.estado #resumo{font-size:.8rem;color:var(--muted)}
.lado{display:grid;grid-template-columns:1fr;gap:1rem}
ol#listagem{list-style:none;margin:0;padding:0;font-family:var(--it-mono);font-size:.82rem;display:grid;gap:1px;max-height:22rem;overflow:auto}
ol#listagem li{display:grid;grid-template-columns:3.2rem 6.5rem 1fr;gap:.6rem;padding:.2rem .5rem;color:var(--ink2)}
ol#listagem li .end{color:var(--muted)} ol#listagem li .bytes{color:var(--azul)}
ol#listagem li.atual{background:var(--card);color:var(--ink);box-shadow:inset 3px 0 0 var(--bronze)}
.legenda{font-size:.8rem;color:var(--muted);display:flex;gap:1rem;flex-wrap:wrap}
.legenda i{display:inline-block;width:.9em;height:.9em;border-radius:2px;vertical-align:-.1em;margin-right:.3em}
@media (min-width:900px){.lado{grid-template-columns:1fr 1fr}}
"""
    pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Olá, Mundo! na placa — hello-world-machine</title>
<meta name="description" content="A máquina desenhada em planta toca, ciclo a ciclo, o programa que escreve Olá, Mundo! na tela: a origem acende, o barramento mostra o padrão, o destino recebe.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&family=Spline+Sans+Mono:wght@400;500&display=swap">
<style>
{css}
{extra}
</style>
</head>
<body>
<div class="pagina" style="max-width:62em">
{BARRA.barra("placa")}
<div class="cab">
  <div><p class="eyebrow">hello-world-machine · instrumento</p><h1>Olá, Mundo! na placa</h1></div>
  <p class="nota"><a href="index.html">← os degraus</a> · ← → anda um ciclo · espaço toca e pausa · clicar num módulo abre o degrau que o explica</p>
</div>
<p class="tese">A máquina já rodou o programa. O que você toca é o traço: em cada ciclo, a origem acende, o barramento mostra o padrão, o destino recebe. Nada anda. O padrão se copia. No eco, cada tecla sua entra na gaveta 8200h e a placa mostra o caminho dela até a tela.</p>
<div class="placa-wrap">
  <div class="quadro"><canvas id="placa" width="1000" height="600" aria-label="A placa em planta: dois barramentos, os módulos entre eles, e a tela"></canvas></div>
  <div class="controles">
    <button id="ant" type="button">← anterior</button>
    <button id="tocar" type="button">tocar</button>
    <button id="prox" type="button">próximo →</button>
    <input id="barra" type="range" min="0" max="60" value="0" aria-label="ciclo">
    <select id="marcha" aria-label="marcha"><option value="1">1 ciclo por segundo</option><option value="4">4 por segundo</option><option value="20">20 por segundo</option></select>
    <label><input id="sotela" type="checkbox"> só as escritas na tela</label>
    <label>programa <select id="programa" aria-label="programa"></select></label>
    <input id="teclado" type="text" placeholder="digite aqui: cada tecla vira um byte" aria-label="teclado da máquina" autocomplete="off" hidden>
  </div>
  <div class="estado"><p id="pos"></p><p id="nota"></p><p id="resumo"></p></div>
  <p class="legenda"><span><i style="background:var(--azul)"></i>endereço</span><span><i style="background:var(--bronze)"></i>dado</span><span><i style="background:var(--bit1)"></i>bit 1</span><span><i style="background:var(--bit0);border:1px solid var(--linha)"></i>bit 0</span><span><i style="background:var(--linha)"></i>apagado</span></p>
  <div class="lado">
    <div>
      <p class="eyebrow">o programa, como a pessoa escreveu e como virou bytes</p>
      <ol id="listagem"></ol>
    </div>
    <div>
      <p class="eyebrow">o que a placa mostra</p>
      <p class="corpo">Em cima, o barramento de endereços: 16 fios, azul. Embaixo, o de dados: 8 fios, bronze, com os oito bits à vista. Entre os dois, os módulos da máquina do Petzold, cada um com o seu rótulo matemático. À direita, a tela, que lê 264 gavetas da RAM. Em cada ciclo acendem no máximo quatro coisas; o resto fica apagado.</p>
      <p class="nota">Especificação: pesquisa/a-maquina.md e pesquisa/a-placa-em-planta.md. O traço desta página é o mesmo que a máquina em Python produz, ciclo a ciclo.</p>
    </div>
  </div>
</div>
<footer class="rodape"><p class="nota">Texto e figuras: CC BY-SA 4.0 · código: MIT · <a href="https://github.com/mateusalkimim/hello-world-machine">repositório</a></p></footer>
</div>
{blocos_programas}
<script src="../maquina/montar.js"></script>
<script src="../maquina/maquina.js"></script>
<script src="../placa.js"></script>
</body>
</html>
"""
    saida = os.path.join(AQUI, "pt", "placa.html")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print(f"pt/placa.html: {len(pagina)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
