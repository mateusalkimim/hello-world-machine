# Seis famílias: por que a escada mudou de forma

Registro da revisão de 2026-10-03. Vale para qualquer mapa que tenha crescido
degrau a degrau e perdido o leitor no caminho.

## O que a medição achou

A página foi medida antes de ser tocada (Python sobre o HTML gerado, Chrome
headless para a tela). Os números que decidiram a reforma:

| medida | valor |
|---|---|
| a frase mais simples de cada degrau (o campo `diz`, 18 a 27 palavras) | existia no código e **não era renderizada** |
| palavras visíveis × palavras de citação | 4.287 × **4.678**; 102 passagens, 5 abertas em inglês |
| inglês no corpo visível | **5 %**, 214 palavras, a maioria em resumos "por dentro" à vista mesmo fechados |
| palavras por cartão, nos quatro campos | 112 a 159; o orçamento de uma tela didática é 85 |
| nomes que são jargão | 11 de 15 |
| termos que nasciam como rótulo no mapa, sem frase | 27 |
| termos nunca definidos | relógio, bit, byte, flip-flop, latch, warrant, vai-um |
| sinônimos concorrendo na mesma página | registrador × latch; porta × gate; avaliador × interpretador; assembler × montador; memória × RAM |
| pares de degraus no mesmo nível com relação explicada | nenhum |
| figura por conceito | 5 de 15 |
| previsão antes do instrumento, pergunta no fim | 0 |

O diagnóstico de quem lê, antes do número: *"o vocabulário está horrível e a
didática ruim"*. O número só disse onde.

## A decisão

Toda peça cabe numa de **seis famílias**, nomeadas pelo que fazem com o número:

| família | verbo | degraus de dentro | a passagem que a define |
|---|---|---|---|
| transistores | ligam e desligam | eletroímã, relé, transistor | cap. 7: uma chave que a eletricidade controla, em vez dos dedos; cap. 15: o transistor também serve de chave em portas lógicas |
| portas lógicas | decidem | porta | cap. 8 |
| somadores | fazem conta | somador, ULA | cap. 14 |
| registradores | guardam número | flip-flop de nível, de borda, registrador, contador, memória | caps. 17, 19, 20 |
| instruções | mandam | máquina de registradores, montador, interpretador, compilador, paradigma | SICP §5.1; cap. 23 |
| relógio | marca o tempo | oscilador | cap. 17: todo computador tem um oscilador que faz tudo o mais se mover em sincronia |

As famílias resolvem três defeitos de uma vez: dão a relação que faltava entre
degraus do mesmo nível (é a mesma família); dão ao relógio o lugar que a
lógica de composição lhe negava (a lista do que falta recusava "relógio ←
oscilador" como identidade, e identidade é exatamente o que uma família tem
com o seu único membro); e dão o **verbo** antes do nome, que é o que quem não
sabe nada precisa primeiro.

Dois degraus entraram, com passagem lida: o **transistor**, porque a família
das chaves sem ele contava a história até 1947; e o **oscilador**, porque o
relógio não existia na escada senão como entrada de um flip-flop.

## A forma

Uma família por tela, no visor. Em cada tela, nesta ordem: a tese (até 25
palavras); **uma aposta** antes de mexer no instrumento; o instrumento, ou a
figura; o corpo (até 60 palavras); a matemática daqui, com a leitura em voz
alta; os degraus de dentro, fechados, cada um com os quatro campos de sempre,
os selos e as citações; **uma pergunta** no fim, cuja resposta diz onde a
aposta divergiu; e a passagem que define a família, fechada.

A aposta e a pergunta não são enfeite: são o que o domínio da casa sobre
instrumentos didáticos mede como a diferença entre *mexer* e *aprender*
(prever antes, explicar depois). Nenhuma das duas trava o "próximo".

O vocabulário: **um nome em português por coisa**. Registrador, nunca latch;
porta E, OU, NÃO-OU e OU-exclusivo, nunca AND, OR, NOR, XOR no corpo;
montador, interpretador. O inglês fica onde é dele: dentro das passagens
citadas, fechadas. O orçamento é imposto pelo gerador, que aborta acima dele,
e pelas conferências de sempre (citação contra o livro, geometria do mapa,
botão que muda o desenho, tela em três resoluções, idioma por pasta).

## O que ficou fora, e por quê

- a seta **oscilador → flip-flop de borda** está lida e não está desenhada no
  mapa: na grade de três colunas ela cruzaria a seta porta → flip-flop de
  borda. O mapa diz isso em texto, e a aresta vale na família relógio;
- o regime de cada degrau (combinacional, sequencial) continua existindo, mas
  deixou de ser a chave do mapa: a cor passou a ser a família;
- o inglês da página (`en/`) ficou para trás por algumas horas: a tabela de
  tradução é chaveada por hash do original, e a reforma mudou quase todos os
  blocos. Foi derivado de novo no mesmo dia, com catorze blocos decididos à
  mão;
- medir se a forma nova ensina mais que a antiga é um teste à parte, com
  régua lacrada antes, e não foi feito.

## A segunda forma, no mesmo dia: a página para quem não sabe nada

A primeira forma de seis famílias passou em todas as conferências e reprovou
na leitura do autor, por três razões que as conferências não mediam:

- **a página falava de método o tempo todo**: selos, datas, "prova da seta",
  "segunda testemunha", o que falta, como foi feita. É conversa de quem fez o
  mapa com quem audita o mapa, e o leitor da página não é nenhum dos dois;
- **as explicações não estavam no registro certo**: os quatro campos de cada
  peça existiam, escondidos atrás de "por dentro" e escritos para quem já
  sabe, e as telas usavam palavras nunca explicadas (corrente, chave, bit,
  byte, binário, vai-um, borda, endereço);
- **a história do repositório** ("entrou em…", "era até…") vazava para o texto.

O que mudou, por decisão do autor depois de uma amostra reprovada e refeita:

- **duas superfícies**: a página é só para quem não sabe nada; o método, o
  que falta e a procedência moram no README e aqui em `pesquisa/`
  (`o-que-falta.md` é gerado pelo gerador);
- **cada palavra nova é explicada antes de ser usada**, em texto corrido, com
  duas perguntas e só duas: o que é, por que existe. As peças de cada
  família aparecem do mesmo jeito, visíveis, e não em cartões (os cartões
  foram reprovados por chamar atenção demais);
- **sem engenharia elétrica além do necessário**: o transistor é uma chave
  sem nada que se mexa, e não um sanduíche de semicondutor;
- **a folha em branco é propriedade de construção**: o gerador tem a lista
  fechada de palavras técnicas com a tela em que cada uma nasce, aborta se
  uma aparecer antes, e aborta com qualquer palavra de método na página,
  moldura e título incluídos. Logo que entrou em uso ele barrou "porta" em "porta
  da geladeira" (o termo técnico passou a ser "porta lógica"), "registradores"
  como nome de família (liberado, porque a primeira tela apresenta as seis),
  "programa" num campo antigo e "amostra" no título da aba.

A medida depois: entre 83 e 109 palavras visíveis por família, 20 palavras
explicadas, 34 campos na página, zero inglês e zero método visíveis.
