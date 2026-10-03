#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Equivalência entre as duas implementações da máquina: Python e JavaScript.

A especificação (pesquisa/a-maquina.md) é quem manda. Duas implementações
independentes que produzem, para o mesmo programa, o MESMO traço campo a campo
são a prova de que nenhuma das duas inventou comportamento. Esta conferência
usa o node só para rodar o JavaScript fora do navegador; o site não depende
dele.

O que ela prova:
  1. os dois montadores produzem os mesmos bytes para cada programa em programas/;
  2. as duas máquinas produzem o mesmo estado final e o mesmo traço, ciclo a
     ciclo, para cada programa — inclusive para um programa QUEBRADO, porque
     equivalência vale para o erro também;
  3. os dois montadores recusam o que a máquina não tem (CALL);
  4. CONTROLE NEGATIVO: um traço com um único campo alterado é acusado pelo
     comparador. Comparador que nunca acusou não compara nada.

Roda:  python3 conferir_equivalencia.py
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import montar  # noqa: E402
import maquina  # noqa: E402

NODE = shutil.which("node")


def js(script, *args):
    r = subprocess.run([NODE, os.path.join(AQUI, script)] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{script} falhou: {r.stderr.strip()}")
    return r.stdout


def estado_py(imagem, roteiro=None, maximo=100_000):
    m = maquina.Maquina(imagem, traco=True)
    for n, c in (roteiro or []):
        m.roteiro[n] = c
    m.rodar(max_instrucoes=maximo)
    return json.loads(json.dumps(maquina.estado(m), sort_keys=True))


def estado_js(imagem, tmp, roteiro=None, maximo=100_000):
    p = os.path.join(tmp, "prog.bin")
    with open(p, "wb") as f:
        f.write(imagem)
    args = [p, "--json", "--max", str(maximo)]
    if roteiro:
        rp = os.path.join(tmp, "roteiro.json")
        with open(rp, "w", encoding="utf-8") as f:
            json.dump(roteiro, f)
        args += ["--roteiro", rp]
    return json.loads(js("maquina.js", *args))


def roteiro_de(asm):
    """O roteiro de teclas ao lado do programa, se houver; e o máximo de instruções."""
    rp = asm[:-4] + ".roteiro.json"
    if os.path.exists(rp):
        return json.load(open(rp, encoding="utf-8")), 400
    return None, 100_000


def diferencas(a, b, caminho=""):
    """Lista as diferenças entre dois estados, campo a campo."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{caminho}.{k}: só de um lado")
            else:
                out += diferencas(a[k], b[k], f"{caminho}.{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{caminho}: tamanhos {len(a)} ≠ {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            out += diferencas(x, y, f"{caminho}[{i}]")
    elif a != b:
        out.append(f"{caminho}: {a!r} ≠ {b!r}")
    return out


def main():
    if not NODE:
        print("REPROVADO: node não encontrado — a conferência precisa dele para rodar o JavaScript")
        return 1
    falhas = 0
    programas = sorted(glob.glob(os.path.join(AQUI, "programas", "*.asm")))
    with tempfile.TemporaryDirectory() as tmp:
        for asm in programas:
            nome = os.path.basename(asm)
            fonte = open(asm, encoding="utf-8").read()
            # 1. montadores
            py_bytes = montar.binario(montar.montar(fonte)[0])
            saida_js = os.path.join(tmp, "js.bin")
            js("montar.js", asm, saida_js)
            js_bytes = open(saida_js, "rb").read()
            if py_bytes != js_bytes:
                print(f"REPROVADO {nome}: montadores discordam\n  py {py_bytes.hex(' ')}\n  js {js_bytes.hex(' ')}")
                falhas += 1
                continue
            # 2. máquinas, programa íntegro e programa quebrado
            roteiro, maximo = roteiro_de(asm)
            for rotulo, imagem in (("íntegro", py_bytes), ("quebrado", py_bytes[:6] + b"\x2b" + py_bytes[7:])):
                e = estado_py(imagem, roteiro, maximo)
                d = diferencas(e, estado_js(imagem, tmp, roteiro, maximo))
                if d:
                    print(f"REPROVADO {nome} ({rotulo}): {len(d)} diferença(s), a primeira: {d[0]}")
                    falhas += 1
                else:
                    print(f"{nome} ({rotulo}): {len(py_bytes)} bytes, {e['ciclos']} ciclos{' com teclas de roteiro' if roteiro else ''}, traço idêntico em Python e JavaScript (ok)")
        # 3. recusas
        try:
            montar.montar("        CALL 0005h\n")
            print("REPROVADO: montar.py aceitou CALL"); falhas += 1
        except montar.ErroDeMontagem:
            pass
        p = os.path.join(tmp, "call.asm")
        with open(p, "w", encoding="utf-8") as f:
            f.write("        CALL 0005h\n")
        r = subprocess.run([NODE, os.path.join(AQUI, "montar.js"), p], capture_output=True, text=True)
        if r.returncode == 0:
            print("REPROVADO: montar.js aceitou CALL"); falhas += 1
        else:
            print("os dois montadores recusam CALL (ok)")
        # 4. controle negativo do comparador
        base = estado_py(montar.binario(montar.montar(open(programas[-1], encoding="utf-8").read())[0]))
        alterado = json.loads(json.dumps(base))
        alterado["traco"][8]["dado"] = 0x50          # a letra O vira P num único ciclo
        d = diferencas(base, alterado)
        if not d:
            print("REPROVADO: o comparador não viu um campo alterado"); falhas += 1
        else:
            print(f"controle negativo: campo alterado acusado em {d[0]} (ok)")
    if falhas:
        print(f"REPROVADO: {falhas} falha(s)")
        return 1
    print("PASSA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
