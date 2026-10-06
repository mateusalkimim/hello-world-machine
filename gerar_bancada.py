#!/usr/bin/env python3
"""Gera pt/bancada.html — a bancada de circuitos dentro do material.

A fonte é `bancada/bancada.html`, uma página inteira que anda sozinha, e ela
fica como chegou. Este gerador não toca no jogo: cola a barra das quatro
partes no alto e veste a página com a pele das outras três
(`bancada/pele-itaca.css`: cores, fontes, cabeçalho) e acrescenta o MODO FIGURA
(`?figura=<id>`: o circuito pronto da missão como figura que se toca, para o
seminário). Cada troca é conferida
pela contagem: se a fonte mudar e a marca sumir, aborta em vez de gerar uma
página meio vestida. Só biblioteca padrão.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import barra as BARRA  # noqa: E402

FONTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500'
          '&family=Inter:wght@400;500;600&family=Spline+Sans+Mono:wght@400;500&display=swap">')
REDESENHAR = "buildPalette();buildParts();buildTrilha();draw();"

FIGURA_CSS = r"""
/* modo figura (?figura=<id>): a bancada vira figura interativa dentro do seminário.
   Fica a placa, a Mão, a tabela ao vivo (ao lado) e a frase do que cada peça faz; some tudo que é missão. */
html.figura body{padding:0;margin:0;background:transparent;overflow:hidden}
html.figura main{display:grid;grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"placa tabela" "status tabela";gap:.3rem .9rem;align-items:start;padding:.3rem;max-width:none}
html.figura.sem-tabela main{grid-template-columns:minmax(0,1fr);grid-template-areas:"placa" "status"}
html.figura header,html.figura .partes,html.figura #trilha,html.figura #onb,html.figura #missionCard,
html.figura #legend,html.figura #tools,html.figura #palette,html.figura .actions,html.figura #confirm,
html.figura #done,html.figura #checklist,html.figura #liveNote,html.figura main>section.card:last-of-type{display:none !important}
html.figura #wrap{grid-area:placa;justify-self:center;margin:0}
html.figura #status{grid-area:status;min-height:2.2em;margin:0;font-size:1.15rem;text-align:center}
html.figura #tableCard{grid-area:tabela;margin:0;padding:.6rem 1rem;max-width:24rem;min-width:0;overflow:hidden;align-self:center;font-size:1.2rem}
html.figura #tableCard .readout{flex-wrap:wrap}
html.figura #tableCard table{font-size:1.15rem}
html.figura #tableCard h2{font-size:1.1rem}
html.figura.sem-tabela #tableCard{display:none !important}
"""

FIGURA_JS = r"""
/* ===== modo figura: ?figura=<id>[&liga=A,B|128,64][&tema=claro|escuro][&tabela=0] =====
   Carrega o circuito pronto da missão (o mesmo do botão "Ver exemplo") ou um dos extras só de
   chaves (oficina/figuras/extras.json, conferidos pela tabela-verdade da missão-base), esconde a
   interface de missão e deixa a Mão: no seminário a bancada entra como figura que se toca, sem
   construir. A placa cabe na ALTURA da janela (iframe), não só na largura. Nada é gravado no
   navegador neste modo. Sem o parâmetro, a página é a de sempre. */
