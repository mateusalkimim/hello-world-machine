; Eco — o que você digita aparece na tela.
;
; O primeiro laço desta máquina, e o primeiro caminho de ENTRADA: a tecla vira
; número na gaveta 8200h, o número vai para o acumulador, e do acumulador para
; a tela. O programa pergunta à gaveta o tempo todo e quase sempre encontra
; zero (ninguém apertou): é o que o Petzold chama de polling, no cap. 25.
; Quando encontra um código, copia para a célula que HL aponta, avança HL, e
; zera a gaveta, para não ler a mesma tecla duas vezes.
;
; Não para nunca: a máquina fica à espera. Quem para é quem fecha a página.

        ORG 0000h

        MVI H, 80h          ; HL ← 800Ch: linha 1 da tela (a linha 0 é da faixa)
        MVI L, 0Ch

Espera: LDA 8200h           ; A ← a gaveta do teclado
        CPI 00h             ; apertaram algo?
        JZ Espera           ; não: pergunta de novo

        MOV M, A            ; a tecla vira célula em [HL]
        INX H               ; a próxima célula
        MVI A, 00h
        STA 8200h           ; zera a gaveta: a tecla foi consumida
        JMP Espera
