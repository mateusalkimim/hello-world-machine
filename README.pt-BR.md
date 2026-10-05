<!-- idioma: linha gerada por i18n.py -->
> [!NOTE]
> ### 🌍 **[Read this page in English →](README.md)**

# A máquina do olá, mundo — `hello-world-machine`

**Tudo o que se vê, se lê e se ouve num computador passou por um circuito que
só sabe duas coisas, há corrente ou não há, milhares de vezes por segundo. Esta
página segue uma frase só, "Olá, Mundo!", nessa viagem: da saudação dita no
escuro até a luz que a devolve na tela.** Um degrau por tela; em cada um, o que
esta parte opera no sinal e o que devolve, a matemática que torna isso
possível, uma figura, e a passagem do livro que sustenta o que foi dito.
Nenhum degrau entrou por plausibilidade: **o gerador aborta** se faltar a
citação.

É material para quem não sabe nada. A régua é a folha em branco: uma tese de
até 25 palavras; **as palavras novas explicadas antes de aparecerem** (o que é,
por que existe); uma figura com a palavra nova dentro dela; um parágrafo de até
60; e a passagem do livro atrás de um clique, em "de onde isto vem".

**A página não fala de método.** Selos de procedência, notas, buracos
declarados e a fonte de cada linha do fecho moram aqui e em
[`pesquisa/o-que-falta.md`](pesquisa/o-que-falta.md), gerado pelo gerador; o
leitor da página não precisa deles para aprender. E a folha em branco é
propriedade de construção: o gerador recusa uma palavra técnica antes do degrau
que a explica (a lista fechada, com o degrau de cada uma, está nele) e qualquer
palavra de método na página.

