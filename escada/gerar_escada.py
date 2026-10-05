#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera pt/index.html — a escada de abstrações, em seis famílias.

A página é um visor: uma tela por família (transistores, portas lógicas,
somadores, registradores, instruções, relógio), precedida da folha de
convenções e seguida do mapa. Em cada família: a tese, uma PREVISÃO antes de
mexer no instrumento, o instrumento (ou a figura), o corpo, a matemática
daqui com a leitura em voz alta, os degraus de dentro com os quatro campos e
as citações (fechados), uma pergunta de RECUPERAÇÃO com resposta que explica,
e a passagem que define a família (fechada).

O gerador ABORTA se:
  - uma aresta ou construção vier sem citação, ou citar degrau inexistente;
  - um degrau não tiver os quatro campos, ou um campo alegar fonte sem passagem;
  - um degrau não pertencer a exatamente UMA família, ou uma família citar
    degrau inexistente ou instrumento inexistente;
  - uma família vier sem passagem, sem previsão, sem recuperação, ou com
    resposta certa fora das opções;
  - a tese passar de 25 palavras ou o corpo de 60; uma expressão vier sem
    "lê-se"; sobrar inglês no texto visível (a prova fica na prova).
"""
import html
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import degraus as D      # noqa: E402
import conceitos as CO   # noqa: E402
import mapa as MAPA      # noqa: E402
import familias as F     # noqa: E402
sys.path.append(os.path.dirname(AQUI))   # a raiz vai ao FIM: ela tem outro degraus.py
import barra as BARRA    # noqa: E402

SAIDA = os.path.join(os.path.dirname(AQUI), "pt", "escada.html")
TESE_MAX, CORPO_MAX, LESE_MAX = 25, 60, 40
EN_SINAL = re.compile(r"\b(the|and|of|is|with|that|this|you|are)\b")

# Instrumento por família: cada um PROVA uma aresta do mapa, montando a peça.
# O valor de `data-acao` é identificador (token neutro), nunca palavra da tela.
INSTRUMENTOS = {
    "porta": ("rele-vira-porta", "Dois relés viram uma porta",
              "Ligue os dois e veja: <b>em série</b> a lâmpada só acende com os "
              "dois acionados, que é a porta E, feita de metal. A tabela-verdade "
              "não vem pronta: ela se preenche conforme você visita as combinações, "
              "e enquanto faltar linha o instrumento diz quantas faltam.",
              [("mode", "em série"), ("inA", "relé A"), ("inB", "relé B")], 230),
    "somador": ("portas-viram-conta", "Duas portas viram uma conta",
              "A porta OU-exclusivo dá a soma; a porta E dá o vai-um. A conta em "
              "binário aparece ao lado para você conferir que não é coincidência, "
              "e o caso que interessa é <b>1 + 1</b>.",
              [("inA", "A"), ("inB", "B")], 220),
    "flipflop": ("circuito-que-lembra", "O circuito que lembra",
              "<b>S</b> liga, <b>R</b> desliga, e <b>Q</b> é o que o circuito "
              "lembra. Aperte S e solte; aperte R e solte. Nos dois casos a "
              "entrada volta a ser (0, 0), e a saída é diferente. É essa a "
              "definição de lembrar, e é a coisa que nenhuma porta sozinha faz.",
              [("setS", "S — segurar"), ("setR", "R — segurar")], 240),
    "flipflop_b": ("nivel-x-borda", "Nível × borda, no mesmo relógio",
              "Os dois circuitos, o mesmo dado, o mesmo relógio. A faixa clara é "
              "o tempo em que o relógio está alto: o de <b>nível</b> copia o dado "
              "durante toda ela, e por isso <b>vaza</b>. O de <b>borda</b> copia "
              "só na linha pontilhada. Aperte tocar e veja os dois lado a lado.",
              [("playpause", "tocar"), ("restart", "reiniciar")], 260),
    "contador": ("contagem-aparece", "A contagem aparece sozinha",
              "Dê pulsos e olhe as ondas: cada estágio vira na <b>metade</b> da "
              "frequência do anterior. Ninguém projetou a contagem binária; ela "
              "é a fiação.",
              [("step", "um pulso"), ("autorun", "automático"), ("clear", "zerar")], 250),
}

MARCA_CLASSE = {
    "a": ("citação", "lido"),
    "b": ("síntese", "lido"),
    "d": ("ofício · confirmado", "oficio"),
    "d?": ("ofício · não confirmado", "oficio"),
}
NOME_REGIME = {"fisica": "ainda é eletricidade e ferro",
               "comb": "combinacional: a saída depende só das entradas de agora",
               "seq": "sequencial: a saída depende também do que veio antes",
               "arq": "arquitetura: peças em sequência, sob um controlador",
               "lingua": "linguagem: acima da máquina, o assunto é significado"}

FIGURAS = {
    "chave": """<svg viewBox="0 0 520 150" role="img" aria-label="Um relé: a corrente de controle puxa a lâmina, que fecha o contato da outra corrente">
      <text x="20" y="14" font-family="Inter, sans-serif" font-size="11" fill="#c9a266" font-weight="600" letter-spacing="1">RELÉ · uma corrente fecha a chave da outra</text>
      <g stroke="#5b8fc9" stroke-width="2" fill="none"><path d="M 30 100 L 90 100"/><path d="M 90 70 l 0 60" stroke-dasharray="3 3"/><rect x="82" y="70" width="16" height="36" fill="#14263f" stroke="#5b8fc9"/></g>
      <text x="60" y="122" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="#9fadc0">corrente de controle</text>
      <text x="90" y="62" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="#9fadc0">bobina</text>
      <g stroke="#6fbf6a" stroke-width="2.4" fill="none"><path d="M 170 60 L 230 60"/><path d="M 230 60 L 262 42"/><path d="M 268 60 L 330 60"/></g>
      <circle cx="230" cy="60" r="4" fill="#6fbf6a"/><circle cx="268" cy="60" r="4" fill="#33465f"/>
      <text x="250" y="90" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="#9fadc0">a lâmina: aberta = 0, fechada = 1</text>
      <path d="M 120 88 L 230 64" stroke="#c9a266" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
      <text x="400" y="56" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-size="22" fill="#e8e2d6">0 ou 1</text>
      <text x="400" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="#9fadc0">a corrente controlada: passa ou não passa</text>
      <text x="400" y="120" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="#9fadc0">nenhum meio-termo</text>
    </svg>""",
    "ordem": """<svg viewBox="0 0 520 150" role="img" aria-label="O contador de programa aponta uma gaveta; o byte que está nela é lido como ordem">
      <text x="20" y="14" font-family="Inter, sans-serif" font-size="11" fill="#c9a266" font-weight="600" letter-spacing="1">CONTADOR DE PROGRAMA · aponta qual gaveta será lida como ORDEM agora</text>
      <g font-family="Spline Sans Mono, ui-monospace, monospace" font-size="13" text-anchor="middle">
        <rect x="20" y="40" width="110" height="46" rx="4" fill="#0d1c30" stroke="#a883c9"/><text x="75" y="60" fill="#9fadc0">PC</text><text x="75" y="78" fill="#e8e2d6">0004</text>
        <path d="M 130 63 L 180 63" stroke="#a883c9" stroke-width="2"/><path d="M 176 59 L 184 63 L 176 67 Z" fill="#a883c9"/>
        <rect x="190" y="30" width="60" height="30" fill="#0d1c30" stroke="#1e3050"/><text x="220" y="50" fill="#5b6b86">0003</text>
        <rect x="190" y="62" width="60" height="30" fill="#0d1c30" stroke="#a883c9" stroke-width="2"/><text x="220" y="82" fill="#e8e2d6">36</text>
        <rect x="190" y="94" width="60" height="30" fill="#0d1c30" stroke="#1e3050"/><text x="220" y="114" fill="#5b6b86">4F</text>
        <path d="M 250 77 L 300 77" stroke="#a883c9" stroke-width="2"/><path d="M 296 73 L 304 77 L 296 81 Z" fill="#a883c9"/>
        <rect x="310" y="48" width="190" height="56" rx="4" fill="#0d1c30" stroke="#a883c9"/>
        <text x="405" y="70" fill="#9fadc0" font-family="Inter, sans-serif" font-size="11">o byte 36 é lido como</text><text x="405" y="92" fill="#e8e2d6" font-family="Inter, sans-serif">“escreva em [HL]”</text>
      </g>
      <text x="220" y="142" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="#9fadc0">o 4F da gaveta de baixo é uma letra; nada no byte diz isso, só o apontador</text>
    </svg>""",
}


def palavras(h):
    return len(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())


def abortar(msg):
    sys.stderr.write("ABORTADO: " + msg + "\n")
    sys.exit(1)


def sem_ingles(texto, onde):
    if EN_SINAL.search(html.unescape(re.sub(r"<[^>]+>", " ", texto))):
        abortar(f"{onde}: inglês no texto visível — a prova fica na prova")


# --- as conferências que abortam ---------------------------------------------
def conferir():
    nos = {i: (nome, nivel, diz) for i, nome, nivel, diz in D.DEGRAUS}
    for de, para, classe, fonte, ref, cit in D.ARESTAS:
        if not cit.strip():
            abortar(f"a aresta {de}→{para} não tem citação. Seta sem warrant não é desenhada.")
        if de not in nos or para not in nos:
            abortar(f"a aresta {de}→{para} cita degrau inexistente.")
    for degrau, peca, feita, fonte, ref, cit in D.CONSTRUCAO:
        if not cit.strip():
            abortar(f"a construção {peca} não tem citação.")
        if degrau is not None and degrau not in nos:
            abortar(f"a construção {peca} cita degrau inexistente {degrau!r}.")
    for chave in nos:
        if chave not in CO.CONCEITOS:
            abortar(f"o degrau {chave!r} não tem os quatro campos.")
        for campo, _rot in CO.CAMPOS:
            if campo not in CO.CONCEITOS[chave]:
                abortar(f"{chave}.{campo} não existe.")
            texto, classe, ref, cit, ratificado = CO.CONCEITOS[chave][campo]
            if not texto.strip():
                abortar(f"{chave}.{campo} está vazio.")
            if classe in ("a", "b") and not (cit or "").strip():
                abortar(f"{chave}.{campo} diz ser {classe!r} e não traz a passagem.")
    # as famílias
    vistos = {}
    for f in F.FAMILIAS:
        for m in f["membros"]:
            if m not in nos:
                abortar(f"família {f['id']}: degrau {m!r} não existe")
            if m in vistos:
                abortar(f"degrau {m!r} em duas famílias: {vistos[m]} e {f['id']}")
            vistos[m] = f["id"]
        for inst in ([f["instrumento"]] if isinstance(f["instrumento"], str) else (f["instrumento"] or [])):
            if inst not in INSTRUMENTOS:
                abortar(f"família {f['id']}: instrumento {inst!r} não existe")
        if not f["instrumento"] and f["figura"] not in FIGURAS:
            abortar(f"família {f['id']}: sem instrumento e sem figura")
        if not f["citacoes"] or any(not en.strip() or not pt.strip() for en, pt in f["citacoes"]):
            abortar(f"família {f['id']}: sem passagem lida (ou passagem sem tradução)")
        if f["fonte"] not in D.FONTES:
            abortar(f"família {f['id']}: fonte {f['fonte']!r} não está em FONTES")
        n = palavras(f["tese"])
        if n > TESE_MAX:
            abortar(f"família {f['id']}: tese com {n} palavras (máx. {TESE_MAX})")
        n = palavras(f["corpo"])
        if n > CORPO_MAX:
            abortar(f"família {f['id']}: corpo com {n} palavras (máx. {CORPO_MAX})")
        if not f["matematica"]:
            abortar(f"família {f['id']}: sem a matemática daqui")
        for expr, lese in f["matematica"]:
            if not expr.strip() or not lese.strip():
                abortar(f"família {f['id']}: expressão sem leitura em voz alta")
            if palavras(lese) > LESE_MAX:
                abortar(f"família {f['id']}: lê-se com {palavras(lese)} palavras (máx. {LESE_MAX})")
        for bloco in ("previsao", "recuperacao"):
            q = f.get(bloco)
            if not q or not q.get("pergunta") or not q.get("opcoes") or not q.get("porque"):
                abortar(f"família {f['id']}: sem {bloco} completa (pergunta, opções, porque)")
            if not 0 <= q["certa"] < len(q["opcoes"]):
                abortar(f"família {f['id']}: {bloco} com resposta certa fora das opções")
            sem_ingles(q["pergunta"] + " " + " ".join(q["opcoes"]) + " " + q["porque"], f"família {f['id']}.{bloco}")
        sem_ingles(f["tese"], f"família {f['id']}.tese")
        sem_ingles(f["corpo"], f"família {f['id']}.corpo")
    faltam = [k for k in nos if k not in vistos]
    if faltam:
        abortar(f"degraus sem família: {faltam}")
    return nos


# --- pedaços de página ---------------------------------------------------------
def selo(classe, ratificado):
    chave = "d?" if (classe == "d" and not ratificado) else classe
    rot, cls = MARCA_CLASSE[chave]
    data = f" · {ratificado}" if (classe == "d" and ratificado) else ""
    return f'<span class="selo {cls}">{rot}{data}</span>'


def campos_de(chave):
    out = []
    for campo, rot in CO.CAMPOS:
        texto, classe, ref, cit, ratificado = CO.CONCEITOS[chave][campo]
        prova = ""
        if cit:
            fonte = "sicp" if "SICP" in (ref or "") else "petzold"
            prova = (f'<details class="passagem"><summary>a passagem</summary>'
                     f'<blockquote>“{cit}”<cite>{D.FONTES[fonte]} · {html.escape(ref or "")}</cite></blockquote></details>')
        out.append(f'<div class="campo"><div class="rot">{html.escape(rot)} {selo(classe, ratificado)}</div>'
                   f'<p>{texto}</p>{prova}</div>')
    return "".join(out)


def instrumento_de(chave):
    ident, titulo, comoler, botoes, alt = INSTRUMENTOS[chave]
    bs = "".join(f'<button type="button" data-acao="{a}">{html.escape(r)}</button>' for a, r in botoes)
    return (f'<div class="instr" id="i-{ident}"><h4>{titulo}</h4><p class="comoler">{comoler}</p>'
            f'<canvas data-h="{alt}"></canvas><div class="botoes">{bs}</div>'
            f'<p class="prova">Este instrumento <b>é</b> a prova da seta: ele monta a peça no '
            f'navegador, sem o livro na mão. A passagem continua ali, como segunda testemunha.</p></div>')


def pergunta(f, bloco, rotulo):
    q = f[bloco]
    nome = f"{f['id']}-{bloco}"
    ops = "".join(
        f'<label><input type="radio" name="{nome}" value="{i}" id="{nome}-{i}"> <span>{html.escape(o)}</span></label>'
        for i, o in enumerate(q["opcoes"]))
    return (f'<section class="pergunta {bloco}" data-certa="{q["certa"]}">'
            f'<p class="rot">{rotulo}</p><p class="enunciado">{q["pergunta"]}</p>'
            f'<div class="opcoes">{ops}</div>'
            f'<button type="button" class="ver" data-pergunta="{nome}">ver a resposta</button>'
            f'<p class="porque" hidden><b></b> {q["porque"]}</p></section>')


def por_dentro(f, nos, entrada, dentro):
    partes = []
    for chave in f["membros"]:
        nome, nivel, diz = nos[chave]
        reg = MAPA.REGIME[chave]
        setas = "".join(
            f'<details class="seta"><summary>é feito de <b>{html.escape(nos[de][0])}</b> — {classe}; a fonte diz:</summary>'
            f'<blockquote>“{cit}”<cite>{D.FONTES[fonte]} · {html.escape(ref)}</cite></blockquote>'
            + ("".join(
                f'<blockquote>“{c2}”<cite>{D.FONTES[f2]} · {html.escape(r2)}</cite></blockquote>'
                f'<p class="duas">Duas testemunhas independentes, chegando de lados opostos da escada.</p>'
                for f2, r2, c2 in [D.SEGUNDA_TESTEMUNHA[(de, chave)]]) if (de, chave) in D.SEGUNDA_TESTEMUNHA else "")
            + '</details>'
            for de, classe, fonte, ref, cit in entrada.get(chave, []))
        pecas = dentro.get(chave, [])
        dd = ""
        if pecas:
            dd = (f'<details class="dentro"><summary>as peças de dentro: {len(pecas)}, cada uma com a frase que a sustenta</summary>'
                  + "".join(f'<blockquote><b>{html.escape(pc)}</b> ← {html.escape(ft)}<br>“{ct}”<cite>{D.FONTES[fo]} · {html.escape(rf)}</cite></blockquote>'
                            for pc, ft, fo, rf, ct in pecas) + '</details>')
        partes.append(
            f'<details class="degrau" id="{chave}"><summary><b>{html.escape(nome)}</b> '
            f'<span class="diz">{diz}</span></summary>'
            f'<p class="regime">nível {nivel} · {NOME_REGIME[reg]}</p>'
            f'{campos_de(chave)}{setas}{dd}</details>')
    return "".join(partes)


def familia(i, f, nos, entrada, dentro):
    cor = F.COR[f["id"]]
    insts = [f["instrumento"]] if isinstance(f["instrumento"], str) else (f["instrumento"] or [])
    figura = "".join(instrumento_de(i) for i in insts) if insts else f'<figure class="fig">{FIGURAS[f["figura"]]}</figure>'
    mat = "".join(f'<p class="expr">{e}</p><p class="leitura"><b>lê-se:</b> {l}.</p>' for e, l in f["matematica"])
    prova = "".join(
        f'<blockquote lang="en">{en}</blockquote><p class="traducao">{pt} (tradução do autor)</p>'
        for en, pt in f["citacoes"])
    return f"""
