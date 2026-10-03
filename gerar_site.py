#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera pt/index.html — a vida de "Olá, Mundo!", um degrau por tela.

Só biblioteca padrão. A página sai de três fontes: degraus.py (o conteúdo e as
passagens que o sustentam), figuras.py (uma figura por degrau) e a pele
(pele.css + visor.js). O inglês NÃO sai daqui: en/index.html é derivado por
gerar_en.py, da tabela de tradução, e nunca editado à mão.

O gerador ABORTA se:
  - um degrau não tiver citação (lista vazia), salvo selo `a_ler` declarado;
  - um selo alegar fonte (`lida`, `escada`) sem trazer passagem EN + tradução;
  - um degrau apontar figura que não existe;
  - a tese passar de 25 palavras ou o corpo de 60 (o orçamento da folha em branco);
  - sobrar inglês no corpo visível (a prova fica fechada; o corpo é pt-BR);
  - uma expressão matemática vier sem a leitura em voz alta ("lê-se"), ou um
    degrau vier sem o seu objeto matemático declarado;
  - o ciclo que o degrau aponta na placa não existir no traço do Olá, Mundo!,
    ou não mostrar o que o degrau diz que mostra.
"""
import html
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import degraus as D   # noqa: E402
import figuras as F   # noqa: E402
sys.path.insert(0, os.path.join(AQUI, "maquina"))
import montar         # noqa: E402
import maquina        # noqa: E402


def traco_de(programa):
    """O traço do programa, com o roteiro de teclas ao lado dele, se houver."""
    base = os.path.join(AQUI, "maquina", "programas", programa)
    fonte = open(base + ".asm", encoding="utf-8").read()
    m = maquina.Maquina(montar.binario(montar.montar(fonte)[0]), traco=True)
    maximo = 100_000
    if os.path.exists(base + ".roteiro.json"):
        for n, c in json.load(open(base + ".roteiro.json", encoding="utf-8")):
            m.roteiro[n] = c
        maximo = 400
    m.rodar(maximo)
    return m.traco


TRACOS = {"ola-mundo": traco_de("ola-mundo"), "eco": traco_de("eco")}

TESE_MAX, CORPO_MAX, LESE_MAX = 25, 60, 32
SELOS = {
    "lida": ("lida", "lida no acervo"),
    "escada": ("escada", "já na escada"),
    "derivado": ("derivado", "derivado"),
    "oficio": ("oficio", "ofício"),
    "a_ler": ("aler", "a ler"),
}
EN_SINAL = re.compile(r"\b(the|and|of|is|with|that)\b")


def palavras(h):
    return len(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())


def abortar(msg):
    sys.stderr.write("ABORTADO: " + msg + "\n")
    sys.exit(1)


def conferir(d):
    if d["figura"] not in F.FIGURAS:
        abortar(f"{d['id']}: figura '{d['figura']}' não existe em figuras.py")
    if d["selo"] not in SELOS:
        abortar(f"{d['id']}: selo '{d['selo']}' desconhecido")
    if d["selo"] in ("lida", "escada"):
        if not d["citacoes"]:
            abortar(f"{d['id']}: selo '{d['selo']}' sem passagem — o degrau não entra")
        for en, pt in d["citacoes"]:
            if not en.strip() or not pt.strip():
                abortar(f"{d['id']}: citação sem original ou sem tradução")
        if d["fonte"] not in D.FONTES:
            abortar(f"{d['id']}: fonte '{d['fonte']}' não está em FONTES")
    n = palavras(d["tese"])
    if n > TESE_MAX:
        abortar(f"{d['id']}: tese com {n} palavras (máx. {TESE_MAX})")
    n = palavras(d["corpo"])
    if n > CORPO_MAX:
        abortar(f"{d['id']}: corpo com {n} palavras (máx. {CORPO_MAX})")
    if not d.get("objeto", "").strip():
        abortar(f"{d['id']}: sem objeto matemático declarado")
    for expr, lese in d.get("matematica", []):
        if not expr.strip() or not lese.strip():
            abortar(f"{d['id']}: expressão sem leitura em voz alta — toda expressão visível carrega lê-se")
        if palavras(lese) > LESE_MAX:
            abortar(f"{d['id']}: lê-se com {palavras(lese)} palavras (máx. {LESE_MAX})")
    pl = d.get("placa")
    if not pl:
        abortar(f"{d['id']}: sem ciclo na placa (placa=dict(ciclo, diz, espera))")
    traco = TRACOS.get(pl.get("programa", "ola-mundo"))
    if traco is None:
        abortar(f"{d['id']}: programa '{pl.get('programa')}' não existe")
    if not 1 <= pl["ciclo"] <= len(traco):
        abortar(f"{d['id']}: ciclo {pl['ciclo']} não existe no traço ({len(traco)} ciclos)")
    reg = traco[pl["ciclo"] - 1]
    for chave, valor in pl["espera"].items():
        if chave == "nota_comeca":
            ok = reg["nota"].startswith(valor)
        else:
            ok = reg.get(chave) == valor
        if not ok:
            abortar(f"{d['id']}: o ciclo {pl['ciclo']} não mostra {chave}={valor!r} (tem {reg.get(chave) if chave != 'nota_comeca' else reg['nota']!r})")
    for campo in ("tese", "corpo"):
        if EN_SINAL.search(html.unescape(re.sub(r"<[^>]+>", " ", d[campo]))):
            abortar(f"{d['id']}: inglês no {campo} visível — a prova fica na prova")


def selo(chave):
    cls, rot = SELOS[chave]
    return f'<span class="selo {cls}">{rot}</span>'


def prova(d):
    partes = [f'<div class="fonte">{selo(d["selo"])} {D.FONTES[d["fonte"]].split(",")[0]} {html.escape(d["ref"])}']
    if d.get("derivado"):
        partes[0] += f' {selo("derivado")} {html.escape(d["derivado"])}'
    partes[0] += "</div>"
    for en, pt in d["citacoes"]:
        partes.append(
            f'<blockquote><span class="en">{en}</span>'
            f'<span class="pt">{pt} (tradução do autor)</span>'
            f'<cite>{html.escape(d["ref"])}</cite></blockquote>')
    for n in d.get("notas", []):
        partes.append(f'<p class="nota">Buraco: {n}</p>')
    return ('<details class="prova"><summary>mostrar a prova</summary>'
            '<div class="prova-corpo">' + "".join(partes) + "</div></details>")


def matematica(d):
    linhas = "".join(
        f'<p class="expr">{e}</p><p class="leitura"><b>lê-se:</b> {l}.</p>'
        for e, l in d["matematica"])
    return (f'<div class="mat"><p class="obj">a matemática daqui · <b>{d["objeto"]}</b></p>'
            f'{linhas}</div>')


def convencoes():
    linhas = "".join(
        f'<tr><td>{c}</td><td>{o}</td><td class="expr">{e}</td><td class="leitura">{l}</td></tr>'
        for c, o, e, l in D.CONVENCOES)
    return f"""
