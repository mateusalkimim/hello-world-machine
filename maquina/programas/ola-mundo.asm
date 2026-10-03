; Olá, Mundo! — o primeiro programa desta máquina.
;
; Escreve a frase na primeira linha da tela, uma letra por vez. Cada letra faz
; o mesmo caminho: sai do byte seguinte à instrução (Instruction Latch 2),
; atravessa o barramento de dados, e entra na memória de vídeo no endereço que
; o par HL aponta. Depois HL avança uma casa. É o caminho que a cor da peça
; vai fazer no jogo.
;
; A forma é a do cap. 22 do Petzold: MVI H / MVI L apontam, MVI M escreve em
; [HL]. Sem laço de propósito: o primeiro programa é uma linha reta, para que
; cada letra apareça no traço como um evento próprio.

        ORG 0000h

        MVI H, 80h          ; HL ← 8000h: a primeira célula da tela
        MVI L, 00h

        MVI M, 'O'          ; 4Fh entra em [8000h]
        INX H
        MVI M, 'l'          ; 6Ch
        INX H
        MVI M, 'á'          ; E1h — um byte só: a célula fala o código Unicode
        INX H
        MVI M, ','          ; 2Ch
        INX H
        MVI M, ' '          ; 20h — o espaço também é uma letra
        INX H
        MVI M, 'M'          ; 4Dh
        INX H
        MVI M, 'u'          ; 75h
        INX H
        MVI M, 'n'          ; 6Eh
        INX H
        MVI M, 'd'          ; 64h
        INX H
        MVI M, 'o'          ; 6Fh
        INX H
        MVI M, '!'          ; 21h

        HLT                 ; 76h: a máquina para, e a frase fica na tela