<section class="tela familia" id="{f['id']}" data-nome="{html.escape(f['nome'])}" style="--fam:{cor}">
  <header><p class="eyebrow">família {i} de {len(F.FAMILIAS)} · <b>{f['nome']}</b> {f['verbo']}</p><h2>{f['titulo']}</h2></header>
  <p class="tese">{f['tese']}</p>
  {pergunta(f, "previsao", "antes de mexer, aposte")}
  {figura}
  <p class="corpo">{f['corpo']}</p>
  <div class="mat"><p class="obj">a matemática daqui · <b>{f['objeto']}</b></p>{mat}</div>
  <details class="pordentro"><summary>por dentro: {len(f['membros'])} {'degrau' if len(f['membros']) == 1 else 'degraus'} desta família, com os quatro campos e as citações</summary>
    {por_dentro(f, nos, entrada, dentro)}
  </details>
  {pergunta(f, "recuperacao", "antes de seguir, responda")}
  <details class="prova-fam"><summary>a passagem que define a família</summary>
    <div class="fonte">{D.FONTES[f['fonte']]} · {html.escape(f['ref'])}</div>{prova}
  </details>
</section>"""


def convencoes():
    nomes = {d[0]: d[1] for d in D.DEGRAUS}
    fams = "".join(
        f'<div class="sinal"><p class="expr fam" style="color:{F.COR[f["id"]]}">{f["nome"]}</p>'
        f'<p><b>{f["verbo"]}</b>: {", ".join(html.escape(nomes[m]) for m in f["membros"])}.</p></div>'
        for f in F.FAMILIAS)
    sinais = "".join(
        f'<div class="sinal"><p class="expr">{e}</p><p><b>{c}</b>: {o}. <span class="lese">lê-se:</span> {l}.</p></div>'
        for c, o, e, l in F.CONVENCOES)
    return f"""
