# -*- coding: utf-8 -*-
"""Portão da página. Mede a TELA, não o código.

Roda:  CHROME=/caminho/do/chrome python3 conferir_pagina.py pt/index.html
       CONTROLE=1 ...  planta um elemento largo e exige que a sonda acuse

Duas cicatrizes deste projeto estão gravadas aqui:

  a RÉGUA — transbordo se mede contra `documentElement.clientWidth`, nunca
  contra `innerWidth`, que ESTICA junto com o defeito. Dois números crescendo
  juntos dão zero, e uma sonda assim já reportou "sem transbordo" em dez
  páginas que transbordavam;

  o CONTENTOR — elemento largo dentro de algo com overflow-x:auto não é
  defeito, é o que rolar significa. A 1ª versão desta sonda acusou o mapa que
  rola de propósito no telefone: falso positivo dela, não da página.

E mede tinta no canvas, mas essa medida é FRACA e está anotada como tal: ela
aprovou um instrumento que abria sem nenhuma onda desenhada, porque os rótulos
já pintavam pixel bastante. Quem pegou foi o Qwen3-VL lendo a captura.
"""
import sys, os, json
from playwright.sync_api import sync_playwright
EXE = os.environ.get("CHROME")
URL = "file://" + os.path.abspath(sys.argv[1])
TELAS = [(1440, 900), (1366, 768), (390, 844)]

SONDA = """() => {
  const R = {};
  // A REGUA FIRME: clientWidth nao estica com o defeito; innerWidth estica.
  const W = document.documentElement.clientWidth;
  R.viewport = W;
  // A medida que decide: o CORPO da pagina rola na horizontal?
  R.corpoRola = document.documentElement.scrollWidth - W;

  // Elemento largo DENTRO de um contentor que rola de proposito nao e defeito
  // — foi o que a 1a versao desta sonda acusou, e era falso positivo dela.
  const rolante = e => {
    for (let a = e.parentElement; a; a = a.parentElement) {
      const ox = getComputedStyle(a).overflowX;
      if (ox === 'auto' || ox === 'scroll') return true;
    }
    return false;
  };
  R.transbordo = [];
  document.querySelectorAll('body *').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width > 0 && (r.right > W + 1.5 || r.left < -1.5) && !rolante(e)) {
      const nome = e.id || (typeof e.className === 'string' ? e.className : e.tagName);
      R.transbordo.push(String(nome).slice(0,42) + ' ' + Math.round(r.right));
    }
  });
  R.transbordo = R.transbordo.slice(0, 8);
  const svg = document.querySelector('.mapa svg');
  R.mapa = svg ? {w: Math.round(svg.getBoundingClientRect().width),
                  h: Math.round(svg.getBoundingClientRect().height),
                  nos: svg.querySelectorAll('a.no').length} : null;
  R.canvas = [];
  document.querySelectorAll('canvas').forEach(c => {
    const g = c.getContext('2d');
    const d = g.getImageData(0,0,c.width,c.height).data;
    let pintados = 0;
    for (let i=3; i<d.length; i+=4*17) if (d[i] > 8) pintados++;
    R.canvas.push({id: c.parentNode.id, w: Math.round(c.getBoundingClientRect().width),
                   h: Math.round(c.getBoundingClientRect().height), tinta: pintados});
  });
  R.selos = {citacao: 0, sintese: 0, oficio: 0};
  document.querySelectorAll('.selo').forEach(s => {
    const t = s.textContent.trim();
    if (t.startsWith('cita')) R.selos.citacao++;
    else if (t.startsWith('sínt')) R.selos.sintese++;
    else R.selos.oficio++;
  });
  R.campos = document.querySelectorAll('.campo').length;
  R.degraus = document.querySelectorAll('article.degrau').length;
  R.instrumentos = document.querySelectorAll('.instr').length;
  R.avisos = [...document.querySelectorAll('.aviso')].map(a=>a.textContent);
  return R;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    ruim = 0
    for (w, h) in TELAS:
        p = b.new_page(viewport={"width": w, "height": h})
        erros = []
        p.on("pageerror", lambda e: erros.append(str(e)))
        p.goto(URL); p.wait_for_timeout(700)
        R = p.evaluate(SONDA)
        # A página é um VISOR: só a tela à vista monta o seu canvas. Mede-se cada
        # tela (pelo hash) e fica, por canvas, a medida com mais tinta — senão a
        # sonda acusa "em branco" os instrumentos das telas escondidas (2026-10-03).
        _ids = p.evaluate("[...document.querySelectorAll('.tela')].map(s => s.id)")
        _best = {}
        for _sid in _ids:
            p.evaluate("(id) => { location.hash = '#' + id; }", _sid); p.wait_for_timeout(350)
            _Rk = p.evaluate(SONDA)
            for _c in _Rk["canvas"]:
                if _c["tinta"] > _best.get(_c["id"], {"tinta": -1})["tinta"]:
                    _best[_c["id"]] = _c
        if _best:
            R["canvas"] = list(_best.values())
        if os.environ.get("CONTROLE"):
            p.evaluate("() => { const d = document.createElement('div');"
                       "d.style.cssText='width:3000px;height:20px';"
                       "d.id='defeito-plantado'; document.body.appendChild(d); }")
            C = p.evaluate(SONDA)
            ok = C["corpoRola"] > 1 or any("defeito-plantado" in x for x in C["transbordo"])
            print(f"  controle negativo: {'ACUSOU — ok' if ok else 'NAO VIU — sonda cega'}")
            if not ok: ruim += 1
        vazios = [c for c in R["canvas"] if c["tinta"] < 40]
        print(f"--- {w}x{h} ---")
        print(f"  mapa: {R['mapa']}")
        print(f"  degraus={R['degraus']} campos={R['campos']} "
              f"instrumentos={R['instrumentos']} selos={R['selos']}")
        print(f"  canvas com tinta: {len(R['canvas'])-len(vazios)}/{len(R['canvas'])}")
        if R["corpoRola"] > 1:
            print(f"  FALHA o corpo rola {R['corpoRola']}px na horizontal"); ruim += 1
        if R["transbordo"]: print(f"  FALHA transbordo: {R['transbordo']}"); ruim += 1
        if vazios:         print(f"  FALHA canvas em branco: {vazios}");     ruim += 1
        if R["avisos"]:    print(f"  FALHA instrumento caiu: {R['avisos']}");ruim += 1
        if erros:          print(f"  FALHA erro de JS: {erros[:2]}");        ruim += 1
        p.close()
    b.close()
print(f"\n{ruim} achados")
sys.exit(1 if ruim else 0)
