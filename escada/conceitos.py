# -*- coding: utf-8 -*-
"""Os quatro campos de cada degrau — o que ele É, por que EXISTE, onde APARECE
e onde o leitor TRAVA.

Por que este arquivo existe
---------------------------
O `degraus.py` responde *como a escada se sustenta*: cada aresta com a frase do
livro. Ele não responde *o que a peça é* — e a página, por isso, nomeava 33
componentes que nunca definia. Este arquivo paga essa dívida.

A REGRA, e ela é o motivo de o arquivo não ter sido gerado por modelo
---------------------------------------------------------------------
Quatro campos por peça é um molde barato de preencher com um modelo de
linguagem: sai numa tarde e parece completo. O preço aparece depois, quando uma
afirmação plausível e errada fica publicada porque ninguém a leu — e um campo
sobre onde o aluno trava não tem como ser conferido contra fonte nenhuma.

A saída, neste domínio, é que **não é preciso modelo nenhum**: o Petzold é
professor, e o livro já responde *o que é* e *por que existe*, em prosa, com
capítulo. Então cada campo carrega a sua classe:

  (a) CITAÇÃO — o campo é tradução fiel de uma passagem, e a passagem vai junto;
  (b) SÍNTESE — o campo é resumo meu de passagem citada, e a passagem vai junto
      para o leitor conferir se o resumo é honesto;
  (d) OFÍCIO  — julgamento didático de quem ensina. Nenhum livro escreve "onde
      o aluno trava"; isso vem da sala de aula. **Entra sem confirmação, e a
      página o marca como tal até o autor responder por ele** com data.

Não há classe para "o modelo escreveu". Se um campo não tem fonte nem dono, ele
não entra — fica em branco, e a página diz que está em branco.

Fonte da prosa citada: o `livro.md` da dissecação `petzold-code-2ed` do
Mouseion (classe A, epub nato-digital), conferido capítulo a capítulo.
"""

# (texto em portugues, classe, referencia, passagem original, confirmado_em)
# classe: "a" citação · "b" síntese de passagem citada · "d" ofício
#
# CONFIRMACAO (2026-08-27). Os 17 campos de classe "d" nasceram sem
# confirmacao. Nesta data o autor os leu e respondeu por eles, e o selo deixou
# de dizer "nao confirmado". A data nao e enfeite: ela diz A PARTIR DE QUANDO
# alguem responde pelo texto, e um campo que mudar depois dela deixa de estar
# confirmado ate ser relido.
RATIFICADO_EM = "2026-08-27"

C = lambda t, ref, cit: (t, "a", ref, cit, None)
S = lambda t, ref, cit: (t, "b", ref, cit, None)
O = lambda t, em=RATIFICADO_EM: (t, "d", None, None, em)