<section class="tela" id="conv" data-nome="As seis famílias, e como ler os sinais">
  <header><p class="eyebrow">antes de tudo</p><h2>Seis famílias, e o que cada uma faz com o número</h2></header>
  <p class="tese">Toda peça de um computador cabe numa de seis famílias, nomeadas pelo que fazem com o número. As famílias vêm primeiro; os nomes das peças, depois.</p>
  <div class="sinais">{fams}</div>
  <p class="corpo">Em cada família: a ideia principal, as palavras novas explicadas antes de aparecerem, uma aposta, um instrumento ou uma figura, as peças, a matemática daqui lida em voz alta, e uma pergunta no fim. De onde cada coisa vem fica a um clique.</p>
  <p class="rot">como ler os sinais desta página</p>
  <div class="sinais">{sinais}</div>
</section>"""


def mapa_tela():
    chave = "".join(
        f'<span class="chave"><i style="background:{F.COR[f["id"]]}"></i>{MAPA.NOME_FAMILIA[f["id"]]}</span>'
        for f in F.FAMILIAS)
    return f"""
<section class="tela" id="mapa" data-nome="O mapa">
  <header><p class="eyebrow">o fecho</p><h2>O mapa inteiro, de baixo para cima</h2></header>
  <p class="tese">O eletroímã é o chão; o paradigma é o topo. Cada seta diz de que a peça de cima é feita, ou de que ela depende. Clique num nome para ir à peça.</p>
  <div class="mapa">{MAPA.desenhar()}</div>
  <p class="chaves">{chave}</p>
  <p class="corpo">A cor do nó é a família. A linha dourada marca onde o assunto deixa de ser eletricidade e passa a ser lógica; a roxa, onde deixa de ser circuito e passa a ser linguagem. As setas tracejadas apontam para o que ainda não está na escada.</p>
