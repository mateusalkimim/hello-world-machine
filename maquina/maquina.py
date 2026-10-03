#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A máquina: a CPU que o Petzold constrói em *Code* (2ª ed., caps. 20 a 24),
com uma tela e um teclado mapeados em memória (cap. 25).

Este emulador é a ESPECIFICAÇÃO EXECUTÁVEL. Ele não corre rápido; ele conta
tudo. Cada ciclo de máquina registra o que esteve no barramento de endereços,
o que esteve no barramento de dados, de onde veio e para onde foi — porque o
instrumento deste repositório precisa mostrar o dado em trânsito, e o traço é a fonte
da animação (os dois relógios: o jogo roda cheio, a placa reproduz do traço).

O modelo de ciclo segue o cap. 23: a busca de cada byte de instrução é um
ciclo (PC no barramento de endereços; RAM no barramento de dados; byte salvo no
Instruction Latch; PC incrementado), e a execução gasta um ou dois ciclos
conforme a instrução.

Uso:  python3 maquina.py programa.bin [--traco] [--json]
      --json imprime o estado final e o traço em JSON (para a conferência de equivalência)
"""
import json
import sys

VIDEO_INICIO, VIDEO_COLUNAS, VIDEO_LINHAS = 0x8000, 12, 22
VIDEO_FIM = VIDEO_INICIO + VIDEO_COLUNAS * VIDEO_LINHAS      # exclusivo
TECLADO = 0x8200

NOME_REG = ["B", "C", "D", "E", "H", "L", "M", "A"]
NOME_ULA = ["ADD", "ADC", "SUB", "SBB", "ANA", "XRA", "ORA", "CMP"]


class Maquina:
    def __init__(self, imagem=b"", traco=False):
        self.mem = bytearray(65536)
        self.mem[:len(imagem)] = imagem
        self.reg = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "H": 0, "L": 0}
        self.pc = 0
        self.cy = self.z = self.s = 0
        self.il = [0, 0, 0]           # Instruction Latches 1, 2, 3
        self.parada = False
        self.ciclos = 0
        self.instrucoes = 0
        self.traco = [] if traco else None
        self.tecla = 0

    # --- a memória, com os dois periféricos mapeados -----------------------
    def ler(self, end):
        if end == TECLADO:
            return self.tecla
        return self.mem[end]

    def escrever(self, end, valor):
        if end == TECLADO:
            self.tecla = 0          # escrever no registrador do teclado o limpa
            return
        self.mem[end] = valor & 0xFF

    def apertar(self, codigo):
        self.tecla = codigo & 0xFF

    @property
    def hl(self):
        return (self.reg["H"] << 8) | self.reg["L"]

    def por_hl(self, v):
        self.reg["H"], self.reg["L"] = (v >> 8) & 0xFF, v & 0xFF

    # --- um ciclo de máquina: o que esteve em cada barramento ---------------
    def ciclo(self, fase, end, end_de, dado, dado_de, dado_para, nota=""):
        self.ciclos += 1
        if self.traco is not None:
            self.traco.append(dict(
                n=self.ciclos, instrucao=self.instrucoes, fase=fase,
                endereco=end, endereco_de=end_de,
                dado=dado, dado_de=dado_de, dado_para=dado_para,
                pc=self.pc, a=self.reg["A"], hl=self.hl,
                flags=f"{'C' if self.cy else '-'}{'Z' if self.z else '-'}{'S' if self.s else '-'}",
                nota=nota))

    def buscar(self, latch):
        """Um byte de instrução: PC → endereços; RAM → dados → Instruction Latch; PC+1."""
        b = self.ler(self.pc)
        self.il[latch] = b
        self.ciclo("busca", self.pc, "PC", b, "RAM", f"IL{latch + 1}")
        self.pc = (self.pc + 1) & 0xFFFF
        return b

    # --- a ULA: as oito operações, com os três flags do cap. 21 -------------
    def ula(self, f, b):
        a = self.reg["A"]
        if f == 0:   r = a + b
        elif f == 1: r = a + b + self.cy
        elif f == 2: r = a - b
        elif f == 3: r = a - b - self.cy
        elif f == 4: r = a & b
        elif f == 5: r = a ^ b
        elif f == 6: r = a | b
        else:        r = a - b                       # CMP: compara, não guarda
        if f in (0, 1):
            self.cy = 1 if r > 0xFF else 0
        elif f in (2, 3, 7):
            self.cy = 1 if r < 0 else 0
        else:
            self.cy = 0
        r &= 0xFF
        self.z = 1 if r == 0 else 0
        self.s = 1 if r & 0x80 else 0
        if f != 7:
            self.reg["A"] = r
        return r

    # --- uma instrução inteira ---------------------------------------------
    def passo(self):
        if self.parada:
            return False
        self.instrucoes += 1
        op = self.buscar(0)
        ddd, sss = (op >> 3) & 7, op & 7

        if op == 0x76:                                        # HLT
            self.ciclo("execução", None, "", None, "", "", "HLT: a máquina para")
            self.parada = True
            return False

        if op & 0xC7 == 0x06:                                 # MVI r,d8 / MVI M,d8
            v = self.buscar(1)
            if ddd == 6:
                self.escrever(self.hl, v)
                self.ciclo("execução", self.hl, "HL", v, "IL2", "RAM", "MVI M: escreve em [HL]")
            else:
                self.reg[NOME_REG[ddd]] = v
                self.ciclo("execução", None, "", v, "IL2", NOME_REG[ddd], f"MVI {NOME_REG[ddd]}")
            return True

        if op & 0xC0 == 0x40:                                 # MOV d,s
            if sss == 6:
                v = self.ler(self.hl)
                self.reg[NOME_REG[ddd]] = v
                self.ciclo("execução", self.hl, "HL", v, "RAM", NOME_REG[ddd], f"MOV {NOME_REG[ddd]},M")
            elif ddd == 6:
                v = self.reg[NOME_REG[sss]]
                self.escrever(self.hl, v)
                self.ciclo("execução", self.hl, "HL", v, NOME_REG[sss], "RAM", f"MOV M,{NOME_REG[sss]}")
            else:
                v = self.reg[NOME_REG[sss]]
                self.reg[NOME_REG[ddd]] = v
                self.ciclo("execução", None, "", v, NOME_REG[sss], NOME_REG[ddd], f"MOV {NOME_REG[ddd]},{NOME_REG[sss]}")
            return True

        if op & 0xC0 == 0x80:                                 # ADD r … CMP r
            f = ddd
            if sss == 6:
                b = self.ler(self.hl)
                self.ciclo("execução", self.hl, "HL", b, "RAM", "ULA.B", f"{NOME_ULA[f]} M")
            else:
                b = self.reg[NOME_REG[sss]]
                self.ciclo("execução", None, "", b, NOME_REG[sss], "ULA.B", f"{NOME_ULA[f]} {NOME_REG[sss]}")
            r = self.ula(f, b)
            self.ciclo("execução", None, "", r, "ULA", "A" if f != 7 else "flags", f"resultado da ULA, flags {self.flags()}")
            return True

        if op & 0xC7 == 0xC6:                                 # ADI … CPI
            f = ddd
            b = self.buscar(1)
            self.ciclo("execução", None, "", b, "IL2", "ULA.B", f"{NOME_ULA[f]}I")
            r = self.ula(f, b)
            self.ciclo("execução", None, "", r, "ULA", "A" if f != 7 else "flags", f"resultado da ULA, flags {self.flags()}")
            return True

        if op in (0x32, 0x3A):                                # STA / LDA a16
            lo, hi = self.buscar(1), self.buscar(2)
            end = (hi << 8) | lo
            if op == 0x32:
                self.escrever(end, self.reg["A"])
                self.ciclo("execução", end, "IL2+IL3", self.reg["A"], "A", "RAM", "STA")
            else:
                v = self.ler(end)
                self.reg["A"] = v
                self.ciclo("execução", end, "IL2+IL3", v, "RAM" if end != TECLADO else "teclado", "A", "LDA")
            return True

        if op in (0x23, 0x2B):                                # INX H / DCX H
            antes = self.hl
            self.por_hl((antes + (1 if op == 0x23 else -1)) & 0xFFFF)
            self.ciclo("execução", antes, "HL", None, "", "", f"{'INX' if op == 0x23 else 'DCX'} HL → incrementador-decrementador → HL = {self.hl:04X}")
            return True

        if op == 0xE9:                                        # PCHL
            self.ciclo("execução", self.hl, "HL", None, "", "", "PCHL: HL vai para o PC")
            self.pc = self.hl
            return True

        if op & 0xC7 == 0xC2 or op == 0xC3:                   # saltos
            lo, hi = self.buscar(1), self.buscar(2)
            alvo = (hi << 8) | lo
            cond = {0xC3: True, 0xC2: not self.z, 0xCA: bool(self.z),
                    0xD2: not self.cy, 0xDA: bool(self.cy),
                    0xF2: not self.s, 0xFA: bool(self.s)}.get(op)
            if cond is None:
                raise ValueError(f"opcode {op:02X} não existe nesta máquina (PC={self.pc - 3:04X})")
            if cond:
                self.ciclo("execução", alvo, "IL2+IL3", None, "", "", f"salto tomado: PC = {alvo:04X}")
                self.pc = alvo
            else:
                self.ciclo("execução", None, "", None, "", "", "salto não tomado")
            return True

        raise ValueError(f"opcode {op:02X} não existe nesta máquina (PC={self.pc - 1:04X})")

    def flags(self):
        return f"{'C' if self.cy else '-'}{'Z' if self.z else '-'}{'S' if self.s else '-'}"

    def rodar(self, max_instrucoes=1_000_000):
        while not self.parada and self.instrucoes < max_instrucoes:
            self.passo()
        return self.instrucoes

    # --- a tela: cada byte de vídeo vira um glifo (letra) ou uma cor --------
    def tela(self):
        linhas = []
        for r in range(VIDEO_LINHAS):
            base = VIDEO_INICIO + r * VIDEO_COLUNAS
            linhas.append("".join(celula(self.mem[base + c]) for c in range(VIDEO_COLUNAS)))
        return linhas


def estado(m):
    """O estado final e o traço, em forma comparável entre implementações."""
    return dict(
        instrucoes=m.instrucoes, ciclos=m.ciclos, parada=m.parada,
        reg=dict(m.reg), pc=m.pc, flags=m.flags(), hl=m.hl,
        tela=m.tela(), traco=m.traco or [])


def celula(b):
    """A tabela de células: o mesmo byte é letra ou cor, conforme a faixa."""
    if b == 0:
        return "·"
    if 1 <= b <= 7:
        return "▮"                      # as sete cores de peça (a cor vem do visor)
    if b == 8:
        return "█"                      # parede
    if 0x20 <= b <= 0x7E or 0xA0 <= b <= 0xFF:
        return bytes([b]).decode("latin-1")   # os 256 primeiros códigos do Unicode
    return "?"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    imagem = open(sys.argv[1], "rb").read()
    m = Maquina(imagem, traco=("--traco" in sys.argv) or ("--json" in sys.argv))
    n = m.rodar()
    if "--json" in sys.argv:
        print(json.dumps(estado(m), ensure_ascii=False, sort_keys=True))
        return 0
    print(f"{n} instruções, {m.ciclos} ciclos, {'parou em HLT' if m.parada else 'não parou'}")
    print("A=%02X B=%02X C=%02X D=%02X E=%02X HL=%04X PC=%04X flags=%s" % (
        m.reg["A"], m.reg["B"], m.reg["C"], m.reg["D"], m.reg["E"], m.hl, m.pc, m.flags()))
    for r, linha in enumerate(m.tela()):
        if linha.strip("·"):
            print(f"vídeo linha {r:2d}: {linha}")
    if m.traco:
        print("ciclo  fase       endereço(de)        dado(de → para)     nota")
        for t in m.traco:
            end = f"{t['endereco']:04X}({t['endereco_de']})" if t["endereco"] is not None else ""
            dado = f"{t['dado']:02X}({t['dado_de']} → {t['dado_para']})" if t["dado"] is not None else ""
            print(f"{t['n']:5d}  {t['fase']:<9}  {end:<18}  {dado:<18}  {t['nota']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
