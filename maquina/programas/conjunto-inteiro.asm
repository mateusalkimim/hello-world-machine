; Conjunto inteiro — um programa que passa por TODAS as instruções da máquina.
;
; Não ensina nada: serve à conferência de equivalência. Se as duas
; implementações (Python e JavaScript) produzem o mesmo traço para este
; programa, elas concordam em cada instrução, em cada flag e em cada salto,
; tomado e não tomado. O laço do começo é o do cap. 24 do Petzold: somar uma
; lista até a sentinela 00h.

        ORG 0000h

        MVI H, 10h          ; HL ← 1000h, onde mora a lista
        MVI L, 00h
        MVI B, 00h          ; B acumula a soma
Laco:   MOV A, M            ; A ← mem[HL]
        CPI 00h             ; chegou à sentinela?
        JZ Fim              ; sim: sai do laço (salto tomado na 4ª volta)
        ADD B               ; A ← A + B (a última volta tem vai-um)
        MOV B, A
        INX H
        JMP Laco            ; salto incondicional, tomado
Fim:    MOV A, B            ; a soma: 4Fh + 6Ch + E1h = 19Ch → 9Ch com CY
        STA 8000h           ; vai para a tela (célula 0)
        LDA 8000h           ; e volta
        SUI 01h             ; 9Ch − 1 = 9Bh, sem vai-um
        JC Nunca            ; não tomado
        ANI 0Fh             ; 0Bh
        XRI FFh             ; F4h
        ORI 01h             ; F5h
        MOV C, A
        MOV D, C
        MOV E, D            ; C = D = E = F5h
        SBI 00h             ; F5h
        ACI 00h             ; F5h (CY era 0)
        ADC C               ; F5h + F5h = 1EAh → EAh, CY = 1
        SUB D               ; EAh − F5h → F5h, CY = 1 (pediu emprestado)
        SBB E               ; F5h − F5h − 1 → FFh, CY = 1
        ANA C               ; FFh AND F5h = F5h
        XRA D               ; F5h XOR F5h = 00h, Z = 1
        ORA E               ; 00h OR F5h = F5h
        CMP C               ; F5h − F5h: Z = 1, A segue F5h
        JNZ Pula            ; não tomado (Z = 1)
        MVI A, 01h          ; executa: A = 01h
Pula:   DCX H               ; HL = 1002h
        MOV M, A            ; mem[1002h] ← 01h (sobrescreve o E1h da lista)
        JNC Segue           ; tomado (CY = 0 depois de CMP igual)
Nunca:  HLT                 ; nunca chega aqui
Segue:  JM Nunca            ; não tomado (S = 0)
        JP Positivo         ; tomado
        HLT
Positivo:
        MVI H, 00h          ; HL ← 0040h
        MVI L, 40h
        PCHL                ; PC ← HL: pula para o fim

        ORG 0040h
        MVI M, 'X'          ; mem[0040h]: escreve sobre si mesmo, só para passar por MVI M de novo
        HLT

        ORG 1000h
        DB 'Olá', 0         ; a lista: 4Fh 6Ch E1h, e a sentinela
