# A placa em planta

A especificação do desenho que o instrumento faz da máquina. Fixada em
2026-10-02, depois da pesquisa sobre placa mínima e dado visível, e da decisão
por canvas 2D em planta: lê-se de cima, como um mapa, e o olho tem no máximo
quatro coisas para seguir.

## O que a placa é

Um desenho fixo da máquina de `a-maquina.md`, no arranjo que o Petzold usa no
capítulo 23: **dois trilhos horizontais**, o barramento de endereços em cima e
o de dados embaixo, e os módulos entre eles, cada um ligado ao trilho que lhe
cabe por uma haste. O traço da máquina (um registro por ciclo) é o que anima:
em cada ciclo, uma haste de origem acende, o trilho mostra o valor, e a haste
de destino acende. Nada se desloca; o padrão aparece e copia-se.

## Os módulos, da esquerda para a direita

| módulo | liga a | mostra | rótulo matemático |
|---|---|---|---|
| PC | endereços | o valor de 16 bits | qual gaveta é ordem |
| incrementador-decrementador | endereços | +1 · −1 | |
| instrução (IL1, IL2, IL3) | dados; IL2+IL3 a endereços | os três bytes | a ordem, byte a byte |
| registradores A B C D E H L | dados; HL a endereços | os sete bytes | guardar · mem(HL) aponta |
| ULA | dados | entrada A, entrada B, saída, flags C Z S | (A + B) mod 256 |
| RAM | endereços e dados | uma janela de gavetas em volta do endereço atual | mem(endereço) = byte |
| tela | lê a RAM de 8000h a 8107h | a grade de 12 × 22 células | cor(x, y) |

O teclado (8200h) é uma gaveta da RAM e aparece na janela dela quando lido.

## O que acende num ciclo

Cada registro do traço diz de onde veio o endereço e de onde veio e para onde
foi o dado. A placa traduz isso em quatro coisas, e só quatro:

1. a haste da **origem do dado** e o módulo dela;
2. o **trilho de dados**, com oito pontos acesos ou apagados: os bits;
3. a haste do **destino do dado** e a célula que recebeu;
4. o **trilho de endereços**, com o valor em hexadecimal, da origem
   (PC, HL ou IL2+IL3) ao destino (RAM, ou o incrementador, ou o PC num salto).

Tudo o mais fica apagado, na cor de linha. É a menor diferença eficaz: só o
que muda brilha.

## O tempo

Um ciclo é uma animação de três fases, com aceleração suave: a origem acende;
o trilho mostra o padrão; o destino recebe. Parado (passo a passo), as três
fases ficam acesas ao mesmo tempo, para leitura. Três marchas: um ciclo por
segundo, quatro, vinte. Setas do teclado andam um ciclo; a barra esfrega. A
velocidade da animação e a da máquina são controles separados: a máquina já
rodou inteira antes de a placa começar, e o traço é o que se toca.

## Código e mundo na mesma tela

A listagem do programa fica ao lado da placa, com a instrução em curso
destacada; a tela da máquina fica dentro da placa, lendo a RAM. Quem lê vê a
linha de montagem, os bytes que ela virou, o ciclo que os move e a célula que
acende, sem trocar de tela.

## Cor é estado

As cores saem dos mesmos tokens da página (claro e escuro): endereço em azul,
dado em bronze, apagado na cor de linha, texto na cor de tinta. Um bit aceso é
o token de bit 1; apagado, o de bit 0. Nenhuma cor é decoração.

## Conferência

`conferir_placa.py` exige que todo nome de origem e destino que apareça no
traço de cada programa tenha um módulo desenhado (um nome sem caixa é um ciclo
invisível), que o roteiro em JavaScript passe no verificador de sintaxe do
node, e que um registro com um nome inventado seja recusado. A medida da
tela em três resoluções é a do verificador de página herdado da escada.
