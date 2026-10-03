# A máquina

A especificação da placa que o instrumento desenha. Fixada em 2026-10-02 e
**executável**: tudo o que está aqui roda em `maquina/` (emulador, montador,
o programa Olá, Mundo! e a conferência com controle negativo). Se este texto e
o código discordarem, o código está errado ou o texto está, e a conferência
não escolhe: ela reprova.

Legenda: **[F]** passagem lida no Petzold, *Code* 2ª ed. (a dissecação do
acervo, capítulo indicado) · **[S]** decisão de desenho deste repositório,
assinada e datada · **[D]** derivado por conta, conferível.

## 1. De onde vem

A máquina não foi inventada. É a CPU que o Petzold constrói nos capítulos 20
a 24, um subconjunto do Intel 8080, e só isso [F]:

> In this chapter and the next few chapters, I use the Intel 8080 as a model
> to design my own CPU. But only as a model. My CPU will implement only a
> subset of the 8080. (cap. 21)

O que é nosso, e está marcado [S], são três coisas que o livro descreve mas
não constrói: uma **tela** mapeada em memória, um **teclado** mapeado em
memória, e a **tabela de células** que decide se um byte da tela é uma letra
ou uma cor. Nada mais. A escolha tem um motivo: cada registrador, cada
instrução e cada ciclo desta placa já tem a frase do livro que o sustenta, e
o instrumento pode abrir essa frase ao lado do módulo, como o
abstraction-ladder faz com cada seta.

## 2. Os módulos, e o que cada um faz com o número

| módulo | o que é | o que faz com o número | fonte |
|---|---|---|---|
| registradores A, B, C, D, E, H, L | sete latches de 8 bits | **guardar**: o número espera | [F] cap. 22 |
| A, o acumulador | o registrador que entra na ULA | é sempre a entrada A da ULA | [F] cap. 22 |
| HL, o par | H e L juntos como endereço de 16 bits | um número **aponta** para outro: mem(HL) | [F] cap. 22 |
| PC, o contador de programa | latch de 16 bits | diz qual gaveta será lida como **ordem** agora | [F] cap. 23 |
| IL1, IL2, IL3 | Instruction Latches | guardam os 1 a 3 bytes da instrução em curso | [F] cap. 22 |
| incrementador-decrementador | soma ou subtrai 1 a 16 bits | PC + 1; HL + 1; HL − 1 | [F] cap. 22 |
| ULA | soma, subtrai, E, OU, OU-exclusivo, compara | **operar**: aritmética módulo 256 e lógica bit a bit | [F] cap. 21 |
| flags CY, Z, S | três bits ao lado da ULA | lembram se houve vai-um, zero, ou sinal | [F] cap. 24 |
| RAM | 64 K × 8 | **endereçar**: mem(endereço) = byte | [F] cap. 19 |
| barramento de dados | 8 fios | por onde o byte passa de um módulo a outro | [F] cap. 23 |
| barramento de endereços | 16 fios | por onde o endereço chega à RAM | [F] cap. 23 |
| tela | 264 bytes da RAM, de 8000h a 8107h | cada byte é uma célula: letra ou cor | [S] |
| teclado | 1 byte em 8200h | o código da última tecla; 00h se nenhuma | [S] |

As passagens:

> In summary, the Intel 8080 (and my CPU) defines seven registers referred to
> as A, B, C, D, E, H, and L. (cap. 22)

> These components are connected to each other and to random access memory
> (RAM) through two data busses: an 8-bit data bus that ferries bytes among
> the components, and a 16-bit address bus used for a memory address. (cap. 23)

> A value called the program counter. This is the 16-bit value that accesses
> instructions. It starts at 0000h and sequentially increases until a HLT
> instruction. (cap. 23)

> The use of registers H and L to form a 16-bit memory address is known as
> indirect addressing, and while it might not be obvious at the moment, it
> turns out to be very useful. (cap. 22)

> These are the Carry flag, the Zero flag, and the Sign flag, and they
> indicate, respectively, whether the ALU operation caused a carry, whether
> the result was equal to zero, and whether the high bit of the result was 1,
> indicating a negative two's complement number. (cap. 24)