(function(){
  const q=new URLSearchParams(location.search); const fid=q.get("figura"); if(!fid) return;
  const EXTRAS={"sw-and":{"base":"g-and","cells":[{"t":"src","x":1,"y":3},{"t":"wire","x":2,"y":3},{"t":"sw","x":3,"y":3,"lbl":"A","r":0},{"t":"wire","x":4,"y":3},{"t":"sw","x":5,"y":3,"lbl":"B","r":0},{"t":"wire","x":6,"y":3},{"t":"lamp","x":7,"y":3,"lbl":"S"}]},"sw-or":{"base":"g-or","cells":[{"t":"src","x":1,"y":3},{"t":"wire","x":2,"y":3},{"t":"wire","x":2,"y":2},{"t":"wire","x":2,"y":4},{"t":"sw","x":3,"y":2,"lbl":"A","r":0},{"t":"sw","x":3,"y":4,"lbl":"B","r":0},{"t":"wire","x":4,"y":2},{"t":"wire","x":4,"y":4},{"t":"wire","x":4,"y":3},{"t":"wire","x":5,"y":3},{"t":"lamp","x":6,"y":3,"lbl":"S"}]}};
  const base=EXTRAS[fid]?EXTRAS[fid].base:fid; const ex=EXTRAS[fid]?EXTRAS[fid].cells:EXAMPLES[fid];
  const i=missions.findIndex(m=>m.id===base);
  if(i<0||!ex){ document.getElementById("status").textContent="Figura desconhecida: "+fid; return; }
  const tema=q.get("tema"); if(tema==="claro"||tema==="escuro") document.documentElement.dataset.theme=(tema==="claro"?"light":"dark");
  document.documentElement.classList.add("figura"); if(q.get("tabela")==="0") document.documentElement.classList.add("sem-tabela");
  save=function(){}; saveDone=function(){};
  mission=missions[i];
  let minX=1e9,maxX=-1,minY=1e9,maxY=-1; for(const it of ex){ minX=Math.min(minX,it.x); maxX=Math.max(maxX,it.x); minY=Math.min(minY,it.y); maxY=Math.max(maxY,it.y); }
  const bw=maxX-minX+1, bh=maxY-minY+1;
  // a grade se recorta ao circuito (com uma célula de ar), para a figura encher a janela; a máquina de binário mantém a grade da missão por causa do mostrador
  sim=mission.binary?new Sim(mission.cols,mission.rows):new Sim(Math.max(bw+2,6),Math.max(bh+2,4));
  let regionH=sim.H;
  if(mission.binary){ const lines=mission.numMode==="float"?3:(mission.outputs.length>8?3:2); regionH=mission.monitorY-(lines===3?2.7:2.1)/2; }
  const ox=Math.floor((sim.W-bw)/2)-minX, oy=Math.max(0,Math.round((regionH-bh)/2))-minY;
  for(const it of ex){ const x=it.x+ox, y=it.y+oy; if(x>=0&&y>=0&&x<sim.W&&y<sim.H) sim.cells[y][x]={t:it.t,r:it.r||0,on:false,lbl:it.lbl||""}; }
  for(const tok of (q.get("liga")||"").split(",").filter(Boolean)){
    const sws=sim.find("sw",tok);
    if(sws.length){ for(const [x,y] of sws) sim.cells[y][x].on=true; continue; }
    for(const [x,y] of sim.find("lamp",tok)){ const c=sim.cell(x,y+1); if(c&&c.t==="sw") c.on=true; }
  }
  tool={k:"hand",lbl:""}; picked=null; undoStack=[]; selected=null;
  resize=function(){
    const main=document.querySelector("main"), wrap=document.getElementById("wrap"), tab=document.getElementById("tableCard");
    const semTabela=document.documentElement.classList.contains("sem-tabela");
    const tw=semTabela?0:tab.getBoundingClientRect().width+16;   // a largura REAL do cartão, nunca um palpite
    const availW=main.clientWidth-tw-12, availH=window.innerHeight-document.getElementById("status").getBoundingClientRect().height-30;
    S=Math.max(10,Math.floor(Math.min(availW/sim.W, availH/sim.H))); const dpr=window.devicePixelRatio||1;
    cv.width=S*sim.W*dpr; cv.height=S*sim.H*dpr; cv.style.width=(S*sim.W)+"px"; cv.style.height=(S*sim.H)+"px"; wrap.style.width=(S*sim.W+2)+"px";
    ctx.setTransform(dpr,0,0,dpr,0,0); draw();
  };
  window.addEventListener("resize",resize);
  readColors(); resize(); tick();
  setStatus("Toque numa chave para ligar ou desligar; toque numa peça para ler o que ela está fazendo.");
})();
"""

# (marca na fonte, quantas vezes ela tem de aparecer, o que entra no lugar)
TROCAS = [
    # as fontes da casa no lugar da fonte da bancada
    ('<link rel="preconnect" href="https://fonts.googleapis.com">\n', 1, ""),
    ('<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">', 1, FONTES),
    ('"IBM Plex Sans"', 7, '"Inter"'),
    # a tinta escura fixa do desenho passa a ser o azul-noite da casa
    ("#1B1F24", 7, "#0a1424"),
    # o cabeçalho no molde das outras páginas
    ("  <h1>Bancada de circuitos</h1>\n",
     1, '  <div><p class="eyebrow">hello-world-machine · bancada</p><h1>Bancada de circuitos</h1></div>\n'),
    # os rótulos das peças são desenhados antes de a fonte chegar: redesenha quando ela chega
    ('addEventListener("change",()=>{' + REDESENHAR + "}); }\n",
     1, 'addEventListener("change",()=>{' + REDESENHAR + "}); }\n"
        "if(document.fonts&&document.fonts.ready){ document.fonts.ready.then(()=>{" + REDESENHAR + "}); }\n"),
]


def main():
    fonte = open(os.path.join(AQUI, "bancada", "bancada.html"), encoding="utf-8").read()
    pele = open(os.path.join(AQUI, "bancada", "pele-itaca.css"), encoding="utf-8").read()
    pagina = fonte
    for marca, vezes, novo in TROCAS + [("</style>", 1, None), ("<main>\n", 1, None), ("})();\n</script>", 1, None)]:
        if fonte.count(marca) != vezes:
            sys.stderr.write(f"ABORTADO: esperava {vezes} ocorrência(s) de {marca[:60]!r} na bancada, achei {fonte.count(marca)}\n")
            return 1
        if novo is not None:
            pagina = pagina.replace(marca, novo)
    pagina = pagina.replace("</style>", pele + BARRA.CSS + FIGURA_CSS + "</style>")
    pagina = pagina.replace("})();\n</script>", FIGURA_JS + "})();\n</script>")  # dentro do IIFE da bancada
    pagina = pagina.replace("<main>\n", "<main>\n" + BARRA.barra("bancada") + "\n")
    saida = os.path.join(AQUI, "pt", "bancada.html")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print(f"pt/bancada.html: {len(pagina)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
