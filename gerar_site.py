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
    ou não mostrar o que o degrau diz que mostra;
  - uma palavra técnica aparecer antes do degrau que a explica (TECNICAS), ou
    uma palavra de método aparecer em qualquer lugar visível da página
    (PROCESSO): a folha em branco é propriedade de construção.

A página é para quem não sabe nada. Selos, notas e buracos são DADO do
catálogo e vão para pesquisa/o-que-falta.md, gerado aqui; nunca para a página.
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

# Palavras de método: conversa de quem fez a página com quem a audita. Nenhuma
# cabe na página, que é para quem não sabe nada.
PROCESSO = ["selo", "ofício", "oficio", "warrant", "prova", "confirmado", "versão", "amostra",
            "testemunha", "tradução do autor", "citação", "síntese", "procedência", "2026-",
            "ratific", "modelo de linguagem", "gerador", "buraco", "decisão nossa", "declarad",
            "a ler", "acervo", "derivad", "régua", "portão"]

# Palavra técnica → o degrau em que ela é explicada (None = nunca aparece).
TECNICAS = {
    "código": "d0",
    "chave": "d0b", "gaveta": "d0b", "tecla": "d0b",
    "tabela": "d1",
    "casa": "d2", "bit": "d2", "byte": "d2",
    "corrente": "d4", "relé": "d4", "limiar": "d4", "volt": "d4",
    "porta lógica": "d5", "estado": "d5",
    "memória": "d6", "endereço": "d6",
    "instrução": "d7", "programa": "d7", "contador de programa": "d7",
    "montador": "d8", "sistema operacional": "d8",
    "pixel": "d9",
    "barramento": None, "RAM": None, "PC": None, "acumulador": None, "latch": None, "polling": None,
    "opcode": None, "registrador": None, "flip-flop": None, "ULA": None, "CPU": None,
    "ASCII": None, "Unicode": None, "UTF-8": None, "hardware": None, "processador": None,
}


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


def texto_visivel(h):
    """O que o leitor vê sem clicar: sem <details>, sem script, sem estilo."""
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"<details.*?</details>", " ", h, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", h))


def portao_de_vocabulario(did, visivel):
    baixo = visivel.lower()
    for termo in PROCESSO:
        if termo in baixo:
            abortar(f"{did}: palavra de método na página: '{termo}'")
    ordem = [d["id"] for d in D.DEGRAUS]
    aqui = ordem.index(did) if did in ordem else (-1 if did == "conv" else len(ordem))
    for palavra, tela in TECNICAS.items():
        if re.search(r"(?<![\w-])" + re.escape(palavra.lower()) + r"(s|es)?(?![\w-])", baixo):
            if tela is None:
                abortar(f"{did}: '{palavra}' não é explicada em degrau nenhum")
                continue
            if ordem.index(tela) > aqui:
                abortar(f"{did}: '{palavra}' aparece antes do degrau que a explica ({tela})")


def linha_palavra(w):
    return (f'<div class="item"><p class="nome-item">{w["palavra"]}</p><ul>'
            f'<li><i>O que é:</i> {w["o_que_e"]}</li>'
            f'<li><i>Por que existe:</i> {w["por_que"]}</li></ul></div>')


def palavras_de(d):
    if not d.get("palavras"):
        return ""
    return ('<div class="palavras"><p class="rot">antes, as palavras deste degrau</p>'
            + "".join(linha_palavra(w) for w in d["palavras"]) + "</div>")


