#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Montador da máquina: texto em linguagem de montagem → bytes.

A linguagem é o subconjunto do Intel 8080 que o Petzold constrói nos capítulos
22 a 24 de *Code* (2ª ed.): MVI, MOV, as oito operações da ULA (com registrador
ou imediata), STA, LDA, INX H, DCX H, os sete saltos, PCHL e HLT. Nada além:
uma mnemônica fora da lista é erro, não extensão.

Uso:  python3 montar.py programa.asm            # imprime os bytes em hexadecimal
      python3 montar.py programa.asm saida.bin  # grava o binário

Sintaxe:
    ORG 0000h            ; endereço de origem (padrão 0000h)
    rotulo:              ; rótulo, sozinho na linha ou antes da instrução
    MVI A, 4Fh           ; números: 4Fh (hexadecimal), 79 (decimal), 'O' (letra)
    DB 'Olá', 0          ; bytes literais; letras com acento valem o código Unicode (á = E1h)
    JMP rotulo           ; rótulo em lugar de endereço de 16 bits
    ; comentário até o fim da linha

O que o montador faz com o número: troca cada palavra por um byte, uma linha
por uma ordem — é a correspondência um-para-um que o livro descreve no cap. 27.
"""
import re
import sys

REG = {"B": 0, "C": 1, "D": 2, "E": 3, "H": 4, "L": 5, "M": 6, "A": 7}
ULA = {"ADD": 0, "ADC": 1, "SUB": 2, "SBB": 3, "ANA": 4, "XRA": 5, "ORA": 6, "CMP": 7}
ULA_IMED = {"ADI": 0, "ACI": 1, "SUI": 2, "SBI": 3, "ANI": 4, "XRI": 5, "ORI": 6, "CPI": 7}
SALTO = {"JMP": 0xC3, "JNZ": 0xC2, "JZ": 0xCA, "JNC": 0xD2, "JC": 0xDA, "JP": 0xF2, "JM": 0xFA}
SIMPLES = {"HLT": 0x76, "INX": 0x23, "DCX": 0x2B, "PCHL": 0xE9}


class ErroDeMontagem(Exception):
    pass


def numero(tok, rotulos=None, linha=0):
    tok = tok.strip()
    if re.fullmatch(r"'.'", tok):
        return ord(tok[1])
    if re.fullmatch(r"[0-9A-Fa-f]+[hH]", tok):
        return int(tok[:-1], 16)
    if re.fullmatch(r"[0-9]+", tok):
        return int(tok)
    if rotulos is not None and tok in rotulos:
        return rotulos[tok]
    raise ErroDeMontagem(f"linha {linha}: não entendo o valor '{tok}'")


def separar(texto):
    """Separa operandos por vírgula, respeitando o que está entre aspas simples."""
    ops, atual, dentro = [], "", False
    for ch in texto:
        if ch == "'":
            dentro = not dentro
        if ch == "," and not dentro:
            ops.append(atual)
            atual = ""
        else:
            atual += ch
    ops.append(atual)
    return ops


def partir(texto):
    """Linha a linha: (número da linha, rótulo ou None, mnemônica ou None, operandos)."""
    for n, bruta in enumerate(texto.splitlines(), 1):
        linha = bruta.split(";", 1)[0].strip()
        if not linha:
            continue
        rotulo = None
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", linha)
        if m:
            rotulo, linha = m.group(1), m.group(2).strip()
        if not linha:
            yield n, rotulo, None, []
            continue
        partes = linha.split(None, 1)
        mnem = partes[0].upper()
        ops = []
        if len(partes) > 1:
            ops = [o.strip() for o in separar(partes[1]) if o.strip()]
        yield n, rotulo, mnem, ops


def tamanho(mnem, ops, n):
    if mnem in ("ORG",):
        return 0
    if mnem == "DB":
        t = 0
        for o in ops:
            t += len(o[1:-1].encode("latin-1")) if (o.startswith("'") and len(o) > 3) else 1
        return t
    if mnem == "MVI":
        return 2
    if mnem in ULA_IMED:
        return 2
    if mnem in ("STA", "LDA") or mnem in SALTO:
        return 3
    if mnem in ("MOV",) or mnem in ULA or mnem in SIMPLES:
        return 1
    raise ErroDeMontagem(f"linha {n}: mnemônica '{mnem}' não existe nesta máquina")


def montar(texto):
    """Devolve (bytes, rotulos, listagem). Duas passadas: rótulos, depois bytes."""
    rotulos, pc = {}, 0
    for n, rot, mnem, ops in partir(texto):
        if rot:
            rotulos[rot] = pc
        if mnem == "ORG":
            pc = numero(ops[0], None, n)
        elif mnem:
            pc += tamanho(mnem, ops, n)
    saida, pc, listagem = {}, 0, []

    def emitir(bs, n, texto):
        nonlocal pc
        listagem.append((pc, bytes(bs), texto))
        for b in bs:
            if not 0 <= b <= 255:
                raise ErroDeMontagem(f"linha {n}: byte fora de 0..255")
            saida[pc] = b
            pc += 1

    for n, rot, mnem, ops in partir(texto):
        if mnem is None:
            continue
        rotulo_txt = (rot + ": ") if rot else ""
        texto = rotulo_txt + mnem + (" " + ", ".join(ops) if ops else "")
        if mnem == "ORG":
            pc = numero(ops[0], None, n)
        elif mnem == "DB":
            bs = []
            for o in ops:
                if o.startswith("'") and len(o) > 3:
                    bs += list(o[1:-1].encode("latin-1"))
                else:
                    bs.append(numero(o, rotulos, n))
            emitir(bs, n, texto)
        elif mnem == "MVI":
            d, v = ops[0].upper(), numero(ops[1], rotulos, n)
            emitir([0x06 | (REG[d] << 3), v], n, texto)
        elif mnem == "MOV":
            d, s = ops[0].upper(), ops[1].upper()
            if d == "M" and s == "M":
                raise ErroDeMontagem(f"linha {n}: MOV M,M não existe (76h é HLT)")
            emitir([0x40 | (REG[d] << 3) | REG[s]], n, texto)
        elif mnem in ULA:
            emitir([0x80 | (ULA[mnem] << 3) | REG[ops[0].upper()]], n, texto)
        elif mnem in ULA_IMED:
            emitir([0xC6 | (ULA_IMED[mnem] << 3), numero(ops[0], rotulos, n)], n, texto)
        elif mnem in ("STA", "LDA"):
            a = numero(ops[0], rotulos, n)
            emitir([0x32 if mnem == "STA" else 0x3A, a & 0xFF, a >> 8], n, texto)
        elif mnem in SALTO:
            a = numero(ops[0], rotulos, n)
            emitir([SALTO[mnem], a & 0xFF, a >> 8], n, texto)
        elif mnem in ("INX", "DCX"):
            if ops and ops[0].upper() not in ("H", "HL"):
                raise ErroDeMontagem(f"linha {n}: só o par HL tem INX/DCX nesta máquina")
            emitir([SIMPLES[mnem]], n, texto)
        elif mnem in SIMPLES:
            emitir([SIMPLES[mnem]], n, texto)
        else:
            raise ErroDeMontagem(f"linha {n}: mnemônica '{mnem}' não existe nesta máquina")
    return saida, rotulos, listagem


def binario(saida):
    """Imagem contígua a partir de 0000h até o último byte (buracos = 00h)."""
    if not saida:
        return b""
    fim = max(saida) + 1
    return bytes(saida.get(i, 0) for i in range(fim))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    texto = open(sys.argv[1], encoding="utf-8").read()
    saida, rotulos, listagem = montar(texto)
    for end, bs, txt in listagem:
        print(f"{end:04X}  {' '.join(f'{b:02X}' for b in bs):<20} {txt}")
    print(f"; {len(saida)} bytes, {len(rotulos)} rótulos")
    if len(sys.argv) > 2:
        with open(sys.argv[2], "wb") as f:
            f.write(binario(saida))
    return 0


if __name__ == "__main__":
    sys.exit(main())
