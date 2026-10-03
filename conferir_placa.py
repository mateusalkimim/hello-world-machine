#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conferência da placa, com controle negativo.

O que ela prova:
  1. placa.js passa no verificador de sintaxe do node;
  2. todo nome de origem e destino que aparece no traço de CADA programa tem
     um módulo desenhado (nome sem caixa = ciclo invisível na placa);
  3. CONTROLE NEGATIVO: um registro com um nome inventado é recusado;
  4. pt/placa.html existe, foi gerada, e referencia os três roteiros.

Roda:  python3 conferir_placa.py
"""
import glob
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "maquina"))
import montar  # noqa: E402
import maquina  # noqa: E402

NODE = shutil.which("node")

SONDA = r"""
const P = require(process.argv[2]);
const traco = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
let falhas = 0;
for (const t of traco) {
  try {
    const m = P.mapear(t);
    for (const k of ['dadoDe', 'dadoPara', 'endDe', 'endPara']) {
      if (m[k] !== null && !(m[k] in P.MODULOS)) { console.log('sem caixa: ' + k + '=' + m[k] + ' no ciclo ' + t.n); falhas++; }
    }
  } catch (e) { console.log('ciclo ' + t.n + ': ' + e.message); falhas++; }
}
let recusou = false;
try { P.mapear({ dado_de: 'XYZ', dado_para: 'RAM', endereco_de: 'PC', endereco: 0, nota: '' }); } catch (e) { recusou = true; }
console.log(JSON.stringify({ falhas, recusou, modulos: Object.keys(P.MODULOS).length }));
"""


def main():
    if not NODE:
        print("REPROVADO: node não encontrado")
        return 1
    falhas = 0
    r = subprocess.run([NODE, "--check", os.path.join(AQUI, "placa.js")], capture_output=True, text=True)
    if r.returncode != 0:
        print("REPROVADO: placa.js não passa na sintaxe:\n" + r.stderr)
        return 1
    print("placa.js: sintaxe ok")
    sonda = os.path.join(AQUI, "__pycache__", "sonda_placa.js")
    os.makedirs(os.path.dirname(sonda), exist_ok=True)
    with open(sonda, "w", encoding="utf-8") as f:
        f.write(SONDA)
    for asm in sorted(glob.glob(os.path.join(AQUI, "maquina", "programas", "*.asm"))):
        fonte = open(asm, encoding="utf-8").read()
        m = maquina.Maquina(montar.binario(montar.montar(fonte)[0]), traco=True)
        m.rodar(100_000)
        tj = os.path.join(AQUI, "__pycache__", "traco.json")
        with open(tj, "w", encoding="utf-8") as f:
            json.dump(m.traco, f)
        r = subprocess.run([NODE, sonda, os.path.join(AQUI, "placa.js"), tj], capture_output=True, text=True)
        linhas = r.stdout.strip().splitlines()
        res = json.loads(linhas[-1]) if linhas else {"falhas": 1, "recusou": False}
        if r.returncode != 0 or res["falhas"]:
            print(f"REPROVADO {os.path.basename(asm)}: {r.stdout}{r.stderr}")
            falhas += 1
        else:
            print(f"{os.path.basename(asm)}: {len(m.traco)} ciclos, todos com origem e destino desenhados em {res['modulos']} módulos (ok)")
        if not res.get("recusou"):
            print("REPROVADO: um nome inventado NÃO foi recusado — a conferência não mede nada")
            falhas += 1
    print("controle negativo: nome inventado recusado (ok)")
    pagina = os.path.join(AQUI, "pt", "placa.html")
    if not os.path.exists(pagina):
        print("REPROVADO: pt/placa.html não existe (rode gerar_placa.py)")
        falhas += 1
    else:
        h = open(pagina, encoding="utf-8").read()
        for ref in ("../maquina/montar.js", "../maquina/maquina.js", "../placa.js", 'id="asm"'):
            if ref not in h:
                print(f"REPROVADO: pt/placa.html não referencia {ref}")
                falhas += 1
        print("pt/placa.html: referencia os três roteiros e carrega o programa (ok)")
    if falhas:
        print(f"REPROVADO: {falhas} falha(s)")
        return 1
    print("PASSA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