<section class="degrau" id="conv" data-nome="Como ler os símbolos">
  <header><p class="regime">antes de tudo · como ler os símbolos desta página</p><h2>Sete sinais, e como cada um se lê</h2></header>
  <p class="tese">Cada expressão desta página vem com a leitura em voz alta logo abaixo. Esta folha diz o que cada tipo de sinal é.</p>
  <figure class="fig">
    <div class="tabela"><table class="simbolos">
      <tr><th>classe</th><th>o que é aqui</th><th>exemplo desta página</th><th>lê-se</th></tr>
      {linhas}
    </table></div>
    <div class="origem"><span>a classe vem antes do símbolo</span></div>
  </figure>
  <p class="corpo">Nenhum sinal aparece antes de estar nesta folha. Letra grega não é o assunto de nenhum degrau. Onde o símbolo é mais curto que a frase, a frase vence.</p>
</section>"""


def degrau(d):
    regua = ""
    if d["regua"]:
        cor, texto = d["regua"]
        regua = f'<div class="regua {cor}">{texto}</div>'
    origem = "".join(f"<span>{html.escape(o)}</span>" for o in d["origem"])
    return f"""
<section class="degrau" id="{d['id']}" data-nome="{html.escape(d['nome'])}">
  <header>{regua}<p class="regime">{d['numero']} · {d['regime']}</p><h2>{d['titulo']}</h2></header>
  <p class="tese">{d['tese']}</p>
  <figure class="fig">
    {F.FIGURAS[d['figura']]}
    <div class="origem">{origem}</div>
  </figure>
  <p class="corpo">{d['corpo']}</p>
  <p class="verplaca"><a href="placa.html#{d['placa'].get('programa', 'ola-mundo')}-c{d['placa']['ciclo']}">ver na placa →</a> <span>{d['placa'].get('programa', 'ola-mundo')}, ciclo {d['placa']['ciclo']}: {d['placa']['diz']}</span></p>
  {matematica(d)}
  {prova(d)}
