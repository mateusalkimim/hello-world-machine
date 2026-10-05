/* Os instrumentos da escada — canvas e aritmética, nada mais.
 *
 * Contrato herdado do seeing-calculus: sem biblioteca de terceiro, sem rede,
 * sem servidor. Abre offline. Nada sai da sua máquina porque não há para onde.
 *
 * A diferença de propósito, e é a tese desta reforma: no seeing-calculus o
 * instrumento deixa uma afirmação ser CONFERIDA com a régua. Aqui ele faz o
 * mesmo com uma ARESTA do mapa. Quando a escada diz "porta lógica ← dois relés
 * em série", o instrumento liga dois relés em série e monta a tabela-verdade na
 * sua frente. A citação do Petzold continua lá, como segunda testemunha — mas
 * ela deixou de ser a única coisa que sustenta a seta.
 */
(function () {
  "use strict";

  var COR = {
    fio:  "#33465f",   // fio sem corrente
    vivo: "#6fbf6a",   // corrente passando
    ferro:"#c1704f",   // o que é físico
    frio: "#5b8fc9",   // lógica combinacional
    seq:  "#4fb3a5",   // lógica sequencial
    ouro: "#c9a266",
    txt:  "#9fadc0",
    fraco:"#5b6b86",
    creme:"#e8e2d6"
  };

  // roundRect é recente. O contrato deste repositório é abrir OFFLINE em
  // navegador qualquer, então a peça entra com remendo em vez de depender da
  // versão de quem abriu.
  if (typeof CanvasRenderingContext2D !== "undefined" &&
      !CanvasRenderingContext2D.prototype.roundRect) {
    CanvasRenderingContext2D.prototype.roundRect = function (x, y, w, h, r) {
      r = Math.min(r || 0, w / 2, h / 2);
      this.moveTo(x + r, y);
      this.arcTo(x + w, y, x + w, y + h, r);
      this.arcTo(x + w, y + h, x, y + h, r);
      this.arcTo(x, y + h, x, y, r);
      this.arcTo(x, y, x + w, y, r);
      this.closePath();
      return this;
    };
  }

  function ctx2d(cv) {
    var r = window.devicePixelRatio || 1, c = cv.getContext("2d");
    var w = cv.clientWidth, h = parseInt(cv.dataset.h || "230", 10);
    cv.width = w * r; cv.height = h * r; cv.style.height = h + "px";
    c.setTransform(r, 0, 0, r, 0, 0);
    c.clearRect(0, 0, w, h);
    c.__w = w; c.__h = h;
    return c;
  }
  function txt(c, s, x, y, cor, tam, al) {
    c.fillStyle = cor || COR.txt;
    c.font = (tam || 12) + "px Inter, system-ui, sans-serif";
    c.textAlign = al || "left"; c.textBaseline = "middle";
    c.fillText(s, x, y);
  }
  function fio(c, pts, ligado, larg) {
    c.strokeStyle = ligado ? COR.vivo : COR.fio;
    c.lineWidth = larg || 2.4; c.lineCap = "round"; c.lineJoin = "round";
    c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    for (var i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
    c.stroke();
  }
  function bolha(c, x, y, ligado, r) {
    c.beginPath(); c.arc(x, y, r || 5, 0, 6.284);
    c.fillStyle = ligado ? COR.vivo : "#1e3050"; c.fill();
    c.strokeStyle = ligado ? COR.vivo : COR.fio; c.lineWidth = 1.4; c.stroke();
  }

  /* ------------------------------------------------------------------ *
   * [1] DOIS RELÉS VIRAM UMA PORTA
   * Prova a aresta  relé → porta lógica.
   * A tabela-verdade não vem pronta: ela se preenche conforme você visita
   * as combinações. Enquanto faltar linha, o instrumento diz que falta.
   * ------------------------------------------------------------------ */
  function releViraPorta(raiz) {
    var cv = raiz.querySelector("canvas");
    var st = { a: false, b: false, serie: true, vistos: {} };

    function chave() { return (st.serie ? "S" : "P") + (st.a ? 1 : 0) + (st.b ? 1 : 0); }
    function saida() { return st.serie ? (st.a && st.b) : (st.a || st.b); }

    function desenhar() {
      st.vistos[chave()] = true;
      var c = ctx2d(cv), w = c.__w, y = 96, on = saida();
      var xA = w * 0.20, xB = w * 0.44, xL = w * 0.76;

      // trilho de alimentação e retorno
      if (st.serie) {
        fio(c, [[40, y], [xA - 26, y]], true);
        fio(c, [[xA + 26, y], [xB - 26, y]], st.a);
        fio(c, [[xB + 26, y], [xL - 30, y]], st.a && st.b);
      } else {
        fio(c, [[40, y], [40, y - 34], [xA - 26, y - 34]], true);
        fio(c, [[40, y], [40, y + 34], [xB - 26, y + 34]], true);
        fio(c, [[xA + 26, y - 34], [xL - 60, y - 34], [xL - 60, y]], st.a);
        fio(c, [[xB + 26, y + 34], [xL - 60, y + 34], [xL - 60, y]], st.b);
        fio(c, [[xL - 60, y], [xL - 30, y]], on);
      }
      relé(c, xA, st.serie ? y : y - 34, st.a, "A");
      relé(c, xB, st.serie ? y : y + 34, st.b, "B");

      // lâmpada
      c.beginPath(); c.arc(xL, y, 15, 0, 6.284);
      c.fillStyle = on ? "rgba(201,162,102,.92)" : "#132440";
      c.fill(); c.strokeStyle = on ? COR.ouro : COR.fio; c.lineWidth = 1.8; c.stroke();
      if (on) { c.beginPath(); c.arc(xL, y, 26, 0, 6.284);
                c.strokeStyle = "rgba(201,162,102,.30)"; c.lineWidth = 6; c.stroke(); }
      txt(c, st.serie ? "em série" : "em paralelo", 40, 30, COR.creme, 13);
      txt(c, st.serie ? "só acende se os dois estiverem acionados"
                      : "acende se qualquer um estiver acionado",
          40, 50, COR.fraco, 11.5);
      tabela(c, w);
    }

    function relé(c, x, y, ligado, rot) {
      c.fillStyle = "#132440"; c.strokeStyle = ligado ? COR.ferro : COR.fio;
      c.lineWidth = 1.6;
      c.beginPath(); c.roundRect(x - 25, y - 24, 50, 48, 5); c.fill(); c.stroke();
      // bobina
      for (var i = 0; i < 4; i++) {
        c.beginPath(); c.arc(x - 12 + i * 8, y + 12, 4, Math.PI, 0);
        c.strokeStyle = ligado ? COR.ferro : COR.fio; c.lineWidth = 1.5; c.stroke();
      }
      // contato: fecha quando acionado
      fio(c, [[x - 18, y - 8], [x - 4, y - 8]], ligado, 2);
      fio(c, [[x + 4, y - 8], [x + 18, y - 8]], ligado, 2);
      c.strokeStyle = ligado ? COR.vivo : COR.fio; c.lineWidth = 2.2;
      c.beginPath(); c.moveTo(x - 4, y - 8);
      c.lineTo(x + 5, ligado ? y - 8 : y - 17); c.stroke();
      txt(c, rot, x, y - 36, ligado ? COR.creme : COR.fraco, 12, "center");
    }

    function tabela(c, w) {
      var pre = st.serie ? "S" : "P", x0 = w - 168, y0 = 152, faltam = 0;
      txt(c, "A   B   saída", x0, y0, COR.fraco, 11.5);
      [[0,0],[0,1],[1,0],[1,1]].forEach(function (l, i) {
        var k = pre + l[0] + l[1], visto = !!st.vistos[k];
        var v = st.serie ? (l[0] && l[1]) : (l[0] || l[1]);
        if (!visto) faltam++;
        var y = y0 + 18 + i * 15;
        var atual = (l[0] === (st.a?1:0) && l[1] === (st.b?1:0));
        if (atual) { c.fillStyle = "rgba(111,191,106,.12)";
                     c.fillRect(x0 - 6, y - 7, 150, 14); }
        txt(c, l[0] + "   " + l[1] + "   " + (visto ? v : "—"), x0, y,
            visto ? (atual ? COR.creme : COR.txt) : "#3b4a60", 11.5);
      });
      var nome = st.serie ? "E" : "OU";
      txt(c, faltam ? ("faltam " + faltam + " combinações para fechar a tabela")
                    : ("tabela completa — isto é uma porta " + nome),
          x0 - 6, y0 + 96, faltam ? COR.fraco : COR.vivo, 11.5);
    }

    raiz.querySelectorAll("[data-acao]").forEach(function (b) {
      b.addEventListener("click", function () {
        var a = b.dataset.acao;
        if (a === "inA") st.a = !st.a;
        if (a === "inB") st.b = !st.b;
        if (a === "mode") { st.serie = !st.serie;
          b.textContent = st.serie ? "em série" : "em paralelo"; }
        b.classList.toggle("on", (a === "inA" && st.a) || (a === "inB" && st.b));
        desenhar();
      });
    });
    desenhar();
    window.addEventListener("resize", desenhar);
  }

  /* ------------------------------------------------------------------ *
   * [2] NÍVEL × BORDA — o instrumento que a escada mais precisava
   * Prova a aresta  flip-flop de nível → flip-flop de borda, e mostra
   * POR QUE ela existe: o de nível VAZA enquanto o relógio está alto.
   * Os dois no MESMO relógio, com o mesmo dado, lado a lado.
   * ------------------------------------------------------------------ */
  function nivelXBorda(raiz) {
    var cv = raiz.querySelector("canvas");
    var st = { t: 0, tocando: false, dado: [], periodo: 96, ultimo: 0 };
    // o dado muda algumas vezes DENTRO da janela em que o relógio está alto —
    // é exatamente aí que os dois circuitos discordam
    var MUDANCAS = [0,0,1,1,1,0,0,1,0,1,1,0,0,0,1,1,0,1,0,0,1,1,1,0];

    function dadoEm(t) { return MUDANCAS[Math.floor(t / 26) % MUDANCAS.length]; }
    function relogioEm(t) { return (t % st.periodo) < st.periodo / 2 ? 1 : 0; }

    function simular(ate) {
      var qn = 0, qb = 0, ant = 0, serie = [];
      for (var t = 0; t <= ate; t++) {
        var ck = relogioEm(t), d = dadoEm(t);
        if (ck === 1) qn = d;                    // NÍVEL: transparente o tempo todo
        if (ck === 1 && ant === 0) qb = d;       // BORDA: só no instante da subida
        ant = ck;
        serie.push([ck, d, qn, qb]);
      }
      return serie;
    }

    function desenhar() {
      var c = ctx2d(cv), w = c.__w, jan = 560;
      var t0 = Math.max(0, st.t - jan), s = simular(st.t);
      var esq = 66, larg = w - esq - 16;
      function X(t) { return esq + (t - t0) / jan * larg; }

      var linhas = [
        ["relógio", 0, COR.ouro],
        ["dado",    1, COR.frio],
        ["nível",   2, "#c1704f"],
        ["borda",   3, COR.seq]
      ];
      linhas.forEach(function (L, i) {
        var yb = 40 + i * 44, alt = 22;
        txt(c, L[0], esq - 10, yb - alt / 2, L[2], 12, "right");
        // faixa em que o relógio está ALTO — a janela do vazamento
        if (i === 2) {
          for (var t = t0; t <= st.t; t++) {
            if (s[t] && s[t][0] === 1) {
              c.fillStyle = "rgba(193,112,79,.10)";
              c.fillRect(X(t), yb - alt - 3, Math.max(1, larg / jan + 0.6), alt + 6);
            }
          }
        }
        c.strokeStyle = L[2]; c.lineWidth = 1.8; c.beginPath();
        var iniciou = false;
        for (var t = t0; t <= st.t; t++) {
          if (!s[t]) continue;
          var y = yb - (s[t][L[1]] ? alt : 0);
          if (!iniciou) { c.moveTo(X(t), y); iniciou = true; } else { c.lineTo(X(t), y); }
        }
        c.stroke();
      });

      // marcas nas bordas de subida
      for (var t = t0; t <= st.t; t++) {
        if (s[t] && s[t][0] === 1 && s[t-1] && s[t-1][0] === 0) {
          c.strokeStyle = "rgba(201,162,102,.35)"; c.lineWidth = 1;
          c.setLineDash([2, 4]); c.beginPath();
          c.moveTo(X(t), 18); c.lineTo(X(t), 200); c.stroke(); c.setLineDash([]);
        }
      }

      var ag = s[st.t] || [0,0,0,0];
      var discorda = ag[2] !== ag[3];
      txt(c, "o de NÍVEL copia o dado durante TODA a faixa clara. o de BORDA "
           + "copia só na linha pontilhada.", esq, 218, COR.fraco, 11.5);
      txt(c, discorda ? "agora eles discordam: nível = " + ag[2]
                      + ", borda = " + ag[3]
                      : "agora eles concordam — espere o dado mudar com o "
                      + "relógio alto",
          esq, 238, discorda ? COR.ouro : COR.fraco, 12);
    }

    function passo() {
      if (st.tocando) { st.t += 2; desenhar(); }
      requestAnimationFrame(passo);
    }
    raiz.querySelectorAll("[data-acao]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (b.dataset.acao === "playpause") {
          st.tocando = !st.tocando;
          b.textContent = st.tocando ? "pausar" : "continuar";
        }
        if (b.dataset.acao === "restart") { st.t = 0; }
        desenhar();
      });
    });
    desenhar(); requestAnimationFrame(passo);
    window.addEventListener("resize", desenhar);
  }

  /* ------------------------------------------------------------------ *
   * [3] O CIRCUITO QUE LEMBRA
   * Prova a aresta  porta lógica → flip-flop de nível: dois NOR realimentados
   * têm DOIS estados estáveis para a mesma entrada. A mesma entrada, duas
   * saídas — que é a definição de lembrar.
   * ------------------------------------------------------------------ */
  function circuitoQueLembra(raiz) {
    var cv = raiz.querySelector("canvas");
    var st = { r: 0, s: 0, q: 0, hist: [] };

    function passo() {
      // NOR realimentado: Q = NOR(R, Qbarra) ; Qbarra = NOR(S, Q)
      if (st.s && !st.r) st.q = 1;
      else if (st.r && !st.s) st.q = 0;
      // ambos 0: mantém — é aqui que ele lembra
      st.hist.push([st.r, st.s, st.q]);
      if (st.hist.length > 26) st.hist.shift();
    }

    function nor(c, x, y, entradaViva, saidaViva) {
      c.fillStyle = "#132440";
      c.strokeStyle = saidaViva ? COR.seq : COR.fio;
      c.lineWidth = 1.7;
      c.beginPath(); c.roundRect(x - 34, y - 17, 62, 34, 5); c.fill(); c.stroke();
      txt(c, "NOR", x - 3, y, saidaViva ? COR.creme : COR.txt, 11.5, "center");
      // a bolinha da negacao, que e o que faz NOR ser NOR
      c.beginPath(); c.arc(x + 31, y, 3.6, 0, 6.284);
      c.fillStyle = saidaViva ? COR.seq : "#1e3050"; c.fill();
      c.strokeStyle = saidaViva ? COR.seq : COR.fio; c.lineWidth = 1.2; c.stroke();
    }

    function desenhar() {
      var c = ctx2d(cv), w = c.__w, y = 84;
      var xg = w * 0.30, xg2 = w * 0.30, xq = w * 0.60;
      nor(c, xg, y - 30, st.r, st.q === 0);
      nor(c, xg, y + 30, st.s, st.q === 1);
      // realimentação cruzada
      fio(c, [[xg + 34, y - 30], [xg + 52, y - 30], [xg + 52, y + 14],
              [xg - 40, y + 14], [xg - 40, y + 22], [xg - 34, y + 22]], st.q === 0);
      fio(c, [[xg + 34, y + 30], [xg + 62, y + 30], [xg + 62, y - 14],
              [xg - 40, y - 14], [xg - 40, y - 22], [xg - 34, y - 22]], st.q === 1);
      fio(c, [[xg + 34, y - 30], [xq, y - 30]], st.q === 0);
      txt(c, "R", xg - 52, y - 38, st.r ? COR.creme : COR.fraco, 12, "right");
      txt(c, "S", xg - 52, y + 38, st.s ? COR.creme : COR.fraco, 12, "right");
      fio(c, [[xg - 48, y - 38], [xg - 34, y - 38]], st.r);
      fio(c, [[xg - 48, y + 38], [xg - 34, y + 38]], st.s);

      // a lâmpada da saída
      c.beginPath(); c.arc(xq + 26, y - 30, 14, 0, 6.284);
      c.fillStyle = st.q ? "rgba(79,179,165,.9)" : "#132440";
      c.fill(); c.strokeStyle = st.q ? COR.seq : COR.fio; c.lineWidth = 1.7; c.stroke();
      txt(c, "Q = " + st.q, xq + 48, y - 30, COR.creme, 13);

      // a tira do histórico: prova que a MESMA entrada dá saídas diferentes
      var x0 = 40, y0 = 176;
      txt(c, "histórico — R e S soltos (0,0), e mesmo assim Q difere:",
          x0, y0 - 16, COR.fraco, 11.5);
      st.hist.forEach(function (h, i) {
        var x = x0 + i * 17, ambos = (h[0] === 0 && h[1] === 0);
        c.fillStyle = h[2] ? (ambos ? COR.seq : "rgba(79,179,165,.45)")
                           : (ambos ? "#25405c" : "#1a2c45");
        c.fillRect(x, y0, 13, 20);
        if (ambos) { c.strokeStyle = COR.ouro; c.lineWidth = 1;
                     c.strokeRect(x + .5, y0 + .5, 12, 19); }
      });
      txt(c, "contornado em ouro = entrada (0,0). Compare dois deles com Q "
           + "diferente: é o circuito lembrando.", x0, y0 + 34, COR.fraco, 11.5);
    }

    raiz.querySelectorAll("[data-acao]").forEach(function (b) {
      b.addEventListener("mousedown", function () {
        if (b.dataset.acao === "setR") st.r = 1;
        if (b.dataset.acao === "setS") st.s = 1;
        passo(); desenhar();
      });
      b.addEventListener("mouseup", function () {
        st.r = 0; st.s = 0; passo(); desenhar();
      });
      b.addEventListener("mouseleave", function () {
        if (st.r || st.s) { st.r = 0; st.s = 0; passo(); desenhar(); }
      });
    });
    // semente: S, solta, R, solta — a tira já abre PROVANDO a afirmação,
    // com duas entradas (0,0) de saídas diferentes. Instrumento que abre
    // neutro obriga o leitor a descobrir sozinho o que ele deveria mostrar.
    [[0,0],[0,1],[0,0],[0,0],[1,0],[0,0],[0,0]].forEach(function (e) {
      st.r = e[0]; st.s = e[1]; passo();
    });
    st.r = 0; st.s = 0;
    desenhar();
    window.addEventListener("resize", desenhar);
  }

  /* ------------------------------------------------------------------ *
   * [4] A CONTAGEM APARECE
   * Prova a aresta  flip-flop de borda → contador, e desarma a pergunta
   * "onde está a peça que faz a conta": não há. Cada estágio vira na metade
   * da frequência do anterior, e o binário É a fiação.
   * ------------------------------------------------------------------ */
  function contagemAparece(raiz) {
    var cv = raiz.querySelector("canvas");
    var st = { n: 0, bits: 4, tocando: false };

    function desenhar() {
      var c = ctx2d(cv), w = c.__w;
      var esq = 56, larg = w - esq - 20, jan = 32;
      // as ondas: cada estágio na metade da frequência do de cima
      for (var b = 0; b < st.bits; b++) {
        var yb = 40 + b * 38, alt = 20, div = Math.pow(2, b + 1);
        txt(c, b === 0 ? "relógio" : ("bit " + (b - 1)), esq - 10, yb - alt / 2,
            b === 0 ? COR.ouro : COR.seq, 11.5, "right");
        c.strokeStyle = b === 0 ? COR.ouro : COR.seq; c.lineWidth = 1.7;
        // A janela é [t0, n]. Quando ainda não houve n pulsos suficientes,
        // ela encolhe em vez de sumir — antes, com n=0, TODO ponto caía no
        // `continue` e a onda não era desenhada. O instrumento abria vazio.
        var t0 = Math.max(0, st.n - jan), span = Math.max(1, st.n - t0);
        c.beginPath();
        for (var i = 0; i <= span; i++) {
          var tt = t0 + i;
          var v = Math.floor(tt / div) % 2;
          var x = esq + i / span * larg, y = yb - (v ? alt : 0);
          if (i === 0) c.moveTo(x, y); else { c.lineTo(x, y); }
        }
        c.stroke();
      }
      // o número, lido da fiação
      var bits = [];
      for (var k = st.bits - 2; k >= 0; k--) bits.push((st.n >> k) & 1);
      var v = st.n % Math.pow(2, st.bits - 1);
      txt(c, "os bits, lidos de cima para baixo:", esq, 196, COR.fraco, 11.5);
      var xs = esq + 200;
      bits.forEach(function (bit, i) {
        c.fillStyle = bit ? COR.seq : "#1a2c45";
        c.fillRect(xs + i * 26, 186, 20, 20);
        txt(c, String(bit), xs + i * 26 + 10, 196, bit ? "#06231f" : COR.fraco,
            12, "center");
      });
      txt(c, "= " + v + " em decimal", xs + bits.length * 26 + 14, 196,
          COR.creme, 13);
      txt(c, "ninguém projetou a contagem: cada estágio vira na METADE da "
           + "frequência do anterior, e o binário é a fiação.",
          esq, 226, COR.fraco, 11.5);
    }

    var alvo = null;
    function tique() {
      if (st.tocando) { st.n++; desenhar(); }
      alvo = setTimeout(tique, 420);
    }
    raiz.querySelectorAll("[data-acao]").forEach(function (b) {
      b.addEventListener("click", function () {
        var a = b.dataset.acao;
        if (a === "step") { st.n++; }
        if (a === "autorun") { st.tocando = !st.tocando;
          b.textContent = st.tocando ? "parar" : "automático"; }
        if (a === "clear") { st.n = 0; }
        desenhar();
      });
    });
    desenhar(); tique();
    window.addEventListener("resize", desenhar);
  }

  /* ------------------------------------------------------------------ *
   * [5] DUAS PORTAS VIRAM UMA CONTA
   * Prova a aresta  porta lógica → somador: XOR dá a soma, AND dá o vai-um.
   * A conta binária aparece ao lado, para conferir que não é coincidência.
   * ------------------------------------------------------------------ */
  function portasViramConta(raiz) {
    var cv = raiz.querySelector("canvas");
    var st = { a: 0, b: 0 };
    function desenhar() {
      var c = ctx2d(cv), w = c.__w;
      var s = st.a ^ st.b, co = st.a & st.b;
      var xg = w * 0.34, y1 = 62, y2 = 128;
      porta(c, xg, y1, "OU-excl.", s, COR.frio);
      porta(c, xg, y2, "E", co, COR.frio);
      fio(c, [[70, y1 - 10], [xg - 32, y1 - 10]], st.a);
      fio(c, [[70, y1 + 10], [xg - 32, y1 + 10]], st.b);
      fio(c, [[70, y2 - 10], [xg - 32, y2 - 10]], st.a);
      fio(c, [[70, y2 + 10], [xg - 32, y2 + 10]], st.b);
      txt(c, "A = " + st.a, 40, y1 - 10, st.a ? COR.creme : COR.fraco, 12);
      txt(c, "B = " + st.b, 40, y1 + 10, st.b ? COR.creme : COR.fraco, 12);
      fio(c, [[xg + 34, y1], [xg + 78, y1]], s);
      fio(c, [[xg + 34, y2], [xg + 78, y2]], co);
      txt(c, "soma  = " + s,   xg + 88, y1, s  ? COR.creme : COR.fraco, 13);
      txt(c, "vai-um = " + co, xg + 88, y2, co ? COR.creme : COR.fraco, 13);
      // a conta, para conferir
      var x0 = w - 150;
      txt(c, "a conta:", x0, 46, COR.fraco, 11.5);
      txt(c, "  " + st.a, x0, 68, COR.creme, 15);
      txt(c, "+ " + st.b, x0, 88, COR.creme, 15);
      c.strokeStyle = COR.fio; c.lineWidth = 1;
      c.beginPath(); c.moveTo(x0, 100); c.lineTo(x0 + 46, 100); c.stroke();
      txt(c, (co ? "1" : "") + s, x0 + (co ? 6 : 18), 116, COR.ouro, 15);
      txt(c, "o par (vai-um, soma) lido como número binário É a soma.",
          40, 178, COR.fraco, 11.5);
      txt(c, st.a && st.b ? "1 + 1 = 10 em binário: dois, não dez."
                          : "experimente A = 1 e B = 1.",
          40, 198, st.a && st.b ? COR.ouro : COR.fraco, 12);
    }
    function porta(c, x, y, nome, ligado, cor) {
      c.fillStyle = "#132440"; c.strokeStyle = ligado ? COR.vivo : cor;
      c.lineWidth = 1.7;
      c.beginPath(); c.roundRect(x - 32, y - 22, 66, 44, 6); c.fill(); c.stroke();
      txt(c, nome, x + 1, y, ligado ? COR.creme : COR.txt, 12.5, "center");
    }
    raiz.querySelectorAll("[data-acao]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (b.dataset.acao === "inA") st.a ^= 1;
        if (b.dataset.acao === "inB") st.b ^= 1;
        b.classList.toggle("on", !!(b.dataset.acao === "inA" ? st.a : st.b));
        desenhar();
      });
    });
    desenhar();
    window.addEventListener("resize", desenhar);
  }

  // As chaves SAO os ids dos elementos, caractere a caractere. Isso nao e
  // estilo: o portao de traducao protege literal que casa com id declarado no
  // HTML, e um prefixo "i-" so no HTML fez o tradutor traduzir estas chaves e
  // derrubar quatro instrumentos na pagina em ingles, em silencio.
  var MONTA = {
    "i-rele-vira-porta": releViraPorta,
    "i-nivel-x-borda": nivelXBorda,
    "i-circuito-que-lembra": circuitoQueLembra,
    "i-contagem-aparece": contagemAparece,
    "i-portas-viram-conta": portasViramConta
  };

  function iniciar() {
    Object.keys(MONTA).forEach(function (id) {
      var el = document.getElementById(id);
      // uma seção escondida tem canvas de largura zero: só monta o que está à
      // vista, e o visor chama de novo quando mostra a tela
      if (el && !el.dataset.montado && el.offsetParent !== null) {
        el.dataset.montado = "1";
        try { MONTA[id](el); } catch (e) {
        var av = document.createElement("p");
        av.className = "aviso";
        av.textContent = "o instrumento não subiu neste navegador (" + e.message
                       + "). O texto e a citação acima continuam valendo.";
        el.appendChild(av);
      } }
    });
  }
  window.ESCADA_MONTAR = iniciar;
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", iniciar);
  else iniciar();
})();