def o_que_falta():
    """pesquisa/o-que-falta.md: selos, notas e buracos, para quem audita."""
    L = ["# O que a página não mostra, e por quê", "",
         "Gerado por `gerar_site.py`. A página é para quem não sabe nada e não carrega isto.", "",
         "## Procedência de cada degrau", "",
         "| degrau | selo | fonte | derivado |", "|---|---|---|---|"]
    for d in D.DEGRAUS:
        L.append(f"| {d['numero']} {d['nome']} | {d['selo']} | {re.sub('<[^>]+>', '', d['ref'])} | {d.get('derivado') or ''} |")
    L += ["", "## Notas dos degraus", ""]
    for d in D.DEGRAUS:
        for n in d.get("notas", []):
            L.append(f"- **{d['numero']} {d['nome']}**: {n}")
    L += ["", "## Buracos declarados", "",
          "Mapa que esconde o que falta mente sobre o próprio tamanho. Estes são os buracos que este mapa sabe ter.", ""]
    for a, b, c in D.A_LER:
        L.append(f"- **{a}** ({b}): {c}")
    L += ["", "## O que cada degrau conserva e esquece, com a fonte", "",
          "| degrau | conserva | esquece | fonte |", "|---|---|---|---|"]
    for a, b, c, d in D.FECHO["linhas"]:
        L.append(f"| {a} | {b} | {c} | {d} |")
    os.makedirs(os.path.join(AQUI, "pesquisa"), exist_ok=True)
    open(os.path.join(AQUI, "pesquisa", "o-que-falta.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


def selo(chave):
    cls, rot = SELOS[chave]
    return f'<span class="selo {cls}">{rot}</span>'


def prova(d):
    """De onde isto vem: a passagem, em inglês e em português, e o capítulo.
    Selo, nota e buraco ficam fora da página (pesquisa/o-que-falta.md)."""
    partes = [f'<div class="fonte">{D.FONTES[d["fonte"]].split(",")[0]} · {html.escape(d["ref"])}</div>']
    for en, pt in d["citacoes"]:
        partes.append(
            f'<blockquote><span class="en" lang="en">{en}</span>'
            f'<span class="pt">{pt}</span>'
            f'<cite>{html.escape(d["ref"])}</cite></blockquote>')
    return ('<details class="prova"><summary>de onde isto vem</summary>'
            '<div class="prova-corpo">' + "".join(partes) + "</div></details>")


def matematica(d):
    linhas = "".join(
        f'<p class="expr">{e}</p><p class="leitura"><b>lê-se:</b> {l}.</p>'
        for e, l in d["matematica"])
    return (f'<div class="mat"><p class="obj">a matemática daqui · <b>{d["objeto"]}</b></p>'
            f'{linhas}</div>')


def convencoes():
    itens = "".join(
        f'<div class="sinal"><p class="expr">{e}</p>'
        f'<p><b>{c}</b>: {o}. <span class="lese">lê-se:</span> {l}.</p></div>'
        for c, o, e, l in D.CONVENCOES)
    return f"""
<section class="degrau" id="conv" data-nome="Como ler os símbolos">
  <header><p class="regime">antes de tudo · como ler os símbolos desta página</p><h2>Sete sinais, e como cada um se lê</h2></header>
  <p class="tese">Cada expressão desta página vem com a leitura em voz alta logo abaixo. Esta folha diz o que cada tipo de sinal é.</p>
  <div class="sinais">{itens}</div>
  <p class="corpo">Nenhum sinal aparece antes de estar nesta folha. Em cada degrau, as palavras novas vêm explicadas antes de aparecerem. Onde o símbolo é mais curto que a frase, a frase vence.</p>
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
  {palavras_de(d)}
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
    itens = "".join(
        f'<div class="sinal"><p class="expr degr">{a}</p>'
        f'<p>conserva <b>{b}</b>; esquece <b>{c}</b>.</p></div>'
        for a, b, c, _fonte in f["linhas"])
    return f"""
<section class="degrau" id="{f['id']}" data-nome="{html.escape(f['nome'])}">
  <header><p class="regime">fecho</p><h2>{f['titulo']}</h2></header>
  <p class="tese">{f['tese']}</p>
  <div class="sinais">{itens}</div>
  <p class="corpo">{f['corpo']}</p>
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
    portao_de_vocabulario("conv", texto_visivel(convencoes()))
    for d in D.DEGRAUS:
        portao_de_vocabulario(d["id"], texto_visivel(degrau(d)))
    portao_de_vocabulario("d10", texto_visivel(fecho(D.FECHO)))
    corpo = convencoes() + "".join(degrau(d) for d in D.DEGRAUS) + fecho(D.FECHO)
    pag = f"""<!doctype html>
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
  <p class="nota">Texto e figuras: CC BY-SA 4.0 · código: MIT · as frases dos livros pertencem aos seus autores e aparecem com fonte e capítulo. <a href="https://github.com/mateusalkimim/hello-world-machine">hello-world-machine</a></p>
</footer>
</div>
<script>
{js}
</script>
</body>
</html>
"""
    portao_de_vocabulario("d10", texto_visivel(pag))
    return pag


def main():
    saida = os.path.join(AQUI, "pt", "index.html")
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    h = pagina()
    with open(saida, "w", encoding="utf-8") as f:
        f.write(h)
    o_que_falta()
    n = len(D.DEGRAUS)
    cit = sum(len(d["citacoes"]) for d in D.DEGRAUS)
    ex = sum(len(d["matematica"]) for d in D.DEGRAUS)
    pal = sum(len(d.get("palavras", [])) for d in D.DEGRAUS)
    print(f"pt/index.html: convenções + {n} degraus + fecho, {pal} palavras explicadas, {cit} passagens, {ex} expressões com lê-se, {len(h)} bytes; pesquisa/o-que-falta.md atualizado")


if __name__ == "__main__":
    main()
