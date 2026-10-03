/* A máquina, em JavaScript: a mesma CPU de maquina.py, para rodar no navegador.
 *
 * Esta é a SEGUNDA implementação da especificação (pesquisa/a-maquina.md). A
 * primeira é maquina.py. As duas têm de produzir, para o mesmo programa, o
 * MESMO traço, campo a campo — é o que conferir_equivalencia.py exige. Se
 * divergirem, uma delas está errada, e a especificação é quem decide.
 *
 * Sem dependência: roda no navegador (global HWM) e no node (module.exports),
 * e o node serve só à conferência, nunca ao site.
 */
(function (raiz) {
  "use strict";

  var VIDEO_INICIO = 0x8000, VIDEO_COLUNAS = 12, VIDEO_LINHAS = 22;
  var VIDEO_FIM = VIDEO_INICIO + VIDEO_COLUNAS * VIDEO_LINHAS;
  var TECLADO = 0x8200;
  var NOME_REG = ["B", "C", "D", "E", "H", "L", "M", "A"];
  var NOME_ULA = ["ADD", "ADC", "SUB", "SBB", "ANA", "XRA", "ORA", "CMP"];

  function hex(n, casas) { return n.toString(16).toUpperCase().padStart(casas, "0"); }

  function Maquina(imagem, traco) {
    this.mem = new Uint8Array(65536);
    if (imagem) this.mem.set(imagem.subarray ? imagem.subarray(0, 65536) : imagem);
    this.reg = { A: 0, B: 0, C: 0, D: 0, E: 0, H: 0, L: 0 };
    this.pc = 0;
    this.cy = 0; this.z = 0; this.s = 0;
    this.il = [0, 0, 0];
    this.parada = false;
    this.ciclos = 0;
    this.instrucoes = 0;
    this.traco = traco ? [] : null;
    this.tecla = 0;
  }

  Maquina.prototype.ler = function (end) {
    if (end === TECLADO) return this.tecla;
    return this.mem[end];
  };
  Maquina.prototype.escrever = function (end, v) {
    if (end === TECLADO) { this.tecla = 0; return; }
    this.mem[end] = v & 0xFF;
  };
  Maquina.prototype.apertar = function (codigo) { this.tecla = codigo & 0xFF; };
  Maquina.prototype.hl = function () { return (this.reg.H << 8) | this.reg.L; };
  Maquina.prototype.porHl = function (v) { this.reg.H = (v >> 8) & 0xFF; this.reg.L = v & 0xFF; };
  Maquina.prototype.flags = function () {
    return (this.cy ? "C" : "-") + (this.z ? "Z" : "-") + (this.s ? "S" : "-");
  };

  Maquina.prototype.ciclo = function (fase, end, endDe, dado, dadoDe, dadoPara, nota) {
    this.ciclos += 1;
    if (this.traco !== null) {
      this.traco.push({
        n: this.ciclos, instrucao: this.instrucoes, fase: fase,
        endereco: end, endereco_de: endDe,
        dado: dado, dado_de: dadoDe, dado_para: dadoPara,
        pc: this.pc, a: this.reg.A, b: this.reg.B, c: this.reg.C, d: this.reg.D, e: this.reg.E, hl: this.hl(),
        flags: this.flags(), nota: nota || ""
      });
    }
  };

  Maquina.prototype.buscar = function (latch) {
    var b = this.ler(this.pc);
    this.il[latch] = b;
    this.ciclo("busca", this.pc, "PC", b, "RAM", "IL" + (latch + 1));
    this.pc = (this.pc + 1) & 0xFFFF;
    return b;
  };

  Maquina.prototype.ula = function (f, b) {
    var a = this.reg.A, r;
    if (f === 0) r = a + b;
    else if (f === 1) r = a + b + this.cy;
    else if (f === 2) r = a - b;
    else if (f === 3) r = a - b - this.cy;
    else if (f === 4) r = a & b;
    else if (f === 5) r = a ^ b;
    else if (f === 6) r = a | b;
    else r = a - b;
    if (f === 0 || f === 1) this.cy = r > 0xFF ? 1 : 0;
    else if (f === 2 || f === 3 || f === 7) this.cy = r < 0 ? 1 : 0;
    else this.cy = 0;
    r &= 0xFF;
    this.z = r === 0 ? 1 : 0;
    this.s = (r & 0x80) ? 1 : 0;
    if (f !== 7) this.reg.A = r;
    return r;
  };

  Maquina.prototype.passo = function () {
    if (this.parada) return false;
    this.instrucoes += 1;
    var op = this.buscar(0);
    var ddd = (op >> 3) & 7, sss = op & 7, v, b, r, f, lo, hi, end, antes, alvo, cond;

    if (op === 0x76) {
      this.ciclo("execução", null, "", null, "", "", "HLT: a máquina para");
      this.parada = true;
      return false;
    }
    if ((op & 0xC7) === 0x06) {                       // MVI
      v = this.buscar(1);
      if (ddd === 6) {
        this.escrever(this.hl(), v);
        this.ciclo("execução", this.hl(), "HL", v, "IL2", "RAM", "MVI M: escreve em [HL]");
      } else {
        this.reg[NOME_REG[ddd]] = v;
        this.ciclo("execução", null, "", v, "IL2", NOME_REG[ddd], "MVI " + NOME_REG[ddd]);
      }
      return true;
    }
    if ((op & 0xC0) === 0x40) {                       // MOV
      if (sss === 6) {
        v = this.ler(this.hl());
        this.reg[NOME_REG[ddd]] = v;
        this.ciclo("execução", this.hl(), "HL", v, "RAM", NOME_REG[ddd], "MOV " + NOME_REG[ddd] + ",M");
      } else if (ddd === 6) {
        v = this.reg[NOME_REG[sss]];
        this.escrever(this.hl(), v);
        this.ciclo("execução", this.hl(), "HL", v, NOME_REG[sss], "RAM", "MOV M," + NOME_REG[sss]);
      } else {
        v = this.reg[NOME_REG[sss]];
        this.reg[NOME_REG[ddd]] = v;
        this.ciclo("execução", null, "", v, NOME_REG[sss], NOME_REG[ddd], "MOV " + NOME_REG[ddd] + "," + NOME_REG[sss]);
      }
      return true;
    }
    if ((op & 0xC0) === 0x80) {                       // ADD r … CMP r
      f = ddd;
      if (sss === 6) {
        b = this.ler(this.hl());
        this.ciclo("execução", this.hl(), "HL", b, "RAM", "ULA.B", NOME_ULA[f] + " M");
      } else {
        b = this.reg[NOME_REG[sss]];
        this.ciclo("execução", null, "", b, NOME_REG[sss], "ULA.B", NOME_ULA[f] + " " + NOME_REG[sss]);
      }
      r = this.ula(f, b);
      this.ciclo("execução", null, "", r, "ULA", f !== 7 ? "A" : "flags", "resultado da ULA, flags " + this.flags());
      return true;
    }
    if ((op & 0xC7) === 0xC6) {                       // ADI … CPI
      f = ddd;
      b = this.buscar(1);
      this.ciclo("execução", null, "", b, "IL2", "ULA.B", NOME_ULA[f] + "I");
      r = this.ula(f, b);
      this.ciclo("execução", null, "", r, "ULA", f !== 7 ? "A" : "flags", "resultado da ULA, flags " + this.flags());
      return true;
    }
    if (op === 0x32 || op === 0x3A) {                 // STA / LDA
      lo = this.buscar(1); hi = this.buscar(2);
      end = (hi << 8) | lo;
      if (op === 0x32) {
        this.escrever(end, this.reg.A);
        this.ciclo("execução", end, "IL2+IL3", this.reg.A, "A", "RAM", "STA");
      } else {
        v = this.ler(end);
        this.reg.A = v;
        this.ciclo("execução", end, "IL2+IL3", v, end !== TECLADO ? "RAM" : "teclado", "A", "LDA");
      }
      return true;
    }
    if (op === 0x23 || op === 0x2B) {                 // INX H / DCX H
      antes = this.hl();
      this.porHl((antes + (op === 0x23 ? 1 : -1)) & 0xFFFF);
      this.ciclo("execução", antes, "HL", null, "", "", (op === 0x23 ? "INX" : "DCX") + " HL → incrementador-decrementador → HL = " + hex(this.hl(), 4));
      return true;
    }
    if (op === 0xE9) {                                // PCHL
      this.ciclo("execução", this.hl(), "HL", null, "", "", "PCHL: HL vai para o PC");
      this.pc = this.hl();
      return true;
    }
    if ((op & 0xC7) === 0xC2 || op === 0xC3) {        // saltos
      lo = this.buscar(1); hi = this.buscar(2);
      alvo = (hi << 8) | lo;
      cond = { 0xC3: true, 0xC2: !this.z, 0xCA: !!this.z, 0xD2: !this.cy, 0xDA: !!this.cy, 0xF2: !this.s, 0xFA: !!this.s }[op];
      if (cond === undefined) throw new Error("opcode " + hex(op, 2) + " não existe nesta máquina (PC=" + hex(this.pc - 3, 4) + ")");
      if (cond) {
        this.ciclo("execução", alvo, "IL2+IL3", null, "", "", "salto tomado: PC = " + hex(alvo, 4));
        this.pc = alvo;
      } else {
        this.ciclo("execução", null, "", null, "", "", "salto não tomado");
      }
      return true;
    }
    throw new Error("opcode " + hex(op, 2) + " não existe nesta máquina (PC=" + hex(this.pc - 1, 4) + ")");
  };

  Maquina.prototype.rodar = function (maxInstrucoes) {
    var max = maxInstrucoes || 1000000;
    while (!this.parada && this.instrucoes < max) this.passo();
    return this.instrucoes;
  };

  function celula(b) {
    if (b === 0) return "·";
    if (b >= 1 && b <= 7) return "▮";
    if (b === 8) return "█";
    if ((b >= 0x20 && b <= 0x7E) || (b >= 0xA0 && b <= 0xFF)) return String.fromCharCode(b);
    return "?";
  }

  Maquina.prototype.tela = function () {
    var linhas = [], r, c, base, s;
    for (r = 0; r < VIDEO_LINHAS; r++) {
      base = VIDEO_INICIO + r * VIDEO_COLUNAS; s = "";
      for (c = 0; c < VIDEO_COLUNAS; c++) s += celula(this.mem[base + c]);
      linhas.push(s);
    }
    return linhas;
  };

  Maquina.prototype.estado = function () {
    return {
      instrucoes: this.instrucoes, ciclos: this.ciclos, parada: this.parada,
      reg: { A: this.reg.A, B: this.reg.B, C: this.reg.C, D: this.reg.D, E: this.reg.E, H: this.reg.H, L: this.reg.L },
      pc: this.pc, flags: this.flags(), hl: this.hl(),
      tela: this.tela(), traco: this.traco || []
    };
  };

  var HWM = {
    Maquina: Maquina, celula: celula, hex: hex,
    VIDEO_INICIO: VIDEO_INICIO, VIDEO_COLUNAS: VIDEO_COLUNAS, VIDEO_LINHAS: VIDEO_LINHAS, VIDEO_FIM: VIDEO_FIM, TECLADO: TECLADO
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = HWM;
    if (require.main === module) {                    // uso: node maquina.js programa.bin [--json]
      var fs = require("fs");
      var args = process.argv.slice(2);
      var imagem = new Uint8Array(fs.readFileSync(args[0]));
      var m = new Maquina(imagem, true);
      m.rodar();
      if (args.indexOf("--json") >= 0) {
        process.stdout.write(JSON.stringify(m.estado()) + "\n");
      } else {
        console.log(m.instrucoes + " instruções, " + m.ciclos + " ciclos, " + (m.parada ? "parou em HLT" : "não parou"));
        m.tela().forEach(function (l, i) { if (l.replace(/·/g, "")) console.log("vídeo linha " + i + ": " + l); });
      }
    }
  } else {
    raiz.HWM = HWM;
  }
})(typeof window !== "undefined" ? window : this);