</section>"""


def fecho(f):
    linhas = "".join(
        f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in f["linhas"])
    buracos = "".join(
        f"<li><b>{html.escape(a)}</b> ({html.escape(b)}): {html.escape(c)}</li>" for a, b, c in D.A_LER)
    origem = "".join(f"<span>{html.escape(o)}</span>" for o in f["origem"])
    return f"""
<section class="degrau" id="{f['id']}" data-nome="{html.escape(f['nome'])}">
  <header><p class="regime">fecho</p><h2>{f['titulo']}</h2></header>
  <p class="tese">{f['tese']}</p>
  <figure class="fig">
    <div class="tabela"><table>
      <tr><th>degrau</th><th>conserva</th><th>esquece</th><th>fonte</th></tr>
      {linhas}
    </table></div>
    <div class="origem">{origem}</div>
  </figure>
  <p class="corpo">{f['corpo']}</p>
  <details class="prova"><summary>buracos declarados</summary><div class="prova-corpo">
    <ul>{buracos}</ul>
    <p class="nota">Mapa que esconde o que falta mente sobre o próprio tamanho. Estes são os buracos que este mapa sabe ter.</p>
  </div></details>
</section>"""


def trilha_js():
    # json.dumps escapa as aspas de dentro do HTML; repr não escapava, e o
    # token "lê-se" (com aspas duplas) quebrou o roteiro inteiro em silêncio.
    return json.dumps([dict(tok=tok, nome=nome) for nome, tok in D.TRILHA], ensure_ascii=False)


def pagina():
    for d in D.DEGRAUS:
        conferir(d)
    if len(D.TRILHA) != len(D.DEGRAUS) + 2:
        abortar(f"trilha com {len(D.TRILHA)} estações para convenções + {len(D.DEGRAUS)} degraus + fecho")
    css = open(os.path.join(AQUI, "pele.css"), encoding="utf-8").read()
    js = open(os.path.join(AQUI, "visor.js"), encoding="utf-8").read().replace("__TRILHA__", trilha_js())
    corpo = convencoes() + "".join(degrau(d) for d in D.DEGRAUS) + fecho(D.FECHO)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A vida de Olá, Mundo! — hello-world-machine</title>
<meta name="description" content="O que cada camada de abstração faz com o número: de uma frase dita no escuro até a luz na tela, um degrau por vez, com a passagem do livro que sustenta cada um.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&family=Spline+Sans+Mono:wght@400;500&display=swap">
<style>
{css}
</style>
</head>
<body>
<div class="pagina">
<div class="cab">
  <div><p class="eyebrow">hello-world-machine</p><h1>A vida de Olá, Mundo!</h1></div>
  <p class="nota"><a href="../en/" lang="en" hreflang="en">English</a> · ← → no teclado; um degrau por tela</p>
</div>
<div class="trilha" id="trilha" aria-label="O que o o já virou"></div>
<div id="degraus">{corpo}
</div>
<nav class="passo" aria-label="Navegação entre degraus">
  <button id="ant" type="button"><small>anterior</small><span></span></button>
  <p class="pos" id="pos"></p>
  <button id="prox" type="button" class="prox"><small>próximo</small><span></span></button>
</nav>
<footer class="rodape">
  <p class="nota">Texto e figuras: CC BY-SA 4.0 · código: MIT · as passagens citadas pertencem aos seus autores e aparecem sob direito de citação, com fonte e capítulo. <a href="https://github.com/mateusalkimim/hello-world-machine">repositório</a></p>
</footer>
</div>
<script>
{js}
</script>
</body>
</html>
"""


def main():
    saida = os.path.join(AQUI, "pt", "index.html")
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    h = pagina()
    with open(saida, "w", encoding="utf-8") as f:
        f.write(h)
    n = len(D.DEGRAUS)
    cit = sum(len(d["citacoes"]) for d in D.DEGRAUS)
    ex = sum(len(d["matematica"]) for d in D.DEGRAUS)
    print(f"pt/index.html: convenções + {n} degraus + fecho, {cit} passagens, {ex} expressões com lê-se, {len(D.A_LER)} buracos declarados, {len(h)} bytes")


if __name__ == "__main__":
    main()