</section>"""


def o_que_falta(dentro):
    """pesquisa/o-que-falta.md — o que a página não mostra, para quem audita."""
    linhas = ["# O que falta na escada, e por quê", "",
              "Gerado por `gerar_escada.py`. A página é para quem não sabe nada e não carrega isto; quem audita o mapa lê aqui.", "",
              "## Passagens lidas que não viraram seta", ""]
    for a, fo, e, motivo in D.NAO_LIDO:
        linhas.append(f"- **{a}** ({fo}): {e}. {re.sub('<[^>]+>', '', motivo)}")
    linhas += ["", "## Construções verificadas, ainda fora da escada", "",
               "Passaram na conferência literal, mas o degrau em que pousam ainda não foi lido.", ""]
    for pc, ft, fo, rf, ct in dentro.get(None, []):
        linhas.append(f"- **{pc}** ← {ft} — *{D.FONTES[fo]}, {rf}*")
    fora = getattr(D, "FORA_DO_MAPA", set())
    if fora:
        linhas += ["", "## Setas lidas que o mapa não desenha", ""]
        for de, para in sorted(fora):
            linhas.append(f"- **{de} → {para}**: na grade de três colunas ela cruzaria outra seta; vale, com a citação, na página da família.")
    open(os.path.join(AQUI, "pesquisa", "o-que-falta.md"), "w", encoding="utf-8").write("\n".join(linhas) + "\n")


# --- a página para quem não sabe nada (2026-10-03) ----------------------------
# Palavras que são do PROCESSO de fazer o mapa, não do conteúdo: não entram na
# página. Quem procura método lê o README e a pesquisa.
PROCESSO = ["selo", "ofício", "oficio", "warrant", "prova da seta", "confirmado", "versão", "amostra", "forma nova",
            "segunda testemunha", "tradução do autor", "citação", "síntese", "procedência",
            "2026-", "ratific", "não confirmado", "modelo de linguagem"]
# Palavras técnicas e a tela em que cada uma é EXPLICADA. Antes dessa tela a
# palavra não pode aparecer; None = nunca aparece na página.
TECNICAS = {
    "corrente": "transistores", "fio": "transistores", "circuito": "transistores", "chave": "transistores",
    "ímã": "transistores", "eletroímã": "transistores", "relé": "transistores", "transistor": "transistores",
    "limiar": "transistores", "válvula": "transistores", "semicondutor": "transistores", "silício": "transistores",
    "porta lógica": "portas", "bit": "somadores", "byte": "somadores", "binário": "somadores", "vai-um": "somadores",
    "somador": "somadores", "ULA": "somadores", "flip-flop": "registradores", "registrador": "registradores",
    "contador": "registradores", "memória": "registradores", "endereço": "registradores",
    "relógio": "relogio", "oscilador": "relogio", "instrução": "instrucoes", "programa": "instrucoes",
    "montador": "instrucoes", "interpretador": "instrucoes", "compilador": "instrucoes", "paradigma": "instrucoes", "controlador": "instrucoes",
    "barramento": None, "decodificador": None, "latch": None, "gate": None, "clock": None,
    "tri-state": None, "acumulador": None,
}
ORDEM = [f["id"] for f in F.FAMILIAS]


def texto_visivel(h):
    h = re.sub(r"<details.*?</details>", " ", h, flags=re.S)       # o que fica fechado não conta
    return html.unescape(re.sub(r"<[^>]+>", " ", h))


def portao_de_vocabulario(fid, visivel):
    baixo = visivel.lower()
    for termo in PROCESSO:
        if termo in baixo:
            abortar(f"família {fid}: palavra de processo na página: {termo!r}")
    aqui = ORDEM.index(fid)
    # os NOMES das famílias são apresentados na primeira tela, antes de tudo:
    # podem aparecer em qualquer família ("é outra família, a dos registradores")
    for fam in F.FAMILIAS:
        baixo = re.sub(r"(?<![\w-])" + re.escape(fam["nome"].lower()) + r"(?![\w-])", " ", baixo)
    for palavra, tela in TECNICAS.items():
        if re.search(r"(?<![\w-])" + re.escape(palavra.lower()) + r"(s|es)?(?![\w-])", baixo):
            if tela is None:
                abortar(f"família {fid}: a palavra {palavra!r} não se explica em tela nenhuma e aparece aqui")
            if ORDEM.index(tela) > aqui:
                abortar(f"família {fid}: {palavra!r} aparece antes da tela que a explica ({tela})")


def linha_palavra(w):
    return (f'<div class="item"><p class="nome-item">{w["palavra"]}</p><ul>'
            f'<li><i>O que é:</i> {w["o_que_e"]}</li>'
            f'<li><i>Por que existe:</i> {w["por_que"]}</li></ul></div>')


def linha_peca(chave, nos):
    nome, c = nos[chave][0], CO.CONCEITOS[chave]
    return (f'<div class="item" id="{chave}"><p class="nome-item">{html.escape(nome)}</p><ul>'
            f'<li><i>O que é:</i> {c["o_que_e"][0]}</li>'
            f'<li><i>Por que existe:</i> {c["por_que_existe"][0]}</li></ul></div>')


def fontes_pecas(membros):
    out = []
    for chave in membros:
        c = CO.CONCEITOS[chave]
        for campo in ("o_que_e", "por_que_existe"):
            cit, ref = c[campo][3], c[campo][2]
            if cit:
                fonte = "sicp" if "SICP" in (ref or "") else "petzold"
                out.append(f'<blockquote lang="en">{cit}<cite>{D.FONTES[fonte]} · {html.escape(ref or "")}</cite></blockquote>')
    return "".join(out)


def familia_v3(i, f, nos):
    cor = F.COR[f["id"]]
    insts = [f["instrumento"]] if isinstance(f["instrumento"], str) else (f["instrumento"] or [])
    figura = "".join(instrumento_de(x) for x in insts) if insts else f'<figure class="fig">{FIGURAS[f["figura"]]}</figure>'
    figura = re.sub(r'<p class="prova">.*?</p>', "", figura, flags=re.S)
    palavras = "".join(linha_palavra(w) for w in f.get("palavras", []))
    pecas = "".join(linha_peca(m, nos) for m in f["membros"])
    mat = "".join(f'<p class="expr">{e}</p><p class="leitura"><b>lê-se:</b> {l}.</p>' for e, l in f["matematica"])
    fonte = "".join(f'<blockquote lang="en">{en}<cite>{D.FONTES[f["fonte"]]} · {html.escape(f["ref"])}</cite></blockquote><p class="traducao">{pt}</p>' for en, pt in f["citacoes"])
    h = f"""
