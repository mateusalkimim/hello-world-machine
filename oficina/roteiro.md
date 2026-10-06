# Roteiro do seminário da oficina

Fonte única do texto falado da oficina de 09/10/2026 (alunos do IMPA,
indicação do Rosivaldo). O deck, e o que mais derivar daqui, sai deste
arquivo. Forma de referência: o seminário "Do registro ao pixel" (capa · ofício
do autor · mapa da viagem com uma pergunta · convenções · estações com pontes ·
onde desagua · fechamento · apêndices).

Texto do autor, Mateus Alkimim. Começado em 06/10/2026.

## As cinco estações

1. A base: o que é um computador, o signo e o espelho (esta abertura).
2. Lógica booleana.
3. Computador.
4. Programa.
5. IA.

## Estação 1 · a base

O que é um computador?

Bem, isso é difícil de definir. Mas pela minha experiência, eu diria que o
computador é um espelho muito elaborado: ele devolve, transformado por regras
que você mesmo (ou outra pessoa) escreveu, aquilo que você pôs nele, e o que
você põe no espelho é um signo. É por isso que para definir um computador,
temos que entender primeiro o que é um signo.

Um signo é uma coisa escolhida para apontar outra. O que produz o signo é uma
intenção. Por exemplo: se eu fizer um sinal de joia para você aqui na América
Latina, a minha intenção é de aprovação, confirmação ou saudação. É um signo
com significado positivo. Porém, se eu fizer esse mesmo joia no Oriente Médio
ou na África Ocidental o gesto é ofensivo. O mesmo gesto, outros observadores,
outros significados.

Agora vamos imaginar a saudação:

"Olá, Mundo!"

Essa saudação é uma intenção (reconhecer alguém), e para essa intenção
escolhemos o signo "Olá".

O que o computador reflete é o signo, ele não entende intenção, não entende
ideia, não entende conceito. O que o computador manipula são sinais elétricos,
presença ou ausência de corrente.

Quando o computador escreve na tela: "Olá, Mundo!", o significado e sentido
está na minha cabeça, o que ele faz é reproduzir o signo, a frase que eu
escolhi para aquele significado.

O fluxo é:

Intenção > Escolha de signo > Signo vira dados > Computador opera > Computador
devolve os dados > Alguém interpreta o significado.

O computador como conhecemos hoje, só tem sentido com um intérprete, com um
observador. O computador não substitui quem interpreta: sem alguém nas duas
pontas, o que sai dele são só padrões. É claro, um computador pode realizar
certas tarefas com mais eficiência do que uma pessoa, mas sem pessoa alguma, o
computador nem teria tarefas para fazer.

Mas como é possível um signo se transformar em dados?

Para demonstrar isso ao longo desta apresentação, eu escolhi uma frase icônica
para a programação, a saudação do primeiro programa:

"Olá, Mundo!"

Eu vou mostrar como essa frase sai da minha mente, ou da sua, vira dados e
depois é devolvida para nós com quase a mesma forma.

Voltando à pergunta inicial, o que é um computador? Vou resumi-lo a seis
famílias de componentes: transistores, portas lógicas, somadores,
registradores, instruções e relógio. Tudo o mais que você vê num computador
(tela, teclado, disco, rede) fica fora dessas seis famílias. São periféricos:
jeitos de colocar números na máquina ou tirar números dela. E é por um deles,
a tela, que o "Olá, Mundo!" vai voltar pra gente. Quando essa apresentação
terminar você entenderá o que é lógica booleana, um computador, um programa e
uma IA.

## Estação 2 · lógica booleana

O que é lógica booleana?

Em 1854, George Boole percebeu uma coisa estranha: frases que só podem ser
verdadeiras ou falsas obedecem a uma aritmética. Não a aritmética dos números,
mas uma com só dois valores, verdadeiro e falso, e três operações: E, OU, NÃO.
Isso é a lógica booleana. Quase um século depois, alguém notou que um
interruptor também só tem dois estados. Daí pra frente, verdadeiro virou
"corrente passa" e falso virou "corrente não passa".

Vamos fazer um exercício no instrumento que desenvolvi especificamente para
essa apresentação:

