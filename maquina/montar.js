/* O montador, em JavaScript: a mesma linguagem de montar.py, para o navegador.
 *
 * Segunda implementação do montador. conferir_equivalencia.py exige que os dois
 * produzam os mesmos bytes para o mesmo texto, e que os dois recusem o que a
 * máquina não tem.
 */
(function (raiz) {
  "use strict";

  var REG = { B: 0, C: 1, D: 2, E: 3, H: 4, L: 5, M: 6, A: 7 };
  var ULA = { ADD: 0, ADC: 1, SUB: 2, SBB: 3, ANA: 4, XRA: 5, ORA: 6, CMP: 7 };
  var ULA_IMED = { ADI: 0, ACI: 1, SUI: 2, SBI: 3, ANI: 4, XRI: 5, ORI: 6, CPI: 7 };
  var SALTO = { JMP: 0xC3, JNZ: 0xC2, JZ: 0xCA, JNC: 0xD2, JC: 0xDA, JP: 0xF2, JM: 0xFA };
  var SIMPLES = { HLT: 0x76, INX: 0x23, DCX: 0x2B, PCHL: 0xE9 };

  function ErroDeMontagem(msg) { this.name = "ErroDeMontagem"; this.message = msg; }
  ErroDeMontagem.prototype = Object.create(Error.prototype);

  function numero(tok, rotulos, linha) {
    tok = tok.trim();
    if (/^'.'$/.test(tok)) return tok.charCodeAt(1);
    if (/^[0-9A-Fa-f]+[hH]$/.test(tok)) return parseInt(tok.slice(0, -1), 16);
    if (/^[0-9]+$/.test(tok)) return parseInt(tok, 10);
    if (rotulos && Object.prototype.hasOwnProperty.call(rotulos, tok)) return rotulos[tok];
    throw new ErroDeMontagem("linha " + linha + ": não entendo o valor '" + tok + "'");
  }

  function separar(texto) {
    var ops = [], atual = "", dentro = false, i, ch;
    for (i = 0; i < texto.length; i++) {
      ch = texto[i];
      if (ch === "'") dentro = !dentro;
      if (ch === "," && !dentro) { ops.push(atual); atual = ""; }
      else atual += ch;
    }
    ops.push(atual);
    return ops;
  }

  function partir(texto) {
    var saida = [], linhas = texto.split(/\r?\n/), n, bruta, linha, m, rotulo, partes, mnem, ops;
    for (n = 0; n < linhas.length; n++) {
      bruta = linhas[n];
      linha = bruta.split(";")[0].trim();
      if (!linha) continue;
      rotulo = null;
      m = /^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$/.exec(linha);
      if (m) { rotulo = m[1]; linha = m[2].trim(); }
      if (!linha) { saida.push([n + 1, rotulo, null, []]); continue; }
      partes = linha.split(/\s+/);
      mnem = partes[0].toUpperCase();
      ops = [];
      if (partes.length > 1) {
        ops = separar(linha.slice(partes[0].length).trim()).map(function (o) { return o.trim(); }).filter(Boolean);
      }
      saida.push([n + 1, rotulo, mnem, ops]);
    }
    return saida;
  }

  function latin1(s) {
    var bs = [], i, c;
    for (i = 0; i < s.length; i++) {
      c = s.charCodeAt(i);
      if (c > 255) throw new ErroDeMontagem("letra fora dos 256 primeiros códigos: '" + s[i] + "'");
      bs.push(c);
    }
    return bs;
  }

  function tamanho(mnem, ops, n) {
    if (mnem === "ORG") return 0;
    if (mnem === "DB") {
      return ops.reduce(function (t, o) {
        return t + ((o[0] === "'" && o.length > 3) ? latin1(o.slice(1, -1)).length : 1);
      }, 0);
    }
    if (mnem === "MVI") return 2;
    if (ULA_IMED.hasOwnProperty(mnem)) return 2;
    if (mnem === "STA" || mnem === "LDA" || SALTO.hasOwnProperty(mnem)) return 3;
    if (mnem === "MOV" || ULA.hasOwnProperty(mnem) || SIMPLES.hasOwnProperty(mnem)) return 1;
    throw new ErroDeMontagem("linha " + n + ": mnemônica '" + mnem + "' não existe nesta máquina");
  }

  function montar(texto) {
    var rotulos = {}, pc = 0, saida = {}, listagem = [], itens = partir(texto), i, it, n, rot, mnem, ops, bs, d, s, a, txt;
    for (i = 0; i < itens.length; i++) {
      it = itens[i]; n = it[0]; rot = it[1]; mnem = it[2]; ops = it[3];
      if (rot) rotulos[rot] = pc;
      if (mnem === "ORG") pc = numero(ops[0], null, n);
      else if (mnem) pc += tamanho(mnem, ops, n);
    }
    pc = 0;
    function emitir(bytes, texto) {
      listagem.push([pc, bytes.slice(), texto]);
      bytes.forEach(function (b) {
        if (b < 0 || b > 255) throw new ErroDeMontagem("linha " + n + ": byte fora de 0..255");
        saida[pc] = b; pc += 1;
      });
    }
    for (i = 0; i < itens.length; i++) {
      it = itens[i]; n = it[0]; rot = it[1]; mnem = it[2]; ops = it[3];
      if (mnem === null) continue;
      txt = (rot ? rot + ": " : "") + mnem + (ops.length ? " " + ops.join(", ") : "");
      if (mnem === "ORG") { pc = numero(ops[0], null, n); }
      else if (mnem === "DB") {
        bs = [];
        ops.forEach(function (o) {
          if (o[0] === "'" && o.length > 3) bs = bs.concat(latin1(o.slice(1, -1)));
          else bs.push(numero(o, rotulos, n));
        });
        emitir(bs, txt);
      }
      else if (mnem === "MVI") {
        d = ops[0].toUpperCase();
        emitir([0x06 | (REG[d] << 3), numero(ops[1], rotulos, n)], txt);
      }
      else if (mnem === "MOV") {
        d = ops[0].toUpperCase(); s = ops[1].toUpperCase();
        if (d === "M" && s === "M") throw new ErroDeMontagem("linha " + n + ": MOV M,M não existe (76h é HLT)");
        emitir([0x40 | (REG[d] << 3) | REG[s]], txt);
      }
      else if (ULA.hasOwnProperty(mnem)) emitir([0x80 | (ULA[mnem] << 3) | REG[ops[0].toUpperCase()]], txt);
      else if (ULA_IMED.hasOwnProperty(mnem)) emitir([0xC6 | (ULA_IMED[mnem] << 3), numero(ops[0], rotulos, n)], txt);
      else if (mnem === "STA" || mnem === "LDA") {
        a = numero(ops[0], rotulos, n);
        emitir([mnem === "STA" ? 0x32 : 0x3A, a & 0xFF, a >> 8], txt);
      }
      else if (SALTO.hasOwnProperty(mnem)) {
        a = numero(ops[0], rotulos, n);
        emitir([SALTO[mnem], a & 0xFF, a >> 8], txt);
      }
      else if (mnem === "INX" || mnem === "DCX") {
        if (ops.length && ops[0].toUpperCase() !== "H" && ops[0].toUpperCase() !== "HL") throw new ErroDeMontagem("linha " + n + ": só o par HL tem INX/DCX nesta máquina");
        emitir([SIMPLES[mnem]], txt);
      }
      else if (SIMPLES.hasOwnProperty(mnem)) emitir([SIMPLES[mnem]], txt);
      else throw new ErroDeMontagem("linha " + n + ": mnemônica '" + mnem + "' não existe nesta máquina");
    }
    return { saida: saida, rotulos: rotulos, listagem: listagem };
  }

  function binario(saida) {
    var chaves = Object.keys(saida).map(Number);
    if (!chaves.length) return new Uint8Array(0);
    var fim = Math.max.apply(null, chaves) + 1, out = new Uint8Array(fim), i;
    for (i = 0; i < fim; i++) out[i] = saida.hasOwnProperty(i) ? saida[i] : 0;
    return out;
  }

  var MONTAR = { montar: montar, binario: binario, ErroDeMontagem: ErroDeMontagem };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = MONTAR;
    if (require.main === module) {                    // uso: node montar.js programa.asm [saida.bin]
      var fs = require("fs");
      var args = process.argv.slice(2);
      var r = montar(fs.readFileSync(args[0], "utf8"));
      r.listagem.forEach(function (l) {
        console.log(l[0].toString(16).toUpperCase().padStart(4, "0") + "  " +
          l[1].map(function (b) { return b.toString(16).toUpperCase().padStart(2, "0"); }).join(" ").padEnd(20) + " " + l[2]);
      });
      if (args[1]) fs.writeFileSync(args[1], Buffer.from(binario(r.saida)));
    }
  } else {
    raiz.HWM_MONTAR = MONTAR;
  }
})(typeof window !== "undefined" ? window : this);
