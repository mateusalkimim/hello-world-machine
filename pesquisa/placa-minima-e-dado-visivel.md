# Placa mínima, dado visível

Pesquisa de 2026-10-02 para o instrumento deste repositório: um jogo de blocos
que cai, jogável, e acima dele uma placa virtual em que se vê o dado (a cor da
peça) sair do registrador, atravessar o barramento e chegar à memória de
vídeo. Três perguntas: já existe? qual é a placa mais simples necessária? o
que a torna legível a quem não sabe nada?

Legenda: **[F]** fonte lida · **[S]** síntese do autor. Licenças só quando o
texto foi visto; senão "não achada".

## 1. Já existe?

Não como um todo. Os projetos do mundo ocupam três cantos disjuntos.

**Jogo real + tabela de registradores.** O emulador de CPU do Nand2Tetris
roda Pong (e Tetris, feito por alunos em Jack) com A, D, PC, ROM, RAM e tela
visíveis; TypeScript, sem servidor, licença MIT [F]. Mostra tabelas que mudam;
não desenha placa nem dado em trânsito [S].
<https://nand2tetris.github.io/web-ide/> · <https://github.com/nand2tetris/web-ide>

**Dado animado no barramento + programa de brinquedo.** O Little Man Computer
de Peter Higginson move "blobs" pelos barramentos no ciclo de busca e execução
[F], e o CPU Visual Simulator anima o dado entre RAM, registradores e ULA [F].
É a gramática visual certa, com cem células e sem jogo; licenças não achadas.
FetchCPU-Pocho faz o mesmo com animação mais pobre, MIT [F].
<https://peterhigginson.co.uk/LMC> · <https://github.com/jcancelli/cpu-visual-simulator> · <https://github.com/Pochonski/fetchcpu-pocho>

**Corrente animada + circuito sem programa.** O simulador de Falstad desenha
pontos em movimento proporcionais à corrente e cor por tensão [F]: é a
estética "corrente navegando". GPL-2.0; o SAP-1 de Ben Eater montado nele roda
a cerca de 200 Hz com 16 bytes [F]. CircuitVerse (MIT), Digital (GPL-3),
Logisim-evolution (GPL-3), Turing Complete (comercial) e Digital Logic Sim
(MIT) mostram o **estado** do fio por cor; nenhum anima o deslocamento [S].
<https://www.falstad.com/circuit/> · <https://github.com/tomwhite/8-bit-computer>

**Jogo + hardware ao lado.** WasmBoy e Mesen expõem registradores e memória
de vídeo do Game Boy e do NES ao lado do jogo [F]; o visual6502 roda programas
reais a nível de transistor, com 1.725 fios e 3.510 chaves [F], ilegível e
com geometria sob licença não comercial, incompatível com MIT [F].
<https://github.com/torch2424/wasmboy> · <https://github.com/trebonian/visual6502>

**O buraco [S]:** não existe site estático em que um jogo jogável roda e, ao
mesmo tempo, uma placa desenhada mostra o dado em trânsito. O cruzamento dos
três cantos está vazio.

## 2. A placa mais simples necessária

| candidata | memória | tela | cor por célula | placa a desenhar | roda o jogo | veredito [S] |
|---|---|---|---|---|---|---|
| CHIP-8 (1977) | 4 KiB, 16 registradores | 64 × 32, monocromática | não | nenhuma: é máquina virtual | sim | programa certo, placa nenhuma |
| Hack (Nand2Tetris) | 32K ROM + 32K RAM, 16 bits | 512 × 256, 1 bit | não | 8 blocos de 16 bits | sim, saturando a ROM | milhões de instruções por segundo; replay inviável |
| SAP-1 (Ben Eater) | 16 bytes | 7 segmentos | — | 10 módulos, 1 barramento com LEDs | não | padrão de legibilidade; pequeno demais |
| Gigatron TTL | 32 KB RAM, 930 portas | 160 × 120, 1 byte por pixel | sim | 8 blocos | sim | jogo sob interpretador e vídeo por software; duas camadas |
| Game Boy / 6502 | 64 KB | 160 × 144, 4 tons | não | milhares de transistores | sim, ROM proprietária | ordens de grandeza a mais |
| **CPU própria, 8 bits** | 256 B RAM + ROM de programa + vídeo 10 × 20 | 10 × 20 células | **sim, 1 byte = cor** | 10 módulos + vídeo | sim, em assembly próprio | **recomendada** |

Fontes: CHIP-8 <https://en.wikipedia.org/wiki/CHIP-8> · Hack
<https://en.wikipedia.org/wiki/Hack_computer> e `Tetris.jack` com 32.654
instruções, 114 abaixo do teto [F] <https://github.com/leocassarani/Tetris.jack> ·
SAP <https://en.wikipedia.org/wiki/Simple-As-Possible_computer> · Gigatron
<https://en.wikipedia.org/wiki/Gigatron_TTL> · um jogo de blocos em 247 bytes
de x86 [F] <https://github.com/pellsson/tinytris>.

**Recomendação [S]:** o SAP-1 de Ben Eater estendido. Barramento único de 8
bits; módulos PC, MAR, RAM de 256 bytes, ROM de programa separada (2 a 4 KB,
16 instruções), A, B, ULA, FLAGS, IR com controle, registrador de teclado, e
uma memória de vídeo de 10 × 20 bytes em que cada byte é a cor da célula. É a
única opção em que a cor é um byte que de fato sai de um registrador,
atravessa o barramento e entra na memória de vídeo. Emulador de 150 a 300
linhas de JavaScript; canvas 2D puro sustenta 100 fios e quatro partículas a
60 quadros por segundo sem biblioteca [F]
<https://wildgames.io/blog/webgl-vs-canvas2d>. Licença limpa por construção.