Dois interruptores em fila no mesmo fio. A lâmpada só acende se os dois
estiverem fechados. Isso é o E. Dois interruptores em caminhos paralelos: basta
um fechado. Isso é o OU. Um interruptor que fecha quando ninguém aperta e abre
quando apertam: isso é o NÃO. Com os três, montados em fios, qualquer frase
lógica vira um circuito. A lógica não está em lugar nenhum dentro da máquina;
está no jeito como os fios foram soldados.

Com números, chamando ligado de 1 e desligado de 0:

1 E 1 = 1, qualquer outra combinação dá 0.
0 OU 0 = 0, qualquer outra combinação dá 1.
NÃO 1 = 0, NÃO 0 = 1.

São as únicas contas que a máquina sabe fazer. Tudo o mais, inclusive somar, é
essas três repetidas.

No "Olá, Mundo!" a lógica booleana aparece antes mesmo da frase existir: quando
você aperta a tecla O, o teclado precisa descobrir qual tecla foi, e faz isso
com uma pergunta booleana por fio: "esta linha está ligada E esta coluna está
ligada?". Onde a resposta é 1, ali está o O.

Então ok. Mas o mundo não é só verdadeiro e falso. O mundo como conhecemos não
possui apenas dois números, duas afirmações, duas leis. São infinitos números e
quase infinitas quantidades. E é aí que entra a matemática, como linguagem e
não só como medida. Os números são para a matemática, o que as palavras são
para o português: signos, formas de se referir a algo pela sua quantidade. É
possível escrever qualquer número inteiro com 0 e 1, e chegar tão perto quanto
se queira de qualquer outro. Isso é o que chamamos de binário.

Vamos ver como funciona:

## Estação 3 · computador

O que é um computador?

Agora dá pra responder. Um computador é um espelho feito de interruptores. Tudo
o que ele tem são seis famílias de peças: cinco feitas uma da outra, e um
relógio que marca o passo de todas.

### Transistores

Um interruptor de luz comum: dedo aperta, lâmpada acende. Agora imagine que o
dedo foi substituído por um eletroímã. Quando chega corrente no eletroímã, ele
puxa a lâmina e fecha o circuito. Quando a corrente para, a lâmina solta e o
circuito abre. Um interruptor que a eletricidade aperta: isso é um transistor.

Na bancada, parte da bateria, transistor, lâmpada S, em linha. Em cima do
transistor, uma chave A com sua própria bateria. A chave não está no caminho da
lâmpada; ela só alimenta o eletroímã. Ligue A: o eletroímã puxa, a lâmina
baixa, a lâmpada S acende. Desligue A: tudo solta.

Número. Um processador atual tem dezenas de bilhões de transistores num chip de
poucos centímetros, e cada um pode abrir e fechar até 4 bilhões de vezes por
segundo.

A chave A é o seu dedo; o transistor é o dedo da máquina. Daqui pra frente,
nenhuma peça do computador precisa de uma pessoa apertando. Um fio aperta o
outro.

### Portas lógicas

Dois transistores em fila no mesmo fio, cada um com seu eletroímã. A lâmpada só
acende se os dois fecharem. Isso é a porta E. Dois transistores em caminhos
paralelos, que se juntam antes da lâmpada: basta um fechar. Porta OU. E um
transistor ao contrário, que nasce fechado e abre quando o eletroímã puxa:
porta NÃO. A lógica booleana da estação passada, agora sem dedo nenhum.

Na bancada. Bateria, transistor N, transistor N, lâmpada S, em linha. Chave A
em cima do primeiro, chave B em cima do segundo. Ligue só A: nada. Só B: nada.
As duas: acende. Depois troque os dois N por P: agora S acende só com as duas
desligadas. É a porta NÃO-OU, o NÃO aplicado ao OU.

Número. Com E, OU e NÃO dá pra montar qualquer circuito que exista. Uma porta E
são dois transistores; o processador inteiro é da ordem de bilhões de portas.

A lâmpada de uma porta é um fio com corrente, e um fio com corrente é
exatamente o que aperta o eletroímã da próxima. A saída de uma porta aciona a
seguinte sozinha. A partir daqui, a cadeia anda sem ninguém no meio.

