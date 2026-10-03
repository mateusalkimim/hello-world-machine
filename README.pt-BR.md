<!-- idioma: linha gerada por i18n.py -->
> [!NOTE]
> ### 🌍 **[Read this page in English →](README.md)**

# A máquina do olá, mundo — `hello-world-machine`

**O que cada camada de abstração faz com o número, seguindo uma frase só: de
"olá mundo" dito no escuro até a luz que o devolve na tela.** Um degrau por
tela; em cada um, o que esta camada faz com a frase, uma figura, e a passagem
do livro que sustenta o que foi dito. Nenhum degrau entrou por plausibilidade:
**o gerador aborta** se faltar a citação.

É material para quem não sabe nada. A régua é a folha em branco: uma tese de
até 25 palavras, uma figura com a palavra nova dentro dela, um parágrafo de até
60, e a prova guardada atrás de um clique.

No ar em <https://mateusalkimim.github.io/hello-world-machine/> — em
[inglês](https://mateusalkimim.github.io/hello-world-machine/en/) e em
[português](https://mateusalkimim.github.io/hello-world-machine/pt/).

## O personagem

"olá mundo": nove letras, **dez bytes**. O acento custa um byte a mais, e esse
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
| 1 | cada letra recebe um número | o **o** vale 111; a frase vira nove números | cap. 13 |
| 2 | cada número vira oito casas | 111 vira 01101111; em oito casas cabem 256 coisas | caps. 11, 12 |
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

Os degraus 3 e 4 se apoiam na escada que já existe, o
[abstraction-ladder](https://github.com/mateusalkimim/abstraction-ladder): as
arestas relé → porta → somador → flip-flop → registrador estão lá com citação e
com instrumento que monta a peça na tela.

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
en/index.html         a mesma página em inglês — DERIVADA de pt/ + traducao/
degraus.py            os degraus, as teses, e as PASSAGENS que os sustentam
figuras.py            uma figura por degrau, com a palavra nova como rótulo
pele.css, visor.js    a pele e o visor: um degrau por tela, trilha no alto
gerar_site.py         o gerador, que aborta se faltar warrant
conferir_degraus.py   o controle negativo do gerador: planta o defeito e exige o aborto
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
  palavras ou parágrafo acima de 60; inglês no texto visível;
- **`conferir_degraus.py`** planta cada um desses defeitos numa cópia e exige
  que o gerador aborte. Se ele aceitar um degrau sem citação, a conferência
  reprova;
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

O que importa aqui não é a eletrônica de cada camada (isso é profundidade, e
mora na escada). É responder três perguntas: como corrente elétrica vira dado;
como o dado navega em forma de corrente; e o que cada camada de abstração
significa matematicamente. A espinha, degrau a degrau, está em
[`pesquisa/espinha-matematica.md`](pesquisa/espinha-matematica.md). Dois
pontos pesam mais: a corrente vira dado por **limiar** (um intervalo inteiro
de tensões vira um símbolo só, e o ruído some na equivalência), e o dado
viaja como **onda de estados**, não como coisa que anda.

## O instrumento que vem

Um jogo de blocos que cai, jogável, e acima dele uma placa virtual em que se
vê a cor da peça sair do registrador, atravessar o barramento e chegar à
memória de vídeo. A pesquisa que define a placa mínima, os dois relógios e as
regras de legibilidade está em
[`pesquisa/placa-minima-e-dado-visivel.md`](pesquisa/placa-minima-e-dado-visivel.md).

## O lugar no ciclo maior

Este é o segundo pedaço de um mapa maior da computação. O primeiro, o
[abstraction-ladder](https://github.com/mateusalkimim/abstraction-ladder),
sobe pela **profundidade**: do eletroímã ao paradigma, o que é feito do quê.
Este segue pela **substância**: o que acontece com um número quando atravessa
cada camada. Os dois usam a mesma máquina (nós com warrant declarado, página
gerada da fonte, inglês derivado do português) e as mesmas duas fontes.

## Proveniência e garantias

- **As passagens vêm de um livro, lido**: Charles Petzold, *Code: The Hidden
  Language of Computer Hardware and Software*, 2ª ed. (2022). Elas aparecem sob
  direito de citação, com capítulo, e pertencem ao autor. O livro **não está**
  neste repositório.
- **Dez degraus, doze passagens**, cada uma com o original em inglês e a
  tradução do autor ao lado, para que a tradução também possa ser conferida.
- **Cinco buracos declarados**, listados no fecho da página e em `A_LER`: o que
  este mapa sabe que falta e ainda não abriu (como o 111 vira o desenho do "o";
  como a tecla vira o número; a tabela ASCII em si; o acento num programa de
  1978; da tela à web). Mapa que esconde o que falta mente sobre o próprio
  tamanho.
- **Dois degraus se apoiam no abstraction-ladder**, e dizem isso com um selo
  próprio. A aresta está lá, com a citação lida e o instrumento.
- **Os números do personagem são derivados**, e marcados assim: os códigos das
  nove letras e os dois bytes do á saem da regra do capítulo 13, e qualquer
  tabela Unicode os confere.
- **A tradução tem dono.** O inglês é derivado do português bloco a bloco, com
  a tabela chaveada por hash do original. Onde a máquina não decidiu, decidiu
  uma pessoa, e a decisão está escrita na tabela.
- Sem rede, sem telemetria, sem dependência. A página abre offline. As fontes
  tipográficas vêm do Google Fonts e têm reserva local.

## Estado, e o que falta

- a página em português está completa nos dez degraus e no fecho;
- a página em inglês ainda **não** foi derivada: a tabela de tradução está por
  preencher;
- os degraus 3 e 4 citam a escada; o instrumento próprio deste repositório
  (virar um bit e ver o número mudar) ainda não existe;
- cada degrau ainda não traz a linha "a matemática daqui" com a leitura em
  voz alta, nem a folha de convenções antes do primeiro símbolo;
- o instrumento da placa virtual está pesquisado e não construído;
- os cinco buracos declarados.

## Licença

Código sob **MIT** (`LICENSE`). Conteúdo, texto e figuras, sob **CC BY-SA 4.0**
(`LICENSE-CONTENT`). As citações do livro pertencem ao seu autor.
