#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conferência da máquina, com controle negativo.

O que ela prova:
  1. o montador produz, para ola-mundo.asm, exatamente os bytes montados À MÃO
     na especificação (pesquisa/a-maquina.md) — o montador e a mão concordam;
  2. a máquina roda esses bytes e a primeira linha da tela diz "Olá, Mundo!";
  3. cada letra chegou à tela por UM ciclo de escrita em que o dado saiu de IL2
     e o endereço veio de HL — o caminho que o instrumento vai animar;
  4. CONTROLE NEGATIVO: um programa com um opcode trocado NÃO produz a frase, e
     a conferência acusa. Conferência que nunca reprovou não provou nada.

Roda:  python3 conferir_maquina.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import montar  # noqa: E402
import maquina  # noqa: E402

# Os bytes montados à mão na especificação. Se o montador discordar, um dos
# dois está errado, e a conferência não escolhe qual: ela reprova.
A_MAO = bytes.fromhex(
    "26 80"            # MVI H,80h
    "2E 00"            # MVI L,00h
    "36 4F 23"         # MVI M,'O'  INX H
    "36 6C 23"         # MVI M,'l'  INX H
    "36 E1 23"         # MVI M,'á'  INX H
    "36 2C 23"         # MVI M,','  INX H
    "36 20 23"         # MVI M,' '  INX H
    "36 4D 23"         # MVI M,'M'  INX H
    "36 75 23"         # MVI M,'u'  INX H
    "36 6E 23"         # MVI M,'n'  INX H
    "36 64 23"         # MVI M,'d'  INX H
    "36 6F 23"         # MVI M,'o'  INX H
    "36 21"            # MVI M,'!'
    "76"               # HLT
)
FRASE = "Olá, Mundo!"


def rodar(imagem):
    m = maquina.Maquina(imagem, traco=True)
    m.rodar(max_instrucoes=10_000)
    return m


def main():
    falhas = 0
    fonte = open(os.path.join(AQUI, "programas", "ola-mundo.asm"), encoding="utf-8").read()
    saida, _, _ = montar.montar(fonte)
    imagem = montar.binario(saida)

    # 1. montador = mão
    if imagem != A_MAO:
        print("REPROVADO: o montador e a montagem à mão discordam")
        print("  montador:", imagem.hex(" ").upper())
        print("  à mão:   ", A_MAO.hex(" ").upper())
        falhas += 1
    else:
        print(f"montador = mão: {len(imagem)} bytes (ok)")

    # 2. a tela
    m = rodar(imagem)
    linha0 = m.tela()[0].rstrip("·")
    if linha0 != FRASE or not m.parada:
        print(f"REPROVADO: a tela diz '{linha0}', parada={m.parada}")
        falhas += 1
    else:
        print(f"tela: '{linha0}' em {m.instrucoes} instruções e {m.ciclos} ciclos, parou em HLT (ok)")

    # 3. o caminho de cada letra: IL2 → barramento → RAM em [HL]
    escritas = [t for t in m.traco if t["dado_para"] == "RAM"]
    esperado = [(maquina.VIDEO_INICIO + i, ord(ch)) for i, ch in enumerate(FRASE)]
    visto = [(t["endereco"], t["dado"]) for t in escritas]
    if visto != esperado or any(t["dado_de"] != "IL2" or t["endereco_de"] != "HL" for t in escritas):
        print("REPROVADO: as escritas na tela não seguem o caminho IL2 → RAM[HL]")
        falhas += 1
    else:
        print(f"caminho: {len(escritas)} escritas, todas IL2 → barramento → RAM em [HL] (ok)")

    # 4. controle negativo: um opcode trocado (INX H → DCX H) não dá a frase
    quebrado = bytearray(imagem)
    quebrado[6] = 0x2B                    # o primeiro INX H vira DCX H
    q = rodar(bytes(quebrado))
    if q.tela()[0].rstrip("·") == FRASE:
        print("REPROVADO: o programa quebrado também produziu a frase — a conferência não mede nada")
        falhas += 1
    else:
        print(f"controle negativo: programa quebrado dá '{q.tela()[0].rstrip('·')}' (acusado, ok)")

    # 5. controle negativo do montador: mnemônica fora do subconjunto é erro
    try:
        montar.montar("        CALL 0005h\n")
        print("REPROVADO: o montador aceitou CALL, que esta máquina não tem")
        falhas += 1
    except montar.ErroDeMontagem as e:
        print(f"montador recusa o que a máquina não tem: {e} (ok)")

    if falhas:
        print(f"REPROVADO: {falhas} falha(s)")
        return 1
    print("PASSA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