### Somadores

Imagem. Uma mão com um dedo só. Dá pra mostrar 0 ou 1. Peça "1 + 1": não tem
como mostrar 2. Então o dedo abaixa e cutuca a pessoa do lado pra ela levantar
o dela. Duas saídas: o que fica no meu dedo (a soma) e o cutucão (o vai-um).

Na bancada. Duas chaves A e B, duas lâmpadas S e C. C acende só com as duas
ligadas: é a porta E. S acende quando exatamente uma está ligada: um OU
passando por um transistor que o NÃO-E controla. Ligue A e B juntas: S apaga, C
acende. Lendo as duas lâmpadas: 10, que é 2.

Número. Oito desses em fila, cada um com um terceiro fio para receber o vai-um
do vizinho, somam de 0 a 255. Um processador faz uns 4 bilhões dessas somas por
segundo, e cada uma é só corrente atravessando portas.

Nenhuma peça sabe somar. O arranjo foi feito de um jeito em que, se entram os
fios de 79 e os fios de 1, saem os fios de 80 por pura física, como um ábaco
cujas contas não sabem matemática.

### Registradores

Uma lâmpada que segura o próprio interruptor. Depois que recebe corrente, ela
alimenta o eletroímã do transistor que a mantém acesa. Mesmo que a fonte
original desligue, ela continua. Só apaga quando alguém manda gravar outra
coisa. Isso é um número guardado.

Na bancada. Chave D é o dado, chave G é "gravar", lâmpada Q é a gaveta. Ligue
G, ligue D: Q acende. Desligue G. Desligue D. Q continua acesa. Ligue G de
novo: Q copia o D atual e apaga. Depois apague o fio que volta de Q pro
transistor e veja a gaveta esquecer.

Número. Uma gaveta de 1 bit são meia dúzia de transistores. Um computador comum
tem 16 GB de memória: 137 bilhões dessas gavetas, cada uma com um endereço.
Neste momento, numa delas, o "O" de "Olá" está guardado como 79: 01001111.

Registrador e memória são a mesma peça em distâncias diferentes. O registrador
fica colado no processador e é rapidíssimo; a memória fica mais longe e é
enorme. O 79 vive numa gaveta até alguém pedir.

### Instruções

Um pátio de trens com chaves de desvio. Um número de 8 bits chega nos fios das
chaves: uma combinação abre fisicamente o caminho até o somador e fecha os
outros; a combinação 00110110, que a placa mostra como 36, abre o caminho até o
circuito que copia um número para a memória. Ninguém lê o número. Ele encaixa,
como uma chave só entra na fechadura certa.

Na bancada. Chave I é a instrução. Monte uma porta E e uma porta OU separadas,
as duas com A e B. A saída do E passa por um transistor P controlado por I; a
do OU, por um N controlado por I. Junte as duas na lâmpada S. Com I desligada,
S responde como E. Com I ligada, como OU. Um bit de instrução escolheu qual
circuito chega na saída.

Número. Um processador real tem algumas centenas de instruções possíveis, cada
uma com seu número. "Olá, Mundo!" é uma instrução de copiar repetida onze
vezes: ponha na célula da tela o número que vem logo atrás de mim. A letra
viaja dentro da própria instrução: 36 e, logo atrás, 4F. Onze, porque a
vírgula, o espaço e a exclamação também são números. Nesta máquina o á cabe num
byte só, E1; nos computadores de hoje ele viaja em dois, e é por isso que o
degrau 4 do site diz que ele não cabe.

Um programa é uma fila de instruções guardada na memória. É a parte da máquina
que mais parece entender, e é a que menos entende: são fios encaixando em
fechaduras.

### Relógio

Um metrônomo ligado em todos os circuitos. A cada batida, a máquina faz uma
coisa só: busca um pedaço da instrução, ou executa, ou guarda o resultado.
Entre uma batida e outra, nada muda. Sem ele, o somador, as gavetas e as chaves
de trem trabalhariam ao mesmo tempo e se atropelariam.

