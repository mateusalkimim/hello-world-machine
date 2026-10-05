#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Portão dos instrumentos: CLICA em cada botão e mede se o desenho mudou.

Existe por causa de um defeito real. Na 1ª tradução desta página o modelo verteu
`data-acao="modo"` para `"mode"` e `"pulso"` para `"step"` — traduções CORRETAS
de palavras que por acaso eram identificadores. O QA de idioma passou tudo em
verde, porque a frase em inglês afirmava exatamente o que a portuguesa afirmava.
E cinco botões ficaram mudos na página em inglês.

Nenhuma sonda de TEXTO acha isso. Só clicar acha. Por isso este portão não lê o
HTML: ele abre a página, aperta cada botão e compara o canvas antes e depois.

Roda:  CHROME=/caminho/do/chrome python3 conferir_instrumentos.py pt/index.html
"""
import os, sys, hashlib
from playwright.sync_api import sync_playwright

EXE = os.environ.get("CHROME")

# A 1a versao amostrava 1 byte em 401 e deu DOIS falsos positivos: nao via um
# pulso que muda 1/32 da onda. Assinatura de imagem tem de ser sobre TODOS os
# bytes — amostragem esparsa em desenho de linha fina mede o fundo.
ASSINA = """(el) => {
  const c = el.querySelector('canvas');
  if (!c) return null;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  let h = 2166136261;
  for (let i = 0; i < d.length; i++) { h ^= d[i]; h = Math.imul(h, 16777619); }
  return h >>> 0;
}"""

def main(caminho):
    url = "file://" + os.path.abspath(caminho)
    achados, testados = [], 0
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        p = b.new_page(viewport={"width": 1280, "height": 900})
        erros = []
        p.on("pageerror", lambda e: erros.append(str(e)))
        p.goto(url); p.wait_for_timeout(700)

        if os.environ.get("CONTROLE"):
            # Planta EXATAMENTE o defeito que criou este portao: traduz o valor
            # de um data-acao, como o modelo fez com "modo"->"mode". O botao
            # continua na tela, com o rotulo certo, e nao faz mais nada.
            p.evaluate("""() => {
              const b = document.querySelector('[data-acao=\"step\"]');
              if (b) b.setAttribute('data-acao', 'pulse');
            }""")
            print("controle negativo: um data-acao foi traduzido de propósito")

        instr = p.locator(".instr")
        n = instr.count()
        print(f"instrumentos na página: {n}")
        for i in range(n):
            el = instr.nth(i)
            ident = el.get_attribute("id") or f"#{i}"
            # [0] a página é um visor: a tela do instrumento precisa estar à
            # vista, senão o canvas tem largura zero e os botões não existem
            p.evaluate("""(id) => { const s = document.getElementById(id).closest('section');
              if (s && s.id) { location.hash = '#' + s.id; } }""", ident)
            p.wait_for_timeout(350)
            # [1] montou? (o script põe .aviso quando cai)
            if el.locator(".aviso").count():
                achados.append(f"{ident}: não montou — "
                               f"{el.locator('.aviso').inner_text()[:80]}")
                continue
            # [2] pintou alguma coisa?
            antes = el.evaluate(ASSINA)
            if antes is None:
                achados.append(f"{ident}: sem canvas"); continue
            # [3] cada botão muda o desenho?
            bts = el.locator("button")
            for j in range(bts.count()):
                bt = bts.nth(j)
                acao = bt.get_attribute("data-acao")
                rot = bt.inner_text().strip()
                testados += 1

                if acao in ("playpause", "autorun"):
                    # Botao de ALTERNANCIA nao se mede pelo quadro seguinte:
                    # pausar corretamente nao muda nada no instante do clique.
                    # O que ele promete e que o desenho PARA de mudar — e que
                    # volte a mudar ao despausar. E isso que se mede.
                    bt.click(); p.wait_for_timeout(260)
                    x1 = el.evaluate(ASSINA); p.wait_for_timeout(420)
                    x2 = el.evaluate(ASSINA)
                    move1 = (x1 != x2)
                    bt.click(); p.wait_for_timeout(260)
                    y1 = el.evaluate(ASSINA); p.wait_for_timeout(420)
                    y2 = el.evaluate(ASSINA)
                    move2 = (y1 != y2)
                    # A alternancia esta correta quando UM estado desenha e o
                    # outro nao. A direcao NAO se assume: "pausar" comeca
                    # parando, "automatico" comeca andando — e a 1a versao
                    # desta condicao reprovou os DOIS por presumir a direcao.
                    if move1 == move2:
                        achados.append(
                            f"{ident} · botão {rot!r} (data-acao={acao!r}) não "
                            f"alterna: desenha={move1} depois={move2}")
                    continue

                a = el.evaluate(ASSINA)
                bt.click(); p.wait_for_timeout(340)
                d = el.evaluate(ASSINA)
                if a == d:
                    achados.append(f"{ident} · botão {rot!r} "
                                   f"(data-acao={acao!r}) não mudou nada")
        if erros:
            achados.append(f"erro de JS na página: {erros[:2]}")
        b.close()
    print(f"botões apertados: {testados}")
    for a in achados: print("  FALHA", a)
    print(f"\n{len(achados)} achados")
    return 1 if achados else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "pt/index.html"))
