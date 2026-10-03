/* A placa em planta: desenha a máquina e toca o traço, um ciclo por vez.
 *
 * Especificação: pesquisa/a-placa-em-planta.md. Dois trilhos (endereços em
 * cima, dados embaixo), os módulos entre eles, hastes para os trilhos. Em cada
 * ciclo acendem no máximo quatro coisas: a haste de origem do dado, o trilho de
 * dados com os oito bits, a haste de destino, e o trilho de endereços com o
 * valor. Nada se desloca: o padrão aparece e copia-se.
 *
 * As cores vêm dos tokens da página (claro e escuro). Sem biblioteca.
 * No node, expõe só o mapeamento e o leiaute, para a conferência.
 */
(function (raiz) {
  "use strict";

  // --- o leiaute, num espaço lógico de 1000 × 600 --------------------------
  var LARG = 1000, ALT = 600;
  var TRILHO_END = 56, TRILHO_DADO = 520, TRILHO_X0 = 30, TRILHO_X1 = 760;
  var MODULOS = {
    pc:  { x: 30,  y: 110, w: 140, h: 64,  nome: "PC", sub: "contador de programa", mat: "qual gaveta é ordem", end: true, dado: false },
    inc: { x: 30,  y: 200, w: 140, h: 64,  nome: "+1 · −1", sub: "incrementador-decrementador", mat: "", end: true, dado: false },
    il:  { x: 30,  y: 290, w: 140, h: 150, nome: "instrução", sub: "IL1 · IL2 · IL3", mat: "a ordem, byte a byte", end: true, dado: true },
    reg: { x: 210, y: 110, w: 180, h: 330, nome: "registradores", sub: "A B C D E H L", mat: "guardar · mem(HL) aponta", end: true, dado: true },
    ula: { x: 430, y: 110, w: 140, h: 330, nome: "ULA", sub: "soma, subtrai, compara", mat: "(A + B) mod 256", end: false, dado: true },
    ram: { x: 610, y: 110, w: 150, h: 330, nome: "RAM", sub: "64 K gavetas", mat: "mem(endereço) = byte", end: true, dado: true },
    tela:{ x: 790, y: 60,  w: 190, h: 480, nome: "tela", sub: "lê 8000h … 8107h", mat: "cor(x, y)", end: false, dado: false }
  };
  var CEL = 14, TELA_X = 801, TELA_Y = 112;

  // --- de cada nome do traço ao módulo desenhado --------------------------
  function moduloDe(nome) {
    if (nome === "" || nome == null) return null;
    if (nome === "RAM" || nome === "teclado") return "ram";
    if (nome === "PC") return "pc";
    if (nome === "HL" || /^[ABCDEHL]$/.test(nome)) return "reg";
    if (/^IL[123]$/.test(nome) || nome === "IL2+IL3") return "il";
    if (nome === "ULA" || nome === "ULA.B" || nome === "flags") return "ula";
    throw new Error("nome sem módulo desenhado: " + nome);
  }

  function mapear(t) {
    var m = { dadoDe: moduloDe(t.dado_de), dadoPara: moduloDe(t.dado_para), endDe: moduloDe(t.endereco_de), endPara: null };
    if (t.endereco !== null && t.endereco !== undefined) {
      if (/^(INX|DCX)/.test(t.nota)) m.endPara = "inc";
      else if (/^(salto tomado|PCHL)/.test(t.nota)) m.endPara = "pc";
      else m.endPara = "ram";
    }
    return m;
  }

  var PLACA = { MODULOS: MODULOS, moduloDe: moduloDe, mapear: mapear };

  if (typeof module !== "undefined" && module.exports) { module.exports = PLACA; return; }
  raiz.HWM_PLACA = PLACA;
  if (typeof document === "undefined") return;

  // --- o tocador --------------------------------------------------------------
  var HWM = raiz.HWM, MONTAR = raiz.HWM_MONTAR;
  var canvas = document.getElementById("placa"), ctx = canvas.getContext("2d");
  var asm = document.getElementById("asm").textContent;
  var montado = MONTAR.montar(asm);
  var imagem = MONTAR.binario(montado.saida);
  var maquina = new HWM.Maquina(imagem, true);
  maquina.rodar(100000);
  var traco = maquina.traco, N = traco.length;
  var porEndereco = {};
  montado.listagem.forEach(function (l, i) { porEndereco[l[0]] = i; });

  var k = 0, p = 1, tocando = false, marcha = 1, ultimoT = 0, soTela = false;
  var MARCHAS = { 1: 1000, 4: 250, 20: 50 };

  function hex(n, c) { return HWM.hex(n, c); }
  function tok(nome) { return getComputedStyle(document.documentElement).getPropertyValue(nome).trim(); }
  function cores() {
    return { bg: tok("--bg"), card: tok("--card"), linha: tok("--linha"), ink: tok("--ink"), ink2: tok("--ink2"),
      muted: tok("--muted"), bronze: tok("--bronze"), azul: tok("--azul"), verde: tok("--verde"),
      bit1: tok("--bit1"), bit0: tok("--bit0"), bit0ink: tok("--bit0-ink") };
  }
  function suave(x) { return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }

  // o estado "depois do ciclo k": registradores do traço; IL e tela reconstruídos
  function estadoAte(k) {
    var il = [0, 0, 0], video = new Uint8Array(HWM.VIDEO_FIM - HWM.VIDEO_INICIO), ram = {}, i, t;
    for (i = 0; i < imagem.length; i++) ram[i] = imagem[i];
    for (i = 0; i <= k && i < N; i++) {
      t = traco[i];
      if (t.dado_para === "IL1") il[0] = t.dado; else if (t.dado_para === "IL2") il[1] = t.dado; else if (t.dado_para === "IL3") il[2] = t.dado;
      if (t.dado_para === "RAM") {
        ram[t.endereco] = t.dado;
        if (t.endereco >= HWM.VIDEO_INICIO && t.endereco < HWM.VIDEO_FIM) video[t.endereco - HWM.VIDEO_INICIO] = t.dado;
      }
    }
    return { il: il, video: video, ram: ram, t: traco[Math.min(k, N - 1)] };
  }

  function linhaDaInstrucao(k) {
    var i, t;
    for (i = k; i >= 0; i--) { t = traco[i]; if (t.dado_para === "IL1") return porEndereco[t.endereco]; }
    return 0;
  }

  // --- desenho ------------------------------------------------------------------
  function caixa(c, m, ativo, C) {
    ctx.fillStyle = C.card; ctx.strokeStyle = ativo ? C.bronze : C.linha; ctx.lineWidth = ativo ? 2.5 : 1;
    ctx.fillRect(m.x, m.y, m.w, m.h); ctx.strokeRect(m.x, m.y, m.w, m.h);
    ctx.fillStyle = C.ink; ctx.font = "600 13px Inter, system-ui, sans-serif"; ctx.textAlign = "left";
    ctx.fillText(m.nome, m.x + 10, m.y + 18);
    ctx.fillStyle = C.muted; ctx.font = "11px Inter, system-ui, sans-serif";
    ctx.fillText(m.sub, m.x + 10, m.y + 33);
    if (m.mat) { ctx.fillStyle = C.bronze; ctx.font = "italic 11px 'Cormorant Garamond', Georgia, serif"; ctx.fillText(m.mat, m.x + 10, m.y + m.h - 8); }
  }
  function haste(m, trilhoY, cor, lit) {
    var x = m.x + m.w / 2, y0 = trilhoY < m.y ? m.y : m.y + m.h;
    ctx.strokeStyle = cor; ctx.lineWidth = lit ? 3 : 1;
    ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x, trilhoY); ctx.stroke();
    if (lit) { ctx.fillStyle = cor; ctx.beginPath(); ctx.arc(x, trilhoY, 4, 0, 6.283); ctx.fill(); }
  }
  function celulaTxt(x, y, w, h, rot, val, lit, C) {
    ctx.fillStyle = lit ? C.bronze : C.linha; ctx.fillRect(x, y, w, h);
    ctx.fillStyle = lit ? C.card : C.ink; ctx.font = "12px 'Spline Sans Mono', ui-monospace, monospace"; ctx.textAlign = "left";
    ctx.fillText(rot, x + 6, y + h - 6);
    ctx.textAlign = "right"; ctx.fillText(val, x + w - 6, y + h - 6); ctx.textAlign = "left";
  }

  function desenhar() {
    var C = cores(), est = estadoAte(k), t = est.t, m = mapear(t), q = tocando ? suave(p) : 1;
    var fOrig = q < 0.35 || q === 1, fTrilho = q >= 0.35 || q === 1, fDest = q >= 0.7 || q === 1;
    var escala = canvas.width / LARG;
    ctx.setTransform(escala, 0, 0, escala, 0, 0);
    ctx.fillStyle = C.bg; ctx.fillRect(0, 0, LARG, ALT);

    // trilhos
    var temEnd = t.endereco !== null && t.endereco !== undefined, temDado = t.dado !== null && t.dado !== undefined;
    ctx.lineWidth = 6; ctx.strokeStyle = (temEnd && fTrilho) ? C.azul : C.linha;
    ctx.beginPath(); ctx.moveTo(TRILHO_X0, TRILHO_END); ctx.lineTo(TRILHO_X1, TRILHO_END); ctx.stroke();
    ctx.strokeStyle = (temDado && fTrilho) ? C.bronze : C.linha;
    ctx.beginPath(); ctx.moveTo(TRILHO_X0, TRILHO_DADO); ctx.lineTo(TRILHO_X1, TRILHO_DADO); ctx.stroke();
    ctx.fillStyle = C.muted; ctx.font = "600 10px Inter, system-ui, sans-serif"; ctx.textAlign = "left";
    ctx.fillText("BARRAMENTO DE ENDEREÇOS · 16 fios", TRILHO_X0, TRILHO_END - 12);
    ctx.fillText("BARRAMENTO DE DADOS · 8 fios", TRILHO_X0, TRILHO_DADO + 24);
    if (temEnd && fTrilho) {
      ctx.fillStyle = C.azul; ctx.font = "600 16px 'Spline Sans Mono', ui-monospace, monospace"; ctx.textAlign = "center";
      ctx.fillText(hex(t.endereco, 4) + "h", (TRILHO_X0 + TRILHO_X1) / 2, TRILHO_END - 12);
    }
    if (temDado && fTrilho) {
      var bits = t.dado.toString(2).padStart(8, "0"), i, bx = (TRILHO_X0 + TRILHO_X1) / 2 - 8 * 22 / 2;
      for (i = 0; i < 8; i++) {
        ctx.fillStyle = bits[i] === "1" ? C.bit1 : C.bit0;
        ctx.beginPath(); ctx.arc(bx + i * 22 + 11, TRILHO_DADO, 7, 0, 6.283); ctx.fill();
        ctx.fillStyle = bits[i] === "1" ? C.card : C.bit0ink; ctx.font = "600 9px 'Spline Sans Mono', monospace"; ctx.textAlign = "center";
        ctx.fillText(bits[i], bx + i * 22 + 11, TRILHO_DADO + 3);
      }
      ctx.fillStyle = C.bronze; ctx.font = "600 16px 'Spline Sans Mono', ui-monospace, monospace"; ctx.textAlign = "center";
      ctx.fillText(hex(t.dado, 2) + "h = " + t.dado, (TRILHO_X0 + TRILHO_X1) / 2, TRILHO_DADO - 14);
    }

    // hastes
    Object.keys(MODULOS).forEach(function (id) {
      var mod = MODULOS[id];
      if (mod.end) {
        var litE = temEnd && ((id === m.endDe && fOrig) || (id === m.endPara && fDest));
        haste(mod, TRILHO_END, litE ? C.azul : C.linha, litE);
      }
      if (mod.dado) {
        var litD = temDado && ((id === m.dadoDe && fOrig) || (id === m.dadoPara && fDest));
        haste(mod, TRILHO_DADO, litD ? C.bronze : C.linha, litD);
      }
    });

    // módulos
    var ativo = {};
    if (fOrig) { ativo[m.dadoDe] = true; ativo[m.endDe] = true; }
    if (fDest) { ativo[m.dadoPara] = true; if (temEnd) ativo[m.endPara] = true; }
    Object.keys(MODULOS).forEach(function (id) { caixa(ctx, MODULOS[id], !!ativo[id], C); });

    // PC, incrementador
    celulaTxt(40, 150, 120, 18, "PC", hex(t.pc, 4), temEnd && t.endereco_de === "PC" && fOrig, C);
    celulaTxt(40, 240, 120, 18, "", m.endPara === "inc" && fDest ? "→ " + hex(t.hl, 4) : "", m.endPara === "inc" && fDest, C);
    // IL
    [0, 1, 2].forEach(function (i) {
      var lit = fDest && t.dado_para === "IL" + (i + 1) || fOrig && (t.dado_de === "IL" + (i + 1) || (t.endereco_de === "IL2+IL3" && i > 0));
      celulaTxt(40, 345 + i * 26, 120, 20, "IL" + (i + 1), hex(est.il[i], 2), !!lit, C);
    });
    // registradores
    var regs = { A: t.a, B: t.b, C: t.c, D: t.d, E: t.e, H: t.hl >> 8, L: t.hl & 0xFF };
    ["A", "B", "C", "D", "E", "H", "L"].forEach(function (r, i) {
      var lit = (fDest && t.dado_para === r) || (fOrig && t.dado_de === r) || (fOrig && t.endereco_de === "HL" && (r === "H" || r === "L"));
      celulaTxt(220, 150 + i * 30, 160, 22, r + (r === "A" ? " · acumulador" : ""), hex(regs[r], 2), !!lit, C);
    });
    // ULA
    celulaTxt(440, 150, 120, 22, "entrada A", hex(t.a, 2), false, C);
    celulaTxt(440, 180, 120, 22, "entrada B", t.dado_para === "ULA.B" ? hex(t.dado, 2) : "", fDest && t.dado_para === "ULA.B", C);
    celulaTxt(440, 210, 120, 22, "saída", t.dado_de === "ULA" ? hex(t.dado, 2) : "", fOrig && t.dado_de === "ULA", C);
    celulaTxt(440, 240, 120, 22, "flags C Z S", t.flags, fDest && t.dado_para === "flags", C);
    // RAM: janela de 8 gavetas
    var base = temEnd ? Math.max(0, t.endereco - 3) : 0, j, e;
    for (j = 0; j < 8; j++) {
      e = base + j;
      var val = est.ram[e] !== undefined ? est.ram[e] : 0;
      celulaTxt(620, 150 + j * 26, 130, 20, hex(e, 4), hex(val, 2), temEnd && e === t.endereco && m.endPara === "ram" && fDest, C);
    }
    // tela
    var r, c, b;
    for (r = 0; r < HWM.VIDEO_LINHAS; r++) for (c = 0; c < HWM.VIDEO_COLUNAS; c++) {
      b = est.video[r * HWM.VIDEO_COLUNAS + c];
      ctx.fillStyle = b ? C.card : C.bg; ctx.fillRect(TELA_X + c * CEL, TELA_Y + r * CEL, CEL - 1, CEL - 1);
      if (b) {
        ctx.fillStyle = (b >= 1 && b <= 8) ? C.bronze : C.ink; ctx.font = "11px 'Spline Sans Mono', ui-monospace, monospace"; ctx.textAlign = "center";
        ctx.fillText(HWM.celula(b), TELA_X + c * CEL + CEL / 2, TELA_Y + r * CEL + 11);
      }
    }
    var escrita = fDest && t.dado_para === "RAM" && t.endereco >= HWM.VIDEO_INICIO && t.endereco < HWM.VIDEO_FIM;
    if (escrita) {
      var off = t.endereco - HWM.VIDEO_INICIO;
      ctx.strokeStyle = C.bronze; ctx.lineWidth = 2;
      ctx.strokeRect(TELA_X + (off % HWM.VIDEO_COLUNAS) * CEL - 1, TELA_Y + Math.floor(off / HWM.VIDEO_COLUNAS) * CEL - 1, CEL + 1, CEL + 1);
    }
    ctx.setLineDash([3, 4]); ctx.strokeStyle = C.linha; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(760, 275); ctx.lineTo(790, 275); ctx.stroke(); ctx.setLineDash([]);

    // painel de texto
    var inst = montado.listagem[linhaDaInstrucao(k)];
    document.getElementById("pos").textContent = "ciclo " + (k + 1) + " de " + N + " · instrução " + t.instrucao + " · " + t.fase;
    document.getElementById("nota").textContent = (inst ? inst[2] + " — " : "") + (t.nota || (t.fase === "busca" ? "busca: PC no barramento de endereços, RAM no de dados, byte salvo em " + t.dado_para : ""));
    var lis = document.getElementById("listagem").children, li;
    for (li = 0; li < lis.length; li++) lis[li].classList.toggle("atual", li === linhaDaInstrucao(k));
    document.getElementById("barra").value = k;
  }

  // --- controle -----------------------------------------------------------------
  function ir(novo) { k = Math.max(0, Math.min(N - 1, novo)); p = 1; desenhar(); }
  function proximoVisivel(dir) {
    var i = k + dir;
    while (soTela && i >= 0 && i < N && !(traco[i].dado_para === "RAM" && traco[i].endereco >= HWM.VIDEO_INICIO)) i += dir;
    return i;
  }
  function quadro(ts) {
    if (!tocando) return;
    var dur = MARCHAS[marcha];
    if (!ultimoT) ultimoT = ts;
    p += (ts - ultimoT) / dur; ultimoT = ts;
    if (p >= 1) {
      var i = proximoVisivel(1);
      if (i >= N) { tocando = false; p = 1; k = N - 1; document.getElementById("tocar").textContent = "tocar"; desenhar(); return; }
      k = i; p = 0;
    }
    desenhar();
    requestAnimationFrame(quadro);
  }
  function tocar() {
    tocando = !tocando; ultimoT = 0;
    document.getElementById("tocar").textContent = tocando ? "pausar" : "tocar";
    if (tocando) { if (k >= N - 1) { k = 0; } p = 0; requestAnimationFrame(quadro); } else { p = 1; desenhar(); }
  }
  function redimensionar() {
    // no telefone a placa não encolhe: fica legível e o quadro rola de lado
    var w = Math.max(820, canvas.parentNode.clientWidth - 2), dpr = window.devicePixelRatio || 1;
    canvas.style.width = w + "px"; canvas.style.height = Math.round(w * ALT / LARG) + "px";
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(w * ALT / LARG * dpr);
    desenhar();   // a escala lógica (canvas.width / LARG) já inclui o dpr
  }

  // listagem
  var ul = document.getElementById("listagem");
  montado.listagem.forEach(function (l) {
    var li = document.createElement("li");
    li.innerHTML = '<span class="end">' + hex(l[0], 4) + '</span><span class="bytes">' +
      l[1].map(function (b) { return hex(b, 2); }).join(" ") + '</span><span class="txt"></span>';
    li.querySelector(".txt").textContent = l[2];
    ul.appendChild(li);
  });
  document.getElementById("ant").addEventListener("click", function () { tocando = false; ir(proximoVisivel(-1)); });
  document.getElementById("prox").addEventListener("click", function () { tocando = false; ir(proximoVisivel(1)); });
  document.getElementById("tocar").addEventListener("click", tocar);
  document.getElementById("barra").max = N - 1;
  document.getElementById("barra").addEventListener("input", function (e) { tocando = false; document.getElementById("tocar").textContent = "tocar"; ir(+e.target.value); });
  document.getElementById("marcha").addEventListener("change", function (e) { marcha = +e.target.value; });
  document.getElementById("sotela").addEventListener("change", function (e) { soTela = e.target.checked; });
  document.addEventListener("keydown", function (e) {
    if (e.target && /^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName) && e.target.type !== "range") return;
    if (e.key === "ArrowRight") { tocando = false; ir(proximoVisivel(1)); }
    if (e.key === "ArrowLeft") { tocando = false; ir(proximoVisivel(-1)); }
    if (e.key === " ") { e.preventDefault(); tocar(); }
  });
  window.addEventListener("resize", redimensionar);
  if (window.matchMedia) { window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () { desenhar(); }); }
  redimensionar();
  var ultimoCiclo = traco[N - 1];
  document.getElementById("resumo").textContent = maquina.instrucoes + " instruções, " + N + " ciclos, " +
    (maquina.parada ? "a máquina parou em HLT" : "a máquina não parou") + " · a tela diz “" + maquina.tela()[0].replace(/·+$/, "") + "”";
})(typeof window !== "undefined" ? window : this);
