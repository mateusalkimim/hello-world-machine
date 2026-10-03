#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controle negativo do gerador: planta o defeito e exige o aborto.

`gerar_site.py` promete abortar quando um degrau vier sem warrant. Promessa
não é prova. Esta conferência copia os dados para uma pasta temporária, planta
UM defeito por vez, roda o gerador ali e exige que ele saia com erro. Se ele
aceitar um degrau sem citação, isto reprova.

Roda:  python3 conferir_degraus.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQUIVOS = ["gerar_site.py", "degraus.py", "figuras.py", "pele.css", "visor.js"]
PASTAS = ["maquina"]

# (nome do defeito, função que muta o texto de degraus.py)
DEFEITOS = [
    ("citação apagada em degrau lido",
     lambda s: s.replace('citacoes=[(\n            "In this book, the word code',
                         'citacoes=[], _x=[(\n            "In this book, the word code', 1)),
    ("tradução vazia",
     lambda s: __import__("re").sub(r'"Neste livro, a palavra código.*?computadores\."', '""', s, count=1, flags=__import__("re").S)),
    ("figura inexistente",
     lambda s: s.replace('figura="tres_meios"', 'figura="nao_existe"', 1)),
    ("tese acima do orçamento",
     lambda s: s.replace("tese='Dizer <span class=\"frase\">Olá, Mundo!</span>",
                         "tese='" + "palavra " * 26 + "<span class=\"frase\">Olá, Mundo!</span>", 1)),
    ("expressão sem lê-se",
     lambda s: s.replace("'código leva cada sinal num significado só, e dá para voltar'", "''", 1)),
    ("ciclo da placa que não mostra o que promete",
     lambda s: s.replace("placa=dict(ciclo=8, diz=", "placa=dict(ciclo=9, diz=", 1)),
    ("ciclo da placa fora do traço",
     lambda s: s.replace("placa=dict(ciclo=1, diz=", "placa=dict(ciclo=999, diz=", 1)),
    ("inglês no corpo visível",
     lambda s: s.replace("corpo='Código aqui não é segredo",
                         "corpo='The code is not a secret. Código aqui não é segredo", 1)),
]


def roda(pasta):
    r = subprocess.run([sys.executable, os.path.join(pasta, "gerar_site.py")],
                       capture_output=True, text=True)
    return r.returncode, r.stderr


def main():
    original = open(os.path.join(AQUI, "degraus.py"), encoding="utf-8").read()
    falhas = 0
    with tempfile.TemporaryDirectory() as tmp:
        for a in ARQUIVOS:
            shutil.copy(os.path.join(AQUI, a), tmp)
        for d in PASTAS:
            shutil.copytree(os.path.join(AQUI, d), os.path.join(tmp, d), ignore=shutil.ignore_patterns("__pycache__"))
        rc, err = roda(tmp)
        if rc != 0:
            print("REPROVADO: o gerador falha nos dados ÍNTEGROS:\n" + err)
            return 1
        print("íntegro: gera (ok)")
        for nome, muta in DEFEITOS:
            mutado = muta(original)
            if mutado == original:
                print(f"REPROVADO: o defeito '{nome}' não foi plantado (o texto-alvo mudou)")
                falhas += 1
                continue
            with open(os.path.join(tmp, "degraus.py"), "w", encoding="utf-8") as f:
                f.write(mutado)
            rc, err = roda(tmp)
            if rc == 0:
                print(f"REPROVADO: '{nome}' passou sem aborto")
                falhas += 1
            else:
                print(f"{nome}: aborta ({err.strip().splitlines()[-1]})")
    if falhas:
        print(f"REPROVADO: {falhas} defeito(s) não detectado(s)")
        return 1
    print(f"PASSA: {len(DEFEITOS)} defeitos plantados, {len(DEFEITOS)} abortos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