No ar em <https://mateusalkimim.github.io/hello-world-machine/> — em
[inglês](https://mateusalkimim.github.io/hello-world-machine/en/) e em
[português](https://mateusalkimim.github.io/hello-world-machine/pt/).

## O personagem

"Olá, Mundo!": onze letras, **doze bytes**. O acento custa um byte a mais, e esse
detalhe é a aula inteira em miniatura: byte não é letra, e o número cresce por
vizinhos, não por ser maior.

| peças lado a lado | valores possíveis | o que é |
|---|---|---|
| 1 relé | 2 | um bit |
| 8 | 256 | um byte, uma letra |
| 24 | 16,7 milhões | um pixel colorido |
| 32 | 4,29 bilhões | um inteiro comum |

## Os degraus

A letra **o** é seguida na trilha do alto da página, degrau a degrau: o que ela
já virou fica visível, apagado; o atual, aceso.

| | degrau | o que a camada faz com o número | fonte |
|---|---|---|---|
| 0 | a frase já é um código | troca o meio, conserva a mensagem | Petzold, cap. 1 |
| ½ | a tecla vira número | a tecla fecha uma chave; a máquina acha o 79 numa gaveta | cap. 25 |
| 1 | cada letra recebe um número | o **O** vale 79; a frase vira onze números | cap. 13 |
| 2 | cada número vira oito casas | 79 vira 01001111; em oito casas cabem 256 coisas | caps. 11, 12 |
| 2½ | o á não cabe em um byte | 225 passa de 127; o **á** custa dois bytes | cap. 13 |
| 3 | cada casa vira corrente | 1 é corrente passando num relé; 0, parada | caps. 7, 8 |
| 4 | os bits somam e ficam parados | somador e flip-flop: o número é operado e espera | caps. 14 a 21 |
| 5 | cada byte ganha um endereço | dois números por letra: o valor e o lugar | cap. 19 |
| 6 | um número é lido como ordem | CD não é letra, é "chame"; só o contador de programa decide | caps. 23, 27 |
| 7 | as ordens são escritas com palavras | CALL 5 vira CD 05 00 pelo montador | cap. 27 |
| 8 | a ordem vira pontos de luz | a tela é memória, três bytes por ponto | caps. 12, 25 |

O fecho é uma tabela só: o que cada degrau **conserva** e o que **esquece**. É
a régua que atravessa todos: cada camada é uma promessa do tipo "pode esquecer
o resto, isto eu garanto", e a execução é o que sobra quando todas foram
cumpridas.

Os degraus 3 e 4 se apoiam na escada, que agora mora aqui, em
[`pt/escada.html`](pt/escada.html): as arestas relé → porta → somador →
flip-flop → registrador estão lá com citação e com instrumento que monta a peça
na tela.

## Início rápido

```bash
git clone https://github.com/mateusalkimim/hello-world-machine.git
cd hello-world-machine
xdg-open pt/index.html        # no Windows, duplo clique
```

Ou <https://mateusalkimim.github.io/hello-world-machine/>. Para regerar a
página (só Python 3, biblioteca padrão):

```bash
python3 gerar_site.py        # pt/index.html, a matriz
python3 gerar_en.py          # en/index.html, derivado da tabela de tradução
```

Passo a passo em [`docs/INSTALACAO.md`](docs/INSTALACAO.md).

## O que tem aqui

```
index.html            a porta — encaminha por idioma
pt/index.html         a página, em português — GERADA, não editar à mão
pt/placa.html         Olá, Mundo! na placa: o instrumento — GERADO por gerar_placa.py
placa.js              a placa em planta: desenha a máquina e toca o traço, um ciclo por vez
gerar_placa.py        o gerador da página do instrumento
conferir_placa.py     todo nome do traço tem módulo desenhado; nome inventado é recusado
pt/escada.html        a escada: as seis famílias de circuitos — GERADA por escada/gerar_escada.py
pt/bancada.html       a bancada de circuitos: doze missões — GERADA por gerar_bancada.py
barra.py              a barra das quatro partes, a mesma em toda página
escada/               os fontes da escada: famílias, peças, mapa, instrumentos, gerador e conferências
bancada/              a fonte da bancada, uma página que anda sozinha
gerar_bancada.py      cola a barra na bancada, sem tocar no jogo
en/index.html         a mesma página em inglês — DERIVADA de pt/ + traducao/
degraus.py            os degraus, as teses, e as PASSAGENS que os sustentam
figuras.py            uma figura por degrau, com a palavra nova como rótulo
pele.css, visor.js    a pele e o visor: um degrau por tela, trilha no alto
gerar_site.py         o gerador, que aborta se faltar warrant
conferir_degraus.py   o controle negativo do gerador: planta o defeito e exige o aborto
maquina/              a máquina: a CPU do Petzold com tela e teclado mapeados em memória
  maquina.py, maquina.js   o emulador, duas vezes: Python (a referência) e JavaScript (o navegador)
  montar.py, montar.js     o montador, duas vezes: linguagem de montagem → bytes
  programas/               os programas: Olá, Mundo! e o que percorre o conjunto inteiro
  conferir_maquina.py      montador = mão; a tela diz a frase; o caminho de cada letra; controle negativo
  conferir_equivalencia.py as duas implementações dão o MESMO traço, ciclo a ciclo, para cada programa
conferir_idioma.py    cada página está no idioma da pasta em que mora
conferir_publicacao.py  o que não pode sair numa superfície pública
i18n.py, gerar_en.py, gerar_porta.py   a máquina bilíngue, para quem clonar
traducao/             a tabela pt→en, chaveada por hash do original
pesquisa/             a tese do material, a forma de um degrau, e a placa mínima do instrumento
docs/INSTALACAO.md    passo a passo
LICENSE               MIT, para o código
LICENSE-CONTENT       CC BY-SA 4.0, para o conteúdo
```

## As conferências

Nenhuma é promessa: as que podem ter **controle negativo** o têm. Uma
conferência que nunca reprovou não provou nada.

- **`gerar_site.py`** aborta por conta própria: degrau com selo de leitura e
  sem passagem; passagem sem tradução; figura inexistente; tese acima de 25
  palavras ou parágrafo acima de 60; inglês no texto visível; expressão sem
  "lê-se"; e ciclo da placa que não existe no traço ou não mostra o que o
  degrau promete (o gerador roda a máquina e confere o registro);
- **`conferir_degraus.py`** planta cada um desses defeitos numa cópia e exige
  que o gerador aborte. Se ele aceitar um degrau sem citação, a conferência
  reprova;
- **`maquina/conferir_maquina.py`** prova que o montador e a montagem à mão
  concordam byte a byte, que a tela diz a frase, que cada letra chegou por um
  ciclo de escrita vindo do Instruction Latch 2 com o endereço em HL, e que um
  programa com um opcode trocado **não** produz a frase;
- **`conferir_placa.py`** exige que todo nome de origem e destino que apareça
  no traço de cada programa tenha um módulo desenhado na placa, que o roteiro
  passe na sintaxe do node, e que um nome inventado seja recusado;
- **`maquina/conferir_equivalencia.py`** roda cada programa nas duas máquinas,
  Python e JavaScript, e exige o mesmo traço campo a campo, inclusive para um
  programa quebrado; os dois montadores têm de dar os mesmos bytes e recusar
  o que a máquina não tem; e um traço com um único campo alterado tem de ser
  acusado. Usa o node só para rodar o JavaScript fora do navegador; o site não
  depende dele;
- **`conferir_idioma.py`** mede o texto, nunca o nome do arquivo: a página de
  `en/` tem de estar em inglês e a de `pt/` em português;
- **`conferir_publicacao.py`** lê as superfícies públicas, inclusive as
  mensagens de commit, antes de qualquer envio.

## A forma de um degrau

A primeira versão desta página tinha cinco blocos por degrau e até 278
palavras, com trezentas palavras em inglês no meio do texto. Foi medida, e
reprovou na régua da folha em branco. A forma atual saiu de duas fontes: as
normas de composição didática que já regem os outros materiais do autor, e a
literatura sobre explicações exploráveis e carga cognitiva. O que se concluiu,
com as fontes, está em
[`pesquisa/a-forma-de-um-degrau.md`](pesquisa/a-forma-de-um-degrau.md). As
regras que mais pesaram:

- o nível novo aparece **com o anterior ainda visível** (a trilha do alto);
- um degrau é **uma tese e uma figura**; a palavra nova é rótulo dentro da
  figura, nunca glossário ao lado;
- o leitor controla o passo; nada roda sozinho;
- a prova existe, mas fica fechada por padrão.

## A tese

O que torna um computador possível é mais simples do que ele: é morse.
Linguagem por sinal de onda. A corrente muda, o sinal que ela expressa muda a
cada camada, e no fim está o conjunto completo. A pergunta desta página é a
matemática disso: como o que se vê, se lê e se ouve vira 0 e 1; como o já
convertido viaja pelas partes do computador; o que cada parte opera no sinal,
e o que cada pedaço devolve. A espinha, degrau a degrau, está em
[`pesquisa/espinha-matematica.md`](pesquisa/espinha-matematica.md). Dois
pontos pesam mais: a corrente vira dado por **limiar** (um intervalo inteiro
de tensões vira um símbolo só, e o ruído some na equivalência), e o dado
viaja como **onda de estados**, não como coisa que anda.

A eletrônica de cada parte não é o assunto. A corrente entra uma vez, como os
dois estados que a máquina distingue, e daí em diante o assunto é a engenharia
do computador.

## O instrumento

A máquina desenhada em planta, em `pt/placa.html`: dois barramentos, os
módulos entre eles, a tela ao lado, e o traço do Olá, Mundo! tocado ciclo a
ciclo. Em cada ciclo acendem no máximo quatro coisas: a origem do dado, os
oito bits no barramento, o destino, e o endereço. A especificação do desenho
está em [`pesquisa/a-placa-em-planta.md`](pesquisa/a-placa-em-planta.md); a
da máquina, em [`pesquisa/a-maquina.md`](pesquisa/a-maquina.md). O que vem
depois é um jogo de blocos que cai, jogável, na mesma placa, em que se vê a
cor da peça sair do registrador, atravessar o barramento e chegar à memória
de vídeo. A pesquisa que define a placa mínima, os dois relógios e as
regras de legibilidade está em
[`pesquisa/placa-minima-e-dado-visivel.md`](pesquisa/placa-minima-e-dado-visivel.md).

## As quatro partes

O material é um só e tem quatro páginas, ligadas por uma barra no alto de cada
uma. A pergunta é a mesma nas quatro: como uma ideia humana, uma saudação, vira
0 e 1 e volta para a mesma pessoa quase na mesma forma.

- **os degraus** (`pt/index.html`): a viagem de "Olá, Mundo!", um degrau por
  tela. É **a matemática** que torna a conversão possível, e a viagem do sinal
  pelas partes;
- **a placa** (`pt/placa.html`): a mesma viagem rodando na máquina desenhada,
  ciclo a ciclo;
- **a escada** (`pt/escada.html`): **o que precisa existir** para a ida e a
  volta, as seis famílias de circuitos. Transistores ligam e desligam, portas
  lógicas decidem, somadores fazem conta, registradores guardam número,
  instruções mandam, e o relógio marca o tempo. Uma família por tela, com as
  peças, o instrumento que monta cada uma, e a passagem do livro;
- **a bancada** (`pt/bancada.html`): as mesmas peças na mão. Doze missões numa
  bancada de circuitos, de acender uma lâmpada a um número que escolhe o
  circuito, com a tabela de cada missão ao vivo.

A escada nasceu como um repositório à parte, o abstraction-ladder, e foi
trazida para cá: os fontes moram em `escada/` e têm gerador e conferências
próprios. A escada e a bancada estão só em português por enquanto.

## Proveniência e garantias

- **As passagens vêm de um livro, lido**: Charles Petzold, *Code: The Hidden
  Language of Computer Hardware and Software*, 2ª ed. (2022). Elas aparecem sob
  direito de citação, com capítulo, e pertencem ao autor. O livro **não está**
  neste repositório.
- **Onze degraus, quinze passagens**, cada uma com o original em inglês e a
  tradução do autor ao lado, para que a tradução também possa ser conferida.
- **Quatro buracos declarados**, listados em `pesquisa/o-que-falta.md` e em
  `A_LER`: o que este mapa sabe que falta e ainda não abriu (como o 79 vira o
  desenho do "O"; a tabela ASCII em si; o acento num programa de 1978; da
  tela à web). O quinto, da tecla ao número, fechou com o eco. Mapa que
  esconde o que falta mente sobre o próprio tamanho.
- **Dois degraus se apoiam na escada**, e dizem isso com um selo próprio. A
  aresta está lá, com a citação lida e o instrumento.
- **Os números do personagem são derivados**, e marcados assim: os códigos das
  onze letras e os dois bytes do á saem da regra do capítulo 13, e qualquer
  tabela Unicode os confere.
- **A tradução tem dono.** O inglês é derivado do português bloco a bloco, com
  a tabela chaveada por hash do original. Onde a máquina não decidiu, decidiu
  uma pessoa, e a decisão está escrita na tabela.
- Sem rede, sem telemetria, sem dependência. A página abre offline. As fontes
  tipográficas vêm do Google Fonts e têm reserva local.

## Estado, e o que falta

- a página está completa nos onze degraus e no fecho, em português e em
  inglês, com a folha de sinais antes do primeiro símbolo e a linha "a
  matemática daqui" lida em voz alta em cada degrau;
- os degraus 3 e 4 citam a escada, e é lá que as peças são montadas na tela;
- a máquina existe como especificação executável (`maquina/`), em Python e em
  JavaScript, com os dois traços idênticos ciclo a ciclo, e a placa em planta
  (`pt/placa.html`) toca o traço do Olá, Mundo! ciclo a ciclo; cada degrau
  tem o botão "ver na placa", que abre o ciclo que o mostra, e cada módulo da
  placa abre o degrau que o explica; o eco está pronto e conferido, e na
  placa dá para digitar e ver cada tecla ir da gaveta 8200h à tela;
- falta na placa o medidor de limiar num fio: virar um bit e ver o número
  mudar;
- os quatro buracos declarados;
- medir se a forma ensina mais que a anterior é um teste à parte, com régua
  lacrada antes, ainda não feito.

## Licença

Código sob **MIT** (`LICENSE`). Conteúdo, texto e figuras, sob **CC BY-SA 4.0**
(`LICENSE-CONTENT`). As citações do livro pertencem ao seu autor.