## 3. Os dois relógios

Um jogo jogável roda milhares de instruções por segundo; ver o dado andar pede
uma ou duas por segundo. A receita é a dos depuradores de emulador e dos
replays de jogo [F]: a simulação é determinística, o jogo roda cheio e grava
o **traço** de cada instrução (registradores antes e depois, valor no
barramento, módulo de origem e destino); ao pausar, a placa reproduz do traço
em câmera lenta, esfregável para trás. O 8bitworkshop tem "step backwards" e
gravação com retrocesso por quadro e por ciclo [F]
<https://8bitworkshop.com/docs/docs/ide.html>; o Python Tutor grava tudo e
exibe depois, com passo à frente e atrás [F]
<https://pg.ucsd.edu/publications/Online-Python-Tutor-web-based-program-visualization_SIGCSE-2013.pdf>;
Bret Victor pede o tempo visível e esfregável [F]
<https://worrydream.com/LearnableProgramming/>.

"Mostrar a última jogada" filtra o traço pelas escritas na memória de vídeo e
anima só o caminho da cor. Uma queda de peça são cerca de 100 a 300 registros
[S]. A cinco instruções por segundo uma queda levaria minutos: esse modo é
obrigatório, não opcional.

## 4. O que torna legível

1. **Um ator por fluxo, com o valor escrito nele.** Human Resource Machine: o
   funcionário segura exatamente uma caixa com um número [F]
   <https://tomorrowcorporation.com/humanresourcemachine>; TIS-100 mostra o
   valor passando de nó a nó [F].
2. **No máximo quatro coisas em movimento por quadro.** Pylyshyn, rastreio de
   múltiplos objetos, "around 4" [F]
   <http://www.scholarpedia.org/article/Multiple_object_tracking>; Alvarez e
   Franconeri 2007: a capacidade cai com a velocidade [F]
   <https://jov.arvojournals.org/article.aspx?articleid=2121950>.
3. **Cor é estado, não enfeite.** Três cores de sinal (0, 1, erro), uma cor
   por tipo de barramento, fio inativo em cinza, fundo escuro. Convenção do
   Logisim [F] <https://cburch.com/logisim/docs/2.1.0/guide/bundles/colors.html>;
   Falstad; Virtual Circuit Board.
4. **Menor diferença eficaz.** Só o que anda brilha; o resto esmaece. Tufte
   [F] <https://boxesandarrows.com/three-lessons-from-tufte-special-deliverable-6/>.
5. **Animação de cerca de um segundo, com aceleração suave, trajeto
   previsível e sem oclusão.** Heer e Robertson 2007 [F]
   <https://idl.cs.washington.edu/files/2007-AnimatedTransitions-InfoVis.pdf>.
6. **Velocidade do modelo e velocidade da animação em controles separados.**
   Falstad tem dois controles, um para a simulação e outro para os pontos [F]
   <https://www.falstad.com/circuit/doc/overview.html>; Ben Eater, relógio
   astável ou manual [F] <https://eater.net/8bit/clock>.
7. **Três marchas fixas, passo a passo e ponto de parada.** TIS-100 (50 Hz,
   5.000 Hz, passo) [F]; EXAPUNKS ("run em velocidade assistível" e avanço
   rápido separados) [F] <https://lparchive.org/EXAPUNKS/Update%2002/>.
8. **Rastro de tempo.** Ponto por instrução na linha do tempo, quadro anterior
   em fantasma. Victor, "make time visible" [F].
9. **Código e mundo na mesma tela; cada edição com efeito visível.** The
   Farmer Was Replaced [F] <https://store.steampowered.com/app/2060160/>;
   a velocidade ali é prêmio que se compra, não padrão [F]
   <https://thefarmerwasreplaced.wiki.gg/wiki/Unlocks>.
10. **Mayer: sinalização e segmentação.** Segmentos curtos, no ritmo do
    aprendiz, melhoram retenção e transferência [F]
    <https://pmc.ncbi.nlm.nih.gov/articles/PMC9762622/>.

## 5. Os três mostradores

Com a tese fixada em [`espinha-matematica.md`](espinha-matematica.md), a placa
mostra três coisas, não uma:

- o **medidor de limiar**, onde a tensão vira bit (um intervalo inteiro de
  tensões vira um símbolo só);
- a **onda de estados** pelo barramento, honesta: nada anda, o padrão se
  copia de módulo em módulo;
- em cada módulo, o **rótulo da operação matemática** (soma módulo 256,
  estado seguinte, endereço → byte).

A eletrônica de cada módulo fica como profundidade, a um clique, apontando
para o abstraction-ladder.

## 6. Riscos

1. "Tetris" é marca registrada; o jogo precisa de nome próprio.
2. Arquitetura própria não tem programa pronto: o jogo tem de ser escrito em
   assembly da máquina nova, estimativa de 600 a 2.000 instruções [S].
3. A cor só "viaja" se a arquitetura obrigar a escrita a passar pelo
   barramento: nenhum atalho de cópia direta no emulador.
4. Mais de quatro partículas vivas, e o leitor perde o fio.
5. CHIP-8 como atalho: licença ambígua da ROM histórica e nenhuma placa para
   mostrar.