<section class="tela familia" id="{f['id']}" data-nome="{html.escape(f['nome'])}" style="--fam:{cor}">
  <header><p class="eyebrow">família {i} de {len(F.FAMILIAS)} · <b>{f['nome']}</b> {f['verbo']}</p><h2>{f['titulo']}</h2></header>
  <p class="tese">{f['tese']}</p>
  <div class="palavras"><p class="rot">antes, as palavras desta tela</p>{palavras}</div>
  {pergunta(f, "previsao", "antes de mexer, aposte")}
  {figura}
  <div class="pecas"><p class="rot">as peças desta família</p>{pecas}</div>
  <p class="corpo">{f['corpo']}</p>
  <div class="mat"><p class="obj">a matemática daqui · <b>{f['objeto']}</b></p>{mat}</div>
  {pergunta(f, "recuperacao", "antes de seguir, responda")}
  <details class="fonte"><summary>de onde isto vem</summary>{fonte}{fontes_pecas(f["membros"])}</details>
</section>"""
    portao_de_vocabulario(f["id"], texto_visivel(h))
    return h


def amostra(fid, saida):
    nos = conferir()
    f = next(x for x in F.FAMILIAS if x["id"] == fid)
    i = ORDEM.index(fid) + 1
    css = open(os.path.join(AQUI, "pele.css"), encoding="utf-8").read()
    extra = open(os.path.join(AQUI, "pele-visor.css"), encoding="utf-8").read()
    js = open(os.path.join(AQUI, "instrumentos.js"), encoding="utf-8").read()
    corpo = familia_v3(i, f, nos)
    pag = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>A escada de abstrações — {f['nome']}</title>
<style>{css}
{extra}
.item{{margin:10px 0 0;max-width:760px}}
.nome-item{{margin:0;font-size:16px;color:var(--fam,var(--ouro));font-weight:600}}
.item ul{{margin:3px 0 0;padding-left:1.2em;font-size:16px;line-height:1.55;color:#c9d2df}}
.item ul li{{margin:2px 0}} .item i{{font-style:normal;color:var(--fraco);font-size:13px;letter-spacing:.04em}}
.palavras .rot,.pecas .rot{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ouro);margin:0 0 8px}}
details.fonte{{margin-top:8px}} details.fonte summary{{font-size:12.5px;color:var(--fraco)}}
.traducao{{font-size:13px;color:#b9c4d4;margin:4px 0 8px}}
</style></head><body><div class="caixa">
<div class="cab"><div><p class="eyebrow">abstraction-ladder</p><h1>A escada de abstrações</h1></div></div>
<div id="telas">{corpo}</div>
<footer><b>A escada de abstrações</b> — Mateus Alkimim · código <b>MIT</b>, conteúdo <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br">CC BY-SA 4.0</a>.</footer>
</div><script>window.ESCADA_MONTAR = null;</script><script>{js}</script></body></html>"""
    portao_de_vocabulario(fid, texto_visivel(re.sub(r"<(script|style)>.*?</\1>", " ", pag, flags=re.S)))
    open(saida, "w", encoding="utf-8").write(pag)
    vis = texto_visivel(corpo)
    print(f"amostra {fid}: {len(vis.split())} palavras visíveis, {len(f.get('palavras', []))} palavras explicadas, {len(f['membros'])} peças")