CONCEITOS = {
"transistor": {
 "o_que_e": S('Um interruptor com um eletroímã no lugar do dedo: com corrente no fio de controle, o caminho fecha; sem corrente, abre. Na bancada ele aparece com ímã e lâmina, que é como dá para ver; dentro do chip, o mesmo abre e fecha acontece sem peça que se mexa.',
   'cap. 15 — Is This for Real?',
   'Vacuum tubes were originally developed for amplification, but they could also be used for switches in logic gates. The same goes for the transistor.'),
 "por_que_existe": S('Para fazer o que o relé faz sendo minúsculo, rápido, sem esquentar e sem gastar quase nada. Foi assim que o rádio passou a caber no bolso.',
   'cap. 15 — Is This for Real?',
   'Vacuum tubes were originally developed for amplification, but they could also be used for switches in logic gates. The same goes for the transistor.'),
 "onde_aparece": S('Em tudo que é pequeno e não esquenta: menor que a válvula, gasta menos, dura mais. O rádio de bolso de 1954 foi o primeiro.',
   'cap. 15 — Is This for Real?',
   'Besides being much smaller than vacuum tubes, transistors require much less power, generate much less heat, and last longer.'),
 "onde_se_trava": O('Em achar que o transistor é uma peça de outra espécie. Aqui ele é a mesma peça que o relé: uma chave que a corrente aciona. Mudou o material, não o papel.', None),
},
"oscilador": {
 "o_que_e": C(
   "Um circuito que muda de estado sozinho, sem ninguém abrir ou fechar uma "
   "chave.",
   "cap. 17 — Feedback and Flip-Flops",
   "The oscillator doesn’t require a human being; it basically runs by itself."),
 "por_que_existe": S(
   "Porque todo computador precisa de algo que faça o resto se mover em "
   "sincronia: é o relógio.",
   "cap. 17 — Feedback and Flip-Flops",
   "All computers have some kind of oscillator that makes everything else move "
   "in synchronicity."),
 "onde_aparece": S(
   "No relógio de todo computador — de cristal de quartzo, nos de verdade —, e "
   "em todo lugar onde se conta o tempo contando voltas.",
   "cap. 17 — Feedback and Flip-Flops",
   "The oscillators in real computers are somewhat more sophisticated, however, "
   "consisting of quartz crystals wired in such a way that they vibrate very "
   "consistently and very quickly."),
 "onde_se_trava": O(
   "Em ouvir “relógio” e pensar em horas. O relógio da máquina não diz a hora: "
   "ele dá o passo. Cada volta é um instante em que os registradores podem "
   "guardar e o contador avançar.", None),
},

"eletroima": {
 "o_que_e": C('Um pedaço de ferro com um fio enrolado nele. Com corrente no fio, o ferro vira ímã; sem corrente, deixa de ser.',
   'cap. 7 — Telegraphs and Relays',
   'If you take an iron bar, wrap it with a couple of hundred turns of thin insulated wire, and then run a current through the wire, the iron bar becomes a magnet.'),
 "por_que_existe": S('Porque é o jeito de a eletricidade puxar alguma coisa à distância, e de ligar e desligar esse puxão à vontade.',
   'cap. 7 — Telegraphs and Relays',
   'Morse couldn’t use a lightbulb as his signaling device because a practical one wouldn’t be invented until 1879. Instead, Morse relied upon the phenomenon of electromagnetism.'),
 "onde_aparece": O('Na campainha da sua casa, na tranca que abre o portão sozinha, no alto-falante, e dentro do relé, que vem a seguir.'),
 "onde_se_trava": O('Ele não é ímã: ele é ímã enquanto a corrente passa. O que importa é que ele desliga. Tudo o que vem depois depende de desligar.'),
},

"rele": {
 "o_que_e": C('Um eletroímã que puxa uma chave. Quando a corrente chega, o ímã puxa a lâmina, e a lâmina fecha outro caminho, de outra pilha.',
   'cap. 7 — Telegraphs and Relays',
   'A relay is like a sounder in that an incoming current is used to power an electromagnet that pulls down a metal lever. The lever, however, is used as part of a switch connecting a battery to an outgoing wire.'),
 "por_que_existe": S('Para um sinal fraco acionar um sinal forte. O fio comprido enfraquece o sinal; o relé o faz nascer de novo, com pilha nova.',
   'cap. 7 — Telegraphs and Relays',
   'the longer a length of wire becomes, the more resistance it has to the flow of electricity. This was a major impediment to long-distance telegraphy. … In this way, a weak incoming current is “amplified” to make a stronger outgoing current.'),
 "onde_aparece": S('No carro, para dar a partida; no ar-condicionado; e, antigamente, no computador inteiro, que era feito de relés.',
   'cap. 7 — Telegraphs and Relays',
   'It’s a switch, surely, but a switch that’s turned on and off not by human hands but by an electrical current. You could do amazing things with such devices. You could actually assemble much of a computer with them.'),
 "onde_se_trava": O('O circuito que manda e o circuito que obedece são dois circuitos separados: eles não se encostam, só o ímã atravessa. É por isso que um relé pode mandar em outro relé, e é disso que tudo o mais é feito.'),
},

"porta": {
 "o_que_e": S('Uma peça que responde sim ou não: deixa a corrente passar, ou bloqueia, conforme o que chega nas entradas. É feita de chaves ligadas de um certo jeito.',
   'cap. 8 — Relays and Gates',
   'Reduced to its essentials, a computer is a synthesis of Boolean algebra and electricity. The crucial components that embody this melding of math and hardware are known as logic gates. … Logic gates perform simple operations in Boolean logic by blocking or letting through the flow of electrical current.'),
 "por_que_existe": S('Porque uma chave acionada por outra chave pode ser ligada a mais chaves, e assim as perguntas de sim ou não se combinam até virar conta.',
   'cap. 8 — Relays and Gates',
   'Relays have an advantage over switches in that relays can be switched on and off by other relays rather than by fingers. This means that logic gates can be combined to perform more complex tasks, such as simple functions in arithmetic and, eventually, the workings of entire computers.'),
 "onde_aparece": O('Toda condição de todo programa que você já escreveu. O <code>if (a &amp;&amp; b)</code> da sua última função é esta porta, com sessenta anos de camadas em cima.'),
 "onde_se_trava": O('Aqui <b>nada mudou fisicamente</b> — mudou a descrição. Continua sendo corrente atravessando metal; o que passou a existir foi <i>chamar</i> aquilo de verdadeiro e falso. Este é o primeiro salto de abstração da escada, e é o mais fácil de atravessar sem perceber que se atravessou — por isso quem pula aqui não entende mais nada lá em cima.'),
},

"somador": {
 "o_que_e": C('Uma peça que soma dois bits e devolve dois: o bit da soma e o vai-um.',
   'cap. 14 — Adding with Logic Gates',
   'adding a pair of binary numbers results in two bits, which are called the sum bit and the carry bit (as in “1 plus 1 equals 0, carry the 1”)'),
 "por_que_existe": S('Porque somar uma casa só não basta: da segunda casa em diante são três bits a somar, os dois da casa e o vai-um que veio da anterior.',
   'cap. 14 — Adding with Logic Gates',
   'We can use the half adder only for the addition of the rightmost column: 1 plus 1 equals 0, carry the 1. For the second column from the right, we really need to add three binary numbers because of the carry. And that goes for all subsequent columns.'),
 "onde_aparece": O('Toda soma de todo processador do mundo, inclusive a que somou o índice do laço que você rodou hoje. Também é onde mora o estouro: o vai-um que sai da última coluna e não tem para onde ir.'),
 "onde_se_trava": S('A armadilha é tratar o somador como caixa-preta — entra isto, sai aquilo, não pergunte. O próprio Petzold corrige: como se sabe o que há dentro, o nome certo é <b>caixa transparente</b>. Quem aceita a caixa-preta aqui aceita em todos os degraus seguintes, e a escada inteira vira mágica.',
   'cap. 14 — Adding with Logic Gates',
   'Sometimes a box like this is called a black box. A particular combination of inputs results in particular outputs, but the implementation is hidden. But since we know what goes on inside the half adder, it’s more correctly termed a clear box.'),
},

"flipflop": {
 "o_que_e": S('O primeiro circuito que lembra: com as duas chaves soltas, ele pode estar de dois jeitos, e fica no jeito em que a última chave o deixou.',
   'cap. 17 — Feedback and Flip-Flops',
   'We can say that this circuit has two stable states when both switches are open. Such a circuit is called a flip-flop… A flip-flop circuit retains information. It “remembers.” It only remembers what switch was most recently closed, but that is significant.'),
 "por_que_existe": O('Porque sem lembrar não existe antes: não há conta acumulada, não há contagem, não há ordem a cumprir. Tudo o que a máquina faz com o tempo começa aqui.'),
 "onde_aparece": S('É de 1918, dos físicos de rádio Eccles e Jordan — anterior ao computador. Hoje: cada bit de cada registrador, e o antitrepidação de todo botão físico que você aperta.',
   'cap. 17 — Feedback and Flip-Flops',
   'The flip-flop dates from 1918 with the work of English radio physicists William Henry Eccles (1875–1966) and F.W. Jordan (1881–1941).'),
 "onde_se_trava": S('A realimentação. A saída volta e vira entrada, então <b>não existe um primeiro instante</b> por onde começar a traçar o sinal. Quem tenta seguir em ordem cronológica entra em looping e conclui que não entendeu. O jeito de ler é outro: parar de seguir o caminho e procurar quais combinações <i>se sustentam</i> — os estados estáveis.',
   'cap. 17 — Feedback and Flip-Flops',
   'The output of the NOR gate on the left is an input to the NOR gate on the right, and the output of that NOR gate is an input to the first NOR gate. This is a type of feedback. Indeed, just as in the oscillator, an output circles back to become an input.'),
},

"flipflop_b": {
 "o_que_e": S('Um flip-flop que só guarda o dado no instante em que o relógio sobe, e não durante todo o tempo em que ele está alto. É feito de dois flip-flops de nível em fila.',
   'cap. 17 — Feedback and Flip-Flops',
   'An edge-triggered D-type flip-flop is constructed from two stages of level-triggered D-type flip-flops, wired together this way:'),
 "por_que_existe": S('Porque o de nível vaza: enquanto o relógio está alto, qualquer mudança na entrada atravessa para a saída. Num circuito ligado à própria saída, isso vira um laço sem fim.',
   'cap. 17 — Feedback and Flip-Flops',
   'This is what’s called an “infinite loop.” It occurs because the D-type flip-flop we designed was level-triggered. The Clock input must change its level from 0 to 1 in order for the value of the Data input to be stored in the latch. But during the time that the Clock input is 1, the Data input can change, and those changes will be reflected in the values of the outputs.'),
 "onde_aparece": O('Todo “relógio” de que se fala em processador. Os 3,6 GHz da sua máquina são 3,6 bilhões dessas bordas por segundo — não 3,6 bilhões de instantes em que o relógio está ligado.'),
 "onde_se_trava": O('O modelo errado é “o relógio <b>habilita</b> o circuito”. Não é: o evento é a <b>transição</b>, não o estado. Enquanto o relógio for lido como uma chave que fica ligada um tempo, o contador não faz sentido nenhum — e quase todo mundo carrega esse modelo errado sem nunca ter sido corrigido, porque em prosa os dois soam iguais.'),
},

"contador": {
 "o_que_e": S('Uma fileira de flip-flops de borda em que cada um dispara o seguinte. Lida em binário, a fileira conta os tiques do relógio.',
   'cap. 20 — Automating Arithmetic',
   'This is a job for a counter built from a row of cascading flip-flops, such as the one you saw on page 237 of Chapter 17:'),
 "por_que_existe": O('Porque a máquina precisa saber qual é a próxima. O número que o contador guarda vira o endereço que ela vai ler em seguida.'),
 "onde_aparece": O('O <code>PC</code> que o depurador te mostra parado numa linha. O relógio digital da parede. E o índice do laço, uma camada acima.'),
 "onde_se_trava": O('Ninguém <i>projetou</i> a contagem binária: ela <b>aparece</b> de graça quando se encadeia flip-flop em flip-flop, porque cada um vira na metade da frequência do anterior. Quem procura a peça que “faz a conta” não acha, e conclui que faltou alguma coisa. Não faltou — a conta é a fiação.'),
},

"registrador": {
 "o_que_e": S('Oito flip-flops lado a lado, que guardam um byte enquanto a ULA trabalha nele. A máquina manda guardar e manda devolver.',
   'cap. 22 — Registers and Busses',
   'These latches are called registers, and a primary purpose of these registers is to store bytes as they are processed by the ALU.'),
 "por_que_existe": O('Porque a ULA precisa de um lugar perto dela para pousar os números que vai somar e o resultado. Buscar na memória a cada passo seria uma viagem a cada conta.'),
 "onde_aparece": O('Quando a ficha de um processador diz “16 registradores de 64 bits”, são estes. E é o que o compilador está disputando quando decide o que fica perto e o que vai para a memória.'),
 "onde_se_trava": O('Achar que registrador é só uma memória pequena. A diferença não é de tamanho, é de <b>endereçamento</b>: memória se acessa por endereço calculado; registrador se nomeia na própria instrução. Por isso um cabe numa instrução e o outro não.'),
},

"maquina": {
 "o_que_e": S('Registradores e operações, mais um controlador que diz a ordem em que as operações acontecem. Desenhada, ela é um diagrama de fiação.',
   'SICP §5.1 — Designing Register Machines',
   'To design a register machine, we must design its data paths (registers and operations) and the controller that sequences these operations. … If we view the arrows as wires and the X buttons as switches, the data-path diagram is very like the wiring diagram for a machine that could be constructed from electrical components.'),
 "por_que_existe": S('Porque peça solta não faz nada em ordem. Faltava um sinal que mandasse as peças trabalharem juntas para cumprir uma instrução guardada na memória.',
   'caps. 22–23 — Registers and Busses · CPU Control Signals',
   '…control signals, so called because they control these components to work together in executing instructions stored in memory. … The CPU control signals are the strings.'),
 "onde_aparece": O('É o degrau em que a construção física encontra a descrição de linguagem: daqui para cima fala-se em instrução, montador, compilador. Abaixo, em fio.'),
 "onde_se_trava": O('O “controlador” soa como alguém que decide. Não é: ele é <b>mais circuito</b> — contador, decodificador e portas, feitos das mesmas peças de baixo. Enquanto restar um homenzinho dentro da máquina, a escada não fechou; e é justamente aqui que quase todo curso para de descer.'),
},

# ---- entram em 2026-08-27, com as arestas aceitas da leitura das dez ----
# Os campos de OFICIO destes quatro nascem SEM confirmacao: a de 2026-08-27
# cobriu os 17 que existiam naquele momento, e confirmacao nao se estende por
# analogia a texto que o autor nao leu. O selo dira "nao confirmado" ate ele os
# ler — que e o mecanismo funcionando, nao uma pendencia esquecida.

"ula": {
 "o_que_e": C('A parte da máquina que soma e subtrai, e faz mais algumas coisas úteis.',
   'cap. 21 — The Arithmetic Logic Unit',
   'The remainder of this chapter focuses on the most fundamental part of the CPU, which is known as the arithmetic logic unit, or ALU. This is the part of the CPU that adds and subtracts, as well as performing a couple of other useful tasks.'),
 "por_que_existe": S('Porque números grandes se somam em pedaços, um byte de cada vez, e cada pedaço precisa levar em conta o vai-um do anterior. A ULA faz essa sequência.',
   'cap. 21 — The Arithmetic Logic Unit',
   'these large numbers must be added and subtracted in bytes, starting with the least significant byte. Each subsequent 1-byte addition or subtraction must take into account the carry from the previous operation.'),
 "onde_aparece": O('É o “A” de qualquer diagrama de CPU que você já viu, e o que o seu profiler chama de <i>arithmetic throughput</i>. Também é onde nascem as flags: zero, sinal, vai-um — as que o seu <code>if</code> consulta sem você saber.', None),
 "onde_se_trava": O('Esperar que ela multiplique e dividir. Não multiplica: o próprio Petzold avisa que a circuitaria é possível e fica fora do livro, e que o 8080 não a tinha. Multiplicação, nesse nível, é <b>programa</b> — soma repetida —, não peça. Quem procura o multiplicador não acha e conclui que entendeu errado.', None),
},

"assembler": {
 "o_que_e": S('Um programa que lê o texto com as ordens, escritas em palavras, e o transforma na lista de instruções que a máquina executa.',
   'SICP §5.2.2 — The Assembler',
   'The assembler transforms the sequence of controller expressions for a machine into a corresponding list of machine instructions, each with its execution procedure.'),
 "por_que_existe": S('Porque o texto usa nomes no lugar de endereços, e um nome é uma promessa de endereço que ainda não existe. O montador lê o texto inteiro antes, só para descobrir a que lugar cada nome aponta.',
   'SICP §5.2.2 — The Assembler',
   'Before it can generate the instruction execution procedures, the assembler must know what all the labels refer to, so it begins by scanning the controller text to separate the labels from the instructions.'),
 "onde_aparece": O('Toda vez que você lê <code>jmp .loop</code> num desmontador e o <code>.loop</code> aparece como um endereço. E em todo compilador, na última etapa antes do binário.', None),
 "onde_se_trava": O('Achar que o montador “traduz palavra por palavra”. Ele não consegue: precisa de <b>duas passadas</b>, porque um salto para a frente aponta para um rótulo que ele ainda não viu. Quem não enxerga as duas passadas não entende por que montar é mais que substituir.', None),
},

"avaliador": {
 "o_que_e": S('Um programa que lê uma expressão e decide o que ela significa, passo a passo, usando os registradores da máquina.',
   'SICP §5.4 — The Explicit-Control Evaluator',
   'The explicit-control evaluator that we develop in this section shows how the underlying procedure-calling and argument-passing mechanisms used in the evaluation process can be described in terms of operations on registers and stacks.'),
 "por_que_existe": S('Porque assim uma linguagem feita para pessoas roda numa máquina que só entende instruções: o interpretador é a ponte, escrito quase na língua da máquina.',
   'SICP §5.4 — The Explicit-Control Evaluator',
   'the explicit-control evaluator can serve as an implementation of a Scheme interpreter, written in a language that is very similar to the native machine language of conventional computers.'),
 "onde_aparece": O('É o que roda quando você digita numa REPL. E é o desenho que a JVM, a CPython e o V8 estão executando por baixo — cada um com o seu laço de buscar, decidir, aplicar.', None),
 "onde_se_trava": O('A circularidade aparente: um interpretador de Scheme escrito em Scheme parece não explicar nada. Ele explica — desde que se veja que o de <b>dentro</b> está descrito em operações de registrador, e não em Scheme. É onde a escada se encontra consigo mesma, e é a passagem mais tonta de atravessar se ninguém disser isso.', None),
},

"paradigma": {
 "o_que_e": S('Um jeito de programar que aparece quando se muda o interpretador. Por exemplo: ensinar o interpretador a procurar sozinho entre várias respostas possíveis.',
   'SICP §4.3 — Variations on a Scheme: Nondeterministic Computing',
   'we extend the Scheme evaluator to support a programming paradigm called nondeterministic computing by building into the evaluator a facility to support automatic search'),
 "por_que_existe": S('Porque, sendo o interpretador um programa, dá para experimentar uma linguagem nova só mudando ele, antes de existir uma implementação de verdade.',
   'SICP §4.2 — Variations on a Scheme: Lazy Evaluation',
   'Now that we have an evaluator expressed as a Lisp program, we can experiment with alternative choices in language design simply by modifying the evaluator. Indeed, new languages are often invented by first writing an evaluator that embeds the new language within an existing high-level language.'),
 "onde_aparece": O('Prolog é a busca automática virada linguagem. <code>async/await</code> é uma mudança na ordem de avaliação. Avaliação preguiçosa é outra. Todas moram no mesmo lugar: na regra que decide o que avaliar e quando.', None),
 "onde_se_trava": O('Tratar paradigma como escola ou como gosto — “sou funcional”, “sou orientado a objetos”. Aqui ele é uma coisa <b>mecânica</b>: uma alteração no laço que avalia. Enquanto for identidade, não dá para perguntar a única coisa útil, que é <i>o que exatamente muda no interpretador</i>.', None),
},

"memoria": {
 "o_que_e": S('Muitos flip-flops em fileiras, cada fileira com um número na porta, o endereço. Dá para guardar um valor numa fileira e, depois, ler o que está lá.',
   'cap. 19 — An Assemblage of Memory',
   'This configuration of flip-flops, decoder, and selector is sometimes known as read/write memory because you can store values (that is, write them) and later determine what those values are (that is, read them). Because you can change the Address signals to any one of the eight values at will, this type of memory is more commonly known as random access memory, or RAM'),
 "por_que_existe": S('Porque escrever e ler acontecem em momentos diferentes, e alguma coisa precisa manter o que foi escrito intacto entre os dois.',
   'cap. 19 — An Assemblage of Memory',
   'We write and we later read. We save and we later retrieve. We store and we later access. The function of memory is to keep the information intact between those two events.'),
 "onde_aparece": O('Os pentes de RAM da sua máquina, e cada nível de cache antes deles. Também é o que o seu processo chama de <i>heap</i>: um espaço grande em que só o endereço distingue uma coisa da outra.', None),
 "onde_se_trava": O('O nome engana: <b>“aleatório” não quer dizer imprevisível</b> — quer dizer que qualquer posição custa o mesmo, em qualquer ordem. O contrário dela é a fita, que obriga a passar por tudo até chegar. Quem lê “aleatório” como “ao acaso” perde a única propriedade que dá nome à peça.', None),
},

"compilador": {
 "o_que_e": S('Um programa que traduz, de uma vez, um programa escrito para pessoas num programa equivalente escrito na língua da máquina.',
   'SICP §5.5 — Compilation',
   "A compiler for a given source language and machine translates a source program into an equivalent program (called the object program) written in the machine's native language."),
 "por_que_existe": S('Porque interpretar a cada vez custa caro: traduzido de uma vez, o programa roda muito mais rápido. O preço é que o interpretador é melhor para experimentar e corrigir.',
   'SICP §5.5 — Compilation',
   'Compared with interpretation, compilation can provide a great increase in the efficiency of program execution, as we will explain below in the overview of the compiler. On the other hand, an interpreter provides a more powerful environment for interactive program development and debugging, because the source program being executed is available at run time to be examined and modified.'),
 "onde_aparece": O('<code>gcc</code>, <code>rustc</code>, o JIT que a sua máquina virtual dispara quando um laço esquenta. E o <i>shader compiler</i> que roda quando você abre um jogo — a tela de “compilando shaders” é literalmente este degrau trabalhando.', None),
 "onde_se_trava": O('Achar que compilar e interpretar são times rivais, e que um venceu. O próprio SICP diz o contrário: os ambientes modernos usam <b>estratégia mista</b>, com procedimentos compilados e interpretados chamando uns aos outros. A pergunta útil não é qual é melhor — é <i>o que se ganha e o que se perde ao decidir cedo</i>.', None),
},

}

# Os quatro campos, na ordem em que a página os mostra, com o rótulo.
CAMPOS = [
    ("o_que_e",       "o que é"),
    ("por_que_existe","por que existe"),
    ("onde_aparece",  "onde aparece"),
    ("onde_se_trava", "onde se trava"),
]

CLASSES = {
    "a": ("citação",  "o campo é tradução fiel da passagem ao lado"),
    "b": ("síntese",  "resumo de passagem citada — a passagem vai junto para conferir"),
    "d": ("ofício",   "julgamento de quem ensina; nenhum livro escreve isto. "
                      "Não confirmado — aguarda a leitura do autor"),
}