Na bancada. Coloque um relógio e uma lâmpada L: ela pisca. Agora ligue o
relógio na chave G da gaveta da estação passada: Q passa a copiar D só nas
batidas. Isso é o computador inteiro em miniatura: o dado espera, o relógio
autoriza.

Número. Um relógio de 4 GHz bate 4 bilhões de vezes por segundo. Cada batida
dura um quarto de bilionésimo de segundo, e nesse tempo a luz anda 7
centímetros.

O relógio é o que faz uma coisa de cada vez, em fila. As onze letras do "Olá,
Mundo!" vão sair uma a cada cinco batidas, 61 batidas ao todo, e você nunca vai
perceber que não foi tudo junto.

## Estação 4 · programa

O que é um programa?

Imagem. Um mapa de trilhos com chaves de desvio. O mapa mostra todos os
caminhos que um trem poderia fazer; nenhum trem anda no mapa. Um programa é
esse mapa: uma fila de instruções guardada na memória, com todos os caminhos
possíveis já desenhados por quem o escreveu. Quando o programa roda, os dados
vão abrindo as chaves, e o trem faz um caminho só. Esse caminho é o percurso.
O fluxograma é o desenho do mapa: cada losango é uma chave de desvio, cada
seta é um trilho.

O "Olá, Mundo!" é um mapa sem nenhuma chave de desvio: onze instruções de
copiar, uma atrás da outra, ponha na célula da tela o número que vem logo
atrás de mim. Só existe um percurso possível. Por isso o traço dele é sempre o
mesmo: 61 batidas do relógio, hoje, amanhã, em qualquer máquina igual. A conta:
duas instruções para apontar a primeira célula da tela, 3 batidas cada, 6;
onze para escrever uma letra, 3 cada, 33; dez para avançar uma célula, 2 cada,
20; uma para parar, 2. Vinte e quatro instruções, 61 batidas.

O eco tem uma chave de desvio que aponta pra trás: um laço. A máquina olha a
gaveta onde o teclado escreve, quase sempre encontra zero e volta a olhar;
quando encontra um número, copia pra tela, zera a gaveta para não ler a mesma
tecla duas vezes, e volta a olhar. O mapa é pequeno, mas cada execução é
diferente, porque o percurso depende do que a pessoa digita e de quando
digita. Mesmo programa, trens diferentes.

O conjunto-inteiro.asm tem cinco chaves de desvio, cinco losangos, e foi
escrito para passar por cada uma nas duas posições, salto tomado e não tomado.
Mas nada entra nele de fora: os números que chegam nas chaves foram escritos
pelo autor. Por isso ele tem um percurso só, 171 batidas, sempre o mesmo. Quem
tem percursos diferentes é o eco, porque é nele que um número vem de fora.

O mapa é um signo: foi uma pessoa que desenhou todos os caminhos, sabendo o
que queria dizer com cada um. O percurso não é signo de nada; é só corrente
passando pelas chaves que os dados abriram. Quando você vê "Olá, Mundo!" na
tela, está vendo o fim de um percurso, e lendo nele o signo que alguém pôs no
começo do mapa.

Mas todo signo nasce de uma intenção. Então o que fazemos na computação é
escrever a intenção num mapa e delegar à máquina o percurso; nós só
embarcamos. A intenção nunca sai do mapa; o que a máquina faz é cumpri-la sem
saber. No começo eram intenções pequenas: o ENIAC, em 1945, fazia cerca de 5
mil somas por segundo. Hoje um único núcleo de processador faz alguns bilhões,
mais de um milhão de vezes mais, e um computador comum tem vários núcleos. As
intenções cresceram na mesma escala.

## Estação 5 · IA

Volte ao mapa de trilhos. Em tudo o que vimos até agora, uma pessoa desenhou
o mapa sabendo o que queria dizer com cada caminho. Uma IA é um mapa que
ninguém desenhou. Ele tem bilhões de chaves, só que de outro tipo: em vez de
abrir ou fechar, cada uma deixa passar uma fração da corrente. E a posição de
cada uma foi ajustada por tentativa: mostra-se um exemplo, olha-se o que saiu,
e cada chave gira um pouquinho na direção de ter acertado. Repita isso
trilhões de vezes, com texto escrito por milhões de pessoas, e as chaves
terminam numa posição que ninguém escolheu e ninguém consegue ler, mas que
funciona. O mapa não foi desenhado; foi esculpido pelos exemplos.