## 3. O ciclo: busca, depois execução

A unidade de tempo do instrumento é o **ciclo de máquina**, como o livro o
define: em cada ciclo, no máximo um valor no barramento de endereços e um
valor no barramento de dados, e cada valor posto num barramento é salvo em
algum lugar [F]:

> The first step is to address RAM with the program counter value of 0000h
> and store the value 3Eh from memory in Instruction Latch 1. This requires
> four control signals involving both the address bus and data bus. (cap. 23)

A **busca** de cada byte de instrução é um ciclo: PC no barramento de
endereços; RAM no barramento de dados; o byte salvo em IL1, IL2 ou IL3; PC
incrementado. A **execução** gasta um ou dois ciclos. Para a escrita na
memória, que é o ciclo que o instrumento mais vai mostrar [F]:

> Instruction Latches 2 & 3 Enable: Puts the second and third instruction
> bytes on the address bus to address RAM. · Accumulator Enable: Puts the
> value of the accumulator on the data bus. · RAM Write: Writes the value on
> the data bus into memory. (cap. 23, a execução de STA)

É isso que "o dado viaja" quer dizer, com precisão: num ciclo, um módulo
**habilita** a sua saída no barramento e outro módulo **salva** o que está lá.
Nada se desloca. O padrão de 8 bits aparece no barramento e, no mesmo
instante, copia-se no destino. O instrumento anima a cópia; a tese do material
diz por que isso é honesto.

## 4. O conjunto de instruções

Tudo o que a máquina entende. Opcodes do 8080, como o livro os usa [F];
nenhuma mnemônica além destas, e o montador recusa o resto.

| mnemônica | bytes | opcode | ciclos | o que faz | fonte |
|---|---|---|---|---|---|
| MVI r, d8 | 2 | 00 rrr 110 | 3 | o byte seguinte vai para o registrador r | [F] cap. 22 |
| MVI M, d8 | 2 | 36h | 3 | o byte seguinte vai para a memória em [HL] | [F] cap. 22 |
| MOV d, s | 1 | 01 ddd sss | 2 | copia o registrador s em d (M = memória em [HL]) | [F] cap. 22 |
| ADD · ADC · SUB · SBB · ANA · XRA · ORA · CMP r | 1 | 10 fff sss | 3 | A ← A (op) r; CMP só mexe nos flags | [F] cap. 21 e 22 |
| ADI · ACI · SUI · SBI · ANI · XRI · ORI · CPI d8 | 2 | 11 fff 110 | 4 | o mesmo, com o byte seguinte | [F] cap. 22 |
| STA a16 | 3 | 32h | 4 | A vai para a memória no endereço a16 | [F] cap. 22 e 23 |
| LDA a16 | 3 | 3Ah | 4 | A recebe a memória no endereço a16 | [F] cap. 22 |
| INX H · DCX H | 1 | 23h · 2Bh | 2 | HL + 1 · HL − 1 | [F] cap. 22 |
| JMP · JNZ · JZ · JNC · JC · JP · JM a16 | 3 | C3h · C2h · CAh · D2h · DAh · F2h · FAh | 4 | PC ← a16, sempre ou conforme o flag | [F] cap. 24 |
| PCHL | 1 | E9h | 2 | PC ← HL | [F] cap. 24 |
| HLT | 1 | 76h | 2 | a máquina para | [F] cap. 22 |

Os códigos de registrador: B = 000, C = 001, D = 010, E = 011, H = 100,
L = 101, M = 110, A = 111 [F] cap. 22. Os códigos de função da ULA: ADD = 000,
ADC = 001, SUB = 010, SBB = 011, ANA = 100, XRA = 101, ORA = 110, CMP = 111
[F] cap. 21.