def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "--amostra":
        return amostra(sys.argv[2], sys.argv[3])
    nos = conferir()
    dentro = {}
    for degrau, peca, feita, fonte, ref, cit in D.CONSTRUCAO:
        dentro.setdefault(degrau, []).append((peca, feita, fonte, ref, cit))
    telas = [convencoes()] + [familia_v3(i + 1, f, nos) for i, f in enumerate(F.FAMILIAS)] + [mapa_tela()]
    trilha = [dict(id="conv", tok="lê-se", nome="sinais")] + [
        dict(id=f["id"], tok=f["nome"], nome=f["verbo"], cor=F.COR[f["id"]]) for f in F.FAMILIAS] + [dict(id="mapa", tok="mapa", nome="o fecho")]
    css = open(os.path.join(AQUI, "pele.css"), encoding="utf-8").read()
    extra = open(os.path.join(AQUI, "pele-visor.css"), encoding="utf-8").read()
    visor = open(os.path.join(AQUI, "visor.js"), encoding="utf-8").read().replace("__TRILHA__", json.dumps(trilha, ensure_ascii=False))
    js = open(os.path.join(AQUI, "instrumentos.js"), encoding="utf-8").read()
    pag = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A escada de abstrações — seis famílias, do transistor à instrução</title>
<meta name="description" content="Uma saudação sai de uma pessoa, atravessa uma máquina que só sabe se há corrente ou não, e volta. Seis famílias de circuitos são tudo o que precisa existir no meio: transistores ligam e desligam, portas decidem, somadores fazem conta, registradores guardam, instruções mandam, o relógio marca o tempo. Para quem não sabe nada, com instrumento, aposta e pergunta em cada família.">
<style>{css}
{extra}
{BARRA.CSS}</style>
</head>
<body>
<div class="caixa">
{BARRA.barra("escada")}
<div class="cab"><div><p class="eyebrow">hello-world-machine</p><h1>A escada de abstrações</h1></div>
<p class="nota">← → no teclado; uma família por tela</p></div>
<div class="trilha" id="trilha" aria-label="as famílias"></div>
<div id="telas">{"".join(telas)}
</div>
<nav class="passo" aria-label="navegação"><button id="ant" type="button"><small>anterior</small><span></span></button>
<p class="pos" id="pos"></p><button id="prox" type="button" class="prox"><small>próximo</small><span></span></button></nav>
<footer><b>A escada de abstrações</b> — Mateus Alkimim · código <b>MIT</b>, conteúdo
<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br">CC BY-SA 4.0</a>.
As frases dos livros pertencem aos seus autores e aparecem com fonte e capítulo.</footer>
</div>
<script>{visor}</script>
<script>{js}</script>
</body>
</html>
"""
    # a página inteira, moldura incluída, sem palavra de processo
    portao_de_vocabulario(F.FAMILIAS[-1]["id"], texto_visivel(re.sub(r"<(script|style)>.*?</\1>", " ", pag, flags=re.S)))
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    open(SAIDA, "w", encoding="utf-8").write(pag)
    o_que_falta(dentro)
    n_cit = sum(len(f["citacoes"]) for f in F.FAMILIAS)
    print(f"pt/escada.html gerado — {len(F.FAMILIAS)} famílias, {len(D.DEGRAUS)} peças, "
          f"{sum(len(f.get('palavras', [])) for f in F.FAMILIAS)} palavras explicadas, {len(INSTRUMENTOS)} instrumentos, "
          f"{len(D.ARESTAS)} arestas com frase lida, {n_cit} frases de família; pesquisa/o-que-falta.md atualizado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