Não há nenhuma peça nova. É o mesmo somador da estação 3, e multiplicar é
somar repetido; só que milhões deles trabalhando juntos, e registradores
guardando bilhões de números. Quando você digita "Olá" numa IA, a palavra vira
79, 108 e os dois bytes do á, como sempre, e depois vira mais uma coisa: uma
lista de milhares de números, uma posição num espaço. E o que importa não é
nenhum número da lista; é onde essa posição fica em relação às outras: perto
de "oi", longe de "parafuso", na mesma direção de "bom dia". O conceito virou
geometria. A máquina percorre o mapa, somando e multiplicando essa posição com
as bilhões de chaves, e no fim entrega outra posição: o signo mais provável de
vir em seguida. Isso, bilhões de vezes, é uma conversa.

Um modelo grande tem algo como centenas de bilhões de chaves, ajustadas com
trilhões de palavras. Cada palavra que entra vira uma lista de milhares de
números. Cada palavra que sai custa duas contas por chave, da ordem de
centenas de bilhões a um trilhão de somas e multiplicações, em somadores do
mesmo tipo dos que montei na bancada de circuitos do hello-world-machine, só
que muitos mais.

O espelho continua espelho: devolve, transformado por regras, o que você pôs
nele. O que mudou é de quem são as regras. Até aqui elas eram de uma pessoa
que escreveu o mapa; agora são a forma deixada por milhões de pessoas que
nunca souberam que estavam desenhando. Então o que volta pra você não é só o
seu reflexo; é o reflexo de muita gente, filtrado pelo seu signo. Continua não
havendo intenção lá dentro: a IA não quer dizer "Olá", ela encontrou a posição
onde "Olá" costuma estar. O mapa dela copia a forma do mundo, não o mundo. Ela
sabe onde "gato" fica em relação a tudo o mais; nunca sentiu pelo. O
conhecimento que ela tem é o do mapa, nunca o do território. E é por isso que,
mesmo com ela, a estação final continua sendo a mesma de sempre: alguém lendo
e pondo significado.

É isso que uma IA é, na prática. Um programa que devolve o mais plausível em
vez de um resultado fixado de antemão. Ele encontra padrões, repetições e
exceções mais rápido do que uma pessoa. Em tarefas processuais digitais,
produz texto dezenas de vezes mais rápido do que qualquer um digita, e segue
as regras que você escreveu na maior parte das vezes. Ligado a uma memória
vetorial, ele recupera o rastro do que foi discutido três meses atrás numa
sessão de estudos e traz de volta detalhes que você já tinha esquecido, porque
a memória humana se perde com o tempo e a dele fica em disco pelo tempo que
você quiser.

## Fechamento

A viagem termina onde começou. Na primeira folha, "Olá, Mundo!" saiu da minha
cabeça, ou da sua. Passou pela lógica booleana e virou corrente que passa ou
não passa; pelo computador, e virou número em gaveta; pelo programa, e virou
um percurso de 61 batidas; e pela IA, onde as regras deixaram de ser de uma
pessoa só. Agora está na tela da placa, com quase a mesma forma. O espelho
devolveu. Eram quatro promessas: lógica booleana, um computador, um programa e
uma IA. O significado continua onde sempre esteve: em quem lê.

Agora eu vou tirar um tempo e mencionar uma outra apresentação que eu
construí para falar do que uma imagem é feita. O nome dela é "Do registro ao
pixel": lá eu mostro tudo que compõe uma imagem na tela do seu computador,
celular, TV, e como a matemática acontece por trás disso. Espero apresentar
esse material para vocês algum dia também.

Mas então, infelizmente toda viagem tem um final, mas eu agradeço a Deus por
estar vivo compartilhando esse momento com vocês. Agradeço todo o incentivo e
oportunidade que meu orientador, Rosivaldo, tem me dado, que me fez estar aqui
hoje. E por fim, agradeço muito o tempo e a atenção de todos que me ouviram.
Espero ter o prazer de encontrá-los novamente!