**O que esta máquina não tem, de propósito:** CALL e RET, pilha, PUSH e POP,
IN e OUT, interrupções, INR e DCR, deslocamentos. O livro constrói os saltos e
PCHL [F] ("The seven jump instructions and PCHL are fairly easily incorporated
into the timing circuitry", cap. 24) e para aí; os programas desta máquina
vivem de MOV, da ULA e de saltos. É pouco, e é completo [F]:

> All programming languages that support a conditional jump (or something
> equivalent to it) are fundamentally equivalent. These programming languages
> are said to be Turing complete. (cap. 24)

## 5. O mapa de memória

Um único espaço de 64 K, como no livro. A tela e o teclado vivem dentro dele,
pelo caminho que o livro nomeia [F]:

> Memory for the video display occupies the regular memory space of the CPU.
> Other peripherals might do so also. This is called memory-mapped I/O.
> (cap. 25)

| faixa | o que é | bytes | selo |
|---|---|---|---|
| 0000h … | programa e dados; o PC começa em 0000h | até 32 K | [F] cap. 23 |
| 8000h … 8107h | **tela**: 22 linhas × 12 colunas, uma célula por byte, linha a linha | 264 | [S] |
| 8200h | **teclado**: o código da última tecla; escrever ali zera | 1 | [S] |

**O que a gaveta do teclado guarda [S], e o que o livro diz [F].** O capítulo
25 lê o teclado por uma porta, `IN 25h`, e avisa que o código que chega é da
**tecla**, não da letra: "It's tempting to assume that this code is the ASCII
code for the key. But it's neither practical nor desirable to design hardware
that figures out the ASCII code." Nesta máquina a gaveta 8200h entrega
**o número da letra** (a mesma tabela de células), porque o navegador que
hospeda a placa já fez a tradução. É uma simplificação declarada: o degrau
"a tecla vira número" diz isso em nota. O programa consulta a gaveta o tempo
todo, que é o que o livro chama de *polling* [F]: "One approach is for the
program to check the keyboard very frequently. This approach is called
polling."

A célula (linha, coluna) mora em 8000h + 12·linha + coluna [D]. A tela tem
esta forma por três razões [S]:

- a **linha 0** é a faixa de texto: "Olá, Mundo!" tem 11 letras e cabe nas 12
  colunas; no jogo ela mostra o placar;
- as **linhas 1 a 20** são o campo, com 10 colunas úteis (1 a 10) e **paredes**
  nas colunas 0 e 11; a **linha 21** é o chão. Paredes e chão são bytes de
  valor 8, e por isso a colisão é uma só comparação: célula diferente de zero
  é obstáculo, seja parede, chão ou peça. É a ideia da **sentinela** do livro
  [F]: "This 00h value signals to your program that the list is complete.
  Such a value is sometimes called a sentinel." (cap. 24);
- 264 bytes cabem numa única página de memória e numa única tela, para que o
  instrumento mostre a tela inteira como gavetas, ao lado do campo.

## 6. A tabela de células: um byte é letra ou cor

O mesmo byte, duas leituras. É o degrau 6 da página (número lido como ordem)
acontecendo de novo na tela.

| valor | o que a tela mostra | selo |
|---|---|---|
| 00h | vazio | [S] |
| 01h … 07h | as sete cores de peça | [S] |
| 08h | parede e chão | [S] |
| 20h … 7Eh | as letras do ASCII | [F] cap. 13 |
| A0h … FFh | as letras acentuadas: os primeiros 256 códigos do Unicode | [D] |

O **á** é E1h, 225: o mesmo número que a página chama de "o á vale 225". Na
tela ele ocupa **uma** célula, porque a tabela é nossa e tem 256 lugares. No
arquivo que viaja pela web ele ocupa **dois** bytes (C3 A1), porque o UTF-8 é
um código de transporte feito para caber em 128 letras antigas. Mesmo número,
dois códigos, e os dois estão certos: é a diferença entre guardar e
transportar [S]. A página conta os dois.

## 7. Olá, Mundo!, o primeiro programa

A forma é a do exemplo do capítulo 22 [F]:

> Three of these codes—26h, 2Eh, and 36h—are in the table I just showed you.
> The first moves the next byte in memory (which is 00h) into register H. The
> second moves the byte 08h into register L. The registers H and L together
> now form the memory address 0008h. The third instruction code is 36h, which
> means to store the next byte (which is 55h) into memory at [HL]. (cap. 22)

Em `maquina/programas/ola-mundo.asm`, montado à mão e pelo montador, com os
dois concordando byte a byte (a conferência exige):

```
0000  26 80      MVI H, 80h      ; HL ← 8000h, a primeira célula da tela
0002  2E 00      MVI L, 00h
0004  36 4F      MVI M, 'O'      ; 4Fh entra em [8000h]
0006  23         INX H
0007  36 6C      MVI M, 'l'
0009  23         INX H
000A  36 E1      MVI M, 'á'      ; um byte só: 225
000C  23         INX H
000D  36 2C      MVI M, ','
000F  23         INX H
0010  36 20      MVI M, ' '      ; o espaço também é uma letra
0012  23         INX H
0013  36 4D      MVI M, 'M'
0015  23         INX H
0016  36 75      MVI M, 'u'
0018  23         INX H
0019  36 6E      MVI M, 'n'
001B  23         INX H
001C  36 64      MVI M, 'd'
001E  23         INX H
001F  36 6F      MVI M, 'o'
0021  23         INX H
0022  36 21      MVI M, '!'
0024  76         HLT
```

**37 bytes, 24 instruções, 61 ciclos**, e a máquina para com a frase na
linha 0 da tela [D]. Sem laço, de propósito: o primeiro programa é uma linha
reta, para que cada letra seja um evento próprio no traço.

O traço da primeira letra, como o emulador o grava:

```
ciclo  fase       endereço (de)   dado (de → para)    nota
    7  busca      0004 (PC)       36 (RAM → IL1)
    8  busca      0005 (PC)       4F (RAM → IL2)
    9  execução   8000 (HL)       4F (IL2 → RAM)      MVI M: escreve em [HL]
   10  busca      0006 (PC)       23 (RAM → IL1)
   11  execução   8000 (HL)                           INX HL → HL = 8001
```

É o ciclo 9 que o instrumento anima: o byte 4Fh, que é a letra O, sai do
Instruction Latch 2, aparece no barramento de dados, e é salvo na RAM no
endereço que HL pôs no barramento de endereços. Onze vezes, uma por letra. No
jogo, a cor da peça fará exatamente este ciclo.

## 8. O traço, e os dois relógios

Cada ciclo grava um registro com: número do ciclo; número da instrução; fase
(busca ou execução); o endereço no barramento de endereços e **de onde veio**
(PC, HL, IL2+IL3); o dado no barramento de dados, **de onde veio** e **para
onde foi** (RAM, IL1, IL2, um registrador, a entrada B da ULA, a saída da
ULA); PC, os sete registradores, HL e os flags depois do ciclo; e uma nota [S].

Os dois relógios: o jogo roda no emulador em velocidade cheia e o traço fica
num anel de memória. Ao pausar, a placa reproduz do traço, um ciclo por
segundo ou por clique, esfregável para trás. "Mostrar a última jogada" filtra
o traço pelos ciclos cujo destino é a RAM entre 8000h e 8107h, e anima só o
caminho da cor. A pesquisa da placa diz de onde isso vem.

## 9. Os degraus e os módulos são o mesmo objeto

| degrau da página | módulo da placa | o que se vê no traço |
|---|---|---|
| 1 letra → número | o byte 4Fh em IL2 | o número da letra, já na máquina |
| 2 número → bits | os 8 fios do barramento de dados | 01001111 aceso e apagado |
| 3 corrente → bit | um fio do barramento, com o medidor de limiar | a tensão e o símbolo que ela vira |
| 4 conta e lembrança | ULA e registradores | ADD, CMP, e o byte que espera em A |
| 5 endereço | HL no barramento de endereços, a RAM | mem(8000h) recebe 4Fh |
| 6 número → ordem | PC, IL1, e o decodificador | 36h lido como "escreva em [HL]" |
| 7 palavras → ordens | o montador, fora da placa | MVI M, 'O' virou 36 4F |
| 8 ordem → luz | a tela, lendo os 264 bytes | a célula 0 mostra O |

Cada degrau ganha o botão "ver na placa", que toca o trecho do traço daquele
degrau; cada módulo da placa abre o degrau correspondente.

## 10. Os três programas

**1. Olá, Mundo!** (acima): ROM → barramento → tela. Pronto e conferido.

**2. Eco**: o que você digita aparece. Pronto e conferido em
`maquina/programas/eco.asm`, com um roteiro de três teclas ao lado
(`eco.roteiro.json`), que a conferência usa: a linha 1 da tela diz "Olá", cada
tecla faz teclado → A → RAM[HL], e a gaveta é zerada depois de cada uma. Na
placa, o modo ao vivo deixa você digitar, e toca só a última jogada:

```
        MVI H, 80h
        MVI L, 0Ch          ; linha 1 da tela
Espera: LDA 8200h           ; o registrador do teclado
        CPI 00h
        JZ Espera           ; nada apertado: volta
        MOV M, A            ; a tecla vira célula
        INX H
        MVI A, 00h
        STA 8200h           ; limpa o registrador
        JMP Espera
```

É o primeiro laço, e o primeiro caminho de **entrada**: teclado → A → tela.
Fecha o buraco "do teclado ao número" declarado na página.

**3. O jogo**: a peça cai, gira, colide, apaga linha. Precisa do que a
máquina já tem: contadores em registradores (a gravidade é um contador que o
laço decrementa, como o exemplo do cap. 24), CPI e JZ para a colisão (célula
diferente de zero), MOV M e INX H para desenhar, e um gerador de números para
a próxima peça, feito com XRA e ADD (dobrar um registrador somando-o a si
mesmo é o deslocamento do cap. 24). Sem CALL, as rotinas se encadeiam por
JMP; estimativa de 600 a 2.000 instruções, a conferir escrevendo.

## 11. Os três mostradores

- **o medidor de limiar**, num fio do barramento de dados: a tensão, e o
  símbolo que ela vira. O limiar da página (2 volts ou mais é 1; 0,8 volt ou
  menos é 0) é a convenção TTL, **sem passagem lida ainda**: fica como ofício
  até ter fonte;
- **a onda de estados** no barramento: no ciclo, o padrão aparece nos 8 fios
  e copia-se no destino. Nada anda;
- **o rótulo matemático** em cada módulo: mem(HL) na RAM, (A + B) mod 256 na
  ULA, próximo = passo(PC, A, mem) no controle, cor(x, y) na tela. São as
  mesmas expressões dos degraus, com o mesmo "lê-se".

## 12. O que está lido, o que é nosso, e o que falta

- **Lido [F]**: os sete registradores, os dois barramentos, PC, os Instruction
  Latches, o incrementador-decrementador, a ULA e os flags, o ciclo de busca e
  execução, cada opcode da tabela, E/S mapeada em memória, a sentinela.
- **Nosso [S]**: a tela de 12 × 22 em 8000h, o teclado em 8200h, a tabela de
  células, as paredes como sentinela, o formato do traço, o Olá, Mundo! em
  linha reta.
- **Derivado [D]**: os 37 bytes e os 61 ciclos; o endereço de cada célula; o
  á como 225 em um byte.
- **Falta**: a fonte do limiar TTL; os códigos de tecla (o livro avisa que não
  são ASCII: cap. 25); o jogo em assembly; a placa desenhada.

## 13. As conferências

Há **duas implementações** desta especificação: `maquina/maquina.py`, a
referência, e `maquina/maquina.js`, a que roda no navegador; e dois
montadores, `montar.py` e `montar.js`. `python3 maquina/conferir_equivalencia.py`
exige que, para cada programa de `programas/`, os dois montadores deem os
mesmos bytes e as duas máquinas deem o **mesmo traço, ciclo a ciclo**,
inclusive para um programa quebrado; que os dois recusem CALL; e que um traço
com um único campo alterado seja acusado. O programa `conjunto-inteiro.asm`
existe para isso: passa por todas as instruções, os sete saltos tomados e não
tomados, as oito operações da ULA nas duas formas, e os valores esperados
estão anotados à mão ao lado de cada linha.

`python3 maquina/conferir_maquina.py` prova, com controle negativo: montador
e mão concordam nos 37 bytes; a tela diz "Olá, Mundo!"; cada letra chegou por
um ciclo cujo dado saiu de IL2 e cujo endereço veio de HL; um programa com um
único opcode trocado (o primeiro INX H virado em DCX H) **não** produz a frase
e é acusado; e o montador recusa CALL, que esta máquina não tem.
