# -*- coding: utf-8 -*-
"""Os degraus da escada, e as arestas que alguém LEU.

Regra dura deste repositório: **uma aresta só entra com a frase que a
sustenta**, copiada da fonte, com capítulo. Não há aresta por plausibilidade,
por consenso ou por memória — nem a minha, nem a de um modelo.

O mapa começa quase vazio de propósito. Seis arestas lidas valem mais que
sessenta supostas, e a diferença aparece na página: cada seta abre a citação.
"""

FONTES = {
    "petzold": ("Charles Petzold, <i>Code: The Hidden Language of Computer "
                "Hardware and Software</i>, 2ª ed."),
    "sicp": ("Harold Abelson &amp; Gerald Jay Sussman, <i>Structure and "
             "Interpretation of Computer Programs</i>, 2ª ed."),
}

# nível: a altura do degrau na escada. Mesmo nível = mesma camada de abstração.
DEGRAUS = [
    ("eletroima",   "eletroímã",                  -1,
     "Um pedaço de ferro que vira ímã enquanto passa corrente. É o único "
     "degrau que não é feito de outro degrau: abaixo dele começa a física."),
    ("rele",        "relé",                        0,
     "Um interruptor que outro circuito aciona. É o primeiro componente que "
     "deixa um circuito controlar outro — e é daí que tudo sobe."),
    ("porta",       "porta lógica",                1,
     "AND, OR, NOR, inversor. A partir daqui o assunto deixa de ser eletricidade "
     "e passa a ser lógica."),
    ("somador",     "somador",                     2,
     "Soma dois bits e passa o vai-um adiante. É a primeira peça que faz "
     "<b>conta</b>, e é feita só de portas."),
    ("flipflop",    "flip-flop de nível",          2,
     "O primeiro circuito que <b>lembra</b>: a saída depende do que entrou "
     "antes, não só do que entra agora."),
    ("flipflop_b",  "flip-flop de borda",          3,
     "Lembra no <i>instante</i> da transição do relógio, e não enquanto ele "
     "está alto. É o que torna o tempo discreto."),
    ("contador",    "contador",                    4,
     "Conta pulsos de relógio. Vira o endereço que a máquina lê em seguida — "
     "o embrião do contador de programa."),
    ("registrador", "registrador",                 4,
     "Guarda um byte e o devolve quando mandarem. É a memória de trabalho da "
     "máquina, não a de armazenamento."),
    ("maquina",     "máquina de registradores",    5,
     "Registradores e operações, mais um controlador que sequencia as "
     "operações. É onde a construção física encontra a descrição de linguagem."),

    # --- entram em 2026-08-27, da leitura das dez que faltavam ---
    ("ula",         "ULA",                         3,
     "A parte da CPU que soma e subtrai. É a primeira peça que junta somador e "
     "portas num órgão com <b>nome de função</b>, e não de construção."),
    ("assembler",   "montador",                    6,
     "Traduz o texto do controlador da máquina numa lista de instruções, cada "
     "uma com o seu procedimento de execução."),
    ("avaliador",   "interpretador",               6,
     "O laço que decide o que uma expressão significa, escrito ele mesmo como "
     "uma máquina de registradores — e por isso <b>executável por ela</b>."),
    ("paradigma",   "paradigma",                   7,
     "Não é escola nem estilo: é o que aparece quando se <b>modifica o "
     "avaliador</b>. Trocar a regra de avaliação troca a linguagem."),

    # --- entram em 2026-10-03, com as seis famílias: a peça de que todo chip
    # é feito, e o circuito que anda sozinho ---
    ("transistor",  "transistor",                  0,
     "Uma chave de silício que a corrente aciona: faz o que o relé faz, sem "
     "peça que se mova, e é a peça de que todo chip é feito."),
    ("oscilador",   "oscilador (o relógio)",       1,
     "Um relé ligado à própria saída, que liga e desliga sozinho. Contar as "
     "voltas dele é medir o tempo."),

    # --- as duas reescritas, aceitas em 2026-08-27 ---
    ("memoria",     "memória (RAM)",               3,
     "Guarda muitos valores e devolve <b>aquele que o endereço pedir</b>. "
     "O acesso é livre: qualquer posição, a qualquer momento, ao mesmo custo."),
    ("compilador",  "compilador",                  7,
     "Traduz o programa-fonte num programa equivalente escrito na língua "
     "nativa da máquina. Em vez de interpretar a cada vez, ele traduz <b>uma "
     "vez só</b>."),
]

# (de, para, classe, fonte, referência, citação verificada)
ARESTAS = [
    ("eletroima", "rele", "construção", "petzold", 'cap. 7 — Telegraphs and Relays',
     'A relay is like a sounder in that an incoming current is used to power an electromagnet that pulls down a metal lever.'),
    ("rele", "porta", "construção", "petzold", 'cap. 8 — Relays and Gates',
     'These two relays wired in series are known as an AND gate because it is performing a Boolean AND operation.'),
    ("rele", "porta", "construção", "petzold", 'cap. 8 — Relays and Gates',
     'The next logic gate requires two relays that are wired in parallel, like this:'),
    ("rele", "porta", "construção", "petzold", 'cap. 8 — Relays and Gates',
     'A single relay wired in this way is called an inverter.'),
    ("porta", "somador", "construção", "petzold", 'cap. 14 — Adding with Logic Gates',
     'A half adder is an XOR gate and an AND gate'),
    ("porta", "flipflop", "construção", "petzold", 'cap. 19 — An Assemblage of Memory',
     'the level-triggered D-type flip-flop, which is made from an inverter, two AND gates, and two NOR gates'),
    ("flipflop", "flipflop_b", "construção", "petzold", 'cap. 17 — Feedback and Flip-Flops',
     'An edge-triggered D-type flip-flop is constructed from two stages of level-triggered D-type flip-flops, wired together this way:'),
    ("porta", "flipflop_b", "construção", "petzold", 'cap. 17 — Feedback and Flip-Flops',
     'Here’s the edge-triggered D-type flip-flop with preset and clear built entirely from six 3-input NOR gates and an inverter.'),
    ("flipflop_b", "contador", "construção", "petzold", 'cap. 20 — Automating Arithmetic',
     'This is a job for a counter built from a row of cascading flip-flops, such as the one you saw on page 237 of Chapter 17:'),
    ("flipflop_b", "registrador", "construção", "petzold", 'cap. 20 — Automating Arithmetic',
     'The counter providing the memory address is built from edge-triggered flip-flops, so it probably has a Clear input. The latch is built from edge-triggered flip-flops as well, and edge-triggered flip-flops have been used for generating the control signals.'),

    ("registrador", "maquina", "definição", "sicp", "§5.1 — Designing Register Machines",
     "To design a register machine, we must design its data paths (registers "
     "and operations) and the controller that sequences these operations. … If "
     "we view the arrows as wires and the X buttons as switches, the data-path "
     "diagram is very like the wiring diagram for a machine that could be "
     "constructed from electrical components."),
]

# A ÚNICA aresta com duas testemunhas independentes, de lados opostos da escada.
# Aceitas em 2026-08-27, depois da leitura das dez que faltavam. As três
# passaram na conferencia literal E no julgamento do autor — e as outras sete
# não entraram, cada uma com o motivo escrito em NAO_LIDO.
ARESTAS += [
    ("somador", "ula", "construção", "petzold", 'cap. 21 — The Arithmetic Logic Unit',
     'The Carry Out from the adder becomes the CY Out from the Add/Subtract module.'),
    ("maquina", "assembler", "dependência", "sicp", '§5.2.2 — The Assembler',
     'The assembler transforms the sequence of controller expressions for a machine into a corresponding list of machine instructions, each with its execution procedure.'),
    ("maquina", "avaliador", "dependência", "sicp", '§5.4 — The Explicit-Control Evaluator',
     'The evaluator can be executed by the register-machine simulator of section 5.2.'),
    ("avaliador", "paradigma", "construção", "sicp", '§4.3 — Variations on a Scheme: Nondeterministic Computing',
     'we extend the Scheme evaluator to support a programming paradigm called nondeterministic computing by building into the evaluator a facility to support automatic search'),

    # As duas REESCRITAS, aceitas em 2026-08-27. Elas entraram na lista dizendo
    # uma coisa que o livro não dizia — "RAM ← registrador" e "compilador ←
    # assembler e avaliador" — e entram na escada dizendo o que ele diz.
    ("flipflop", "memoria", "construção", "petzold", 'cap. 19 — An Assemblage of Memory',
     'This configuration of flip-flops, decoder, and selector is sometimes known as read/write memory'),
    ("avaliador", "compilador", "dependência", "sicp", '§5.5 — Compilation',
     'The compiler that we implement in this section translates programs written in Scheme into sequences of instructions to be executed using the explicit-control evaluator machine\'s data paths.'),
]

# As famílias (2026-10-03). O transistor entra na família das chaves pela
# frase do cap. 15; o oscilador entra como o relógio pela frase do cap. 17 —
# e a aresta "relógio ← oscilador", que a lista do que falta recusava como
# identidade, deixa de ser aresta: é o NOME da família, não uma composição.
ARESTAS += [
    ("transistor", "porta", "construção", "petzold", 'cap. 15 — Is This for Real?',
     'Vacuum tubes were originally developed for amplification, but they could also be used for switches in logic gates. The same goes for the transistor. Here’s a transistor-based AND gate structured much like the relay version:'),
    ("rele", "oscilador", "construção", "petzold", 'cap. 17 — Feedback and Flip-Flops',
     'The oscillator is constructed out of a relay or other switching component that’s flipping back and forth as fast as it can.'),
    ("oscilador", "flipflop_b", "dependência", "petzold", 'cap. 17 — Feedback and Flip-Flops',
     'The overall result is that the Data input is saved only when the Clock changes from 0 to 1.'),
]

# Aresta LIDA que o mapa NÃO desenha, com o motivo (2026-10-03): na grade de
# três colunas, a seta do oscilador (nível 1, à direita) ao flip-flop de borda
# (nível 3, à direita) cruzaria a seta porta → flip-flop de borda, que já
# existe. A aresta continua valendo: aparece na família relógio e no degrau
# flip-flop de borda, com a citação. O mapa diz, em texto, que ela está fora.
FORA_DO_MAPA = {("oscilador", "flipflop_b")}

SEGUNDA_TESTEMUNHA = {
    ("registrador", "maquina"): ("petzold", "caps. 22–23 — Registers and Busses · CPU Control Signals",
     "…control signals, so called because they control these components to work "
     "together in executing instructions stored in memory. … The CPU control "
     "signals are the strings."),
}

# Construção POR DENTRO: a peça é feita de peças da MESMA camada, então não é
# degrau — é a textura do degrau. Mesma regra: só entra com a frase da fonte.
# degrau=None ⇒ verificado, mas ainda não pousou em degrau nenhum.
# (degrau, peça, feita de, fonte, referência, citação verificada)
CONSTRUCAO = [
    ('eletroima', 'magnet', 'iron bar, wrap it with a couple of hundred turns of thin insulated wire',
     "petzold", 'cap. 7 — Telegraphs and Relays',
     'If you take an iron bar, wrap it with a couple of hundred turns of thin insulated wire, and then run a current through the wire, the iron bar becomes a magnet.'),
    ('porta', 'NOR', 'an OR gate followed by an inverter',
     "petzold", 'cap. 8 — Relays and Gates',
     'The NOR is the same as an OR gate followed by an inverter.'),
    ('porta', 'NAND', 'the inverse of the AND gate',
     "petzold", 'cap. 8 — Relays and Gates',
     'The NAND gate is drawn just like the AND gate but with a circle at the output, meaning the output is the inverse of the AND gate:'),
    ('porta', 'inverter', 'a NAND gate',
     "petzold", 'cap. 8 — Relays and Gates',
     'For example, here’s how to combine the inputs of a NAND gate to create an inverter:'),
    ('porta', 'AND gate', 'an inverter and a NAND gate',
     "petzold", 'cap. 8 — Relays and Gates',
     'You can use that inverter on the output of another NAND gate to make an AND gate.'),
    ('porta', 'XOR gate', 'an OR gate, a NAND gate, and an AND gate',
     "petzold", 'cap. 14 — Adding with Logic Gates',
     'The XOR gate is actually a combination of an OR gate, a NAND gate, and an AND gate'),
    ('somador', 'full adder', 'two half adders and an OR gate',
     "petzold", 'cap. 14 — Adding with Logic Gates',
     'Each full adder is two half adders and an OR gate'),
    ('registrador', '8-bit latch', 'flip-flops',
     "petzold", 'cap. 20 — Automating Arithmetic',
     'As you’ll recall, an 8-bit latch uses flip-flops to store an 8-bit value.'),
    ('registrador', 'register array', 'seven latches and seven tri-state buffers',
     "petzold", 'cap. 22 — Registers and Busses',
     'The following circuit contains seven latches and seven tri-state buffers. One 3-to-8 decoder is used to latch the incoming value into one of the registers, and another 3-to-8 decoder is used to enable one of the tri-state buffers to select a value from one of the registers:'),
    ('registrador', 'register array', 'latches for seven registers identified by the letters A, B, C, D, E, H, and L',
     "petzold", 'cap. 23 — CPU Control Signals',
     'The register array contains latches for seven registers identified by the letters A, B, C, D, E, H, and L.'),
    ('maquina', 'Triple-Byte Accumulator', 'a counter to access memory, an adder, and latches',
     "petzold", 'cap. 21 — The Arithmetic Logic Unit',
     'Chapter 20 described a Triple-Byte Accumulator that consisted of a counter to access memory, an adder, and latches.'),
    (None, 'seven-segment decoder', 'BCD decoder',
     "petzold", 'cap. 18 — Let’s Build a Clock!',
     'If your seven-segment display will always be displaying a digit, then a seven-segment decoder can be built from a BCD decoder as shown here:'),
    ('memoria', 'byte of memory', '8 bits of memory',
     "petzold", 'cap. 19 — An Assemblage of Memory',
     'it’s fairly easy to assemble an entire byte of memory by wiring together 8 bits of memory.'),
    ('memoria', '8×8 RAM array', 'eight 8×1 RAM arrays',
     "petzold", 'cap. 19 — An Assemblage of Memory',
     'if you have eight 8×1 RAM arrays and you connect all the Address signals together and all the Write signals together, you can make an 8×8 RAM array'),
    ('memoria', '16×8 RAM array', '16 of these 16×8 memory arrays',
     "petzold", 'cap. 19 — An Assemblage of Memory',
     'you’ll need 16 of these 16×8 memory arrays, wired up like this'),
    # Pousou em 2026-08-27: a ULA virou degrau, e esta construcao — que estava
    # verificada e sem lugar — passou a ser a textura DELE.
    ('ula', 'the entire arithmetic logic unit', 'the Add/Subtract module and the Logic module',
     "petzold", 'cap. 21 — The Arithmetic Logic Unit',
     'The entire arithmetic logic unit combines the Add/Subtract module and the Logic module with some rather messy support circuity:'),
    (None, 'PSW', 'accumulator and ALU flags',
     "petzold", 'cap. 24 — Loops, Jumps, and Calls',
     'It’s just the accumulator in one byte and the ALU flags in another byte.'),

    # Rótulo corrigido no julgamento (circular, anafórico ou duplicado);
    # a citacao e a mesma que passou na conferencia, intacta.
    (None, 'speaker wire', 'a pair of two insulated wires',
     "petzold", 'cap. 5 — Communicating Around Corners',
     'Speaker wire consists of a pair of two insulated wires conveniently stuck together, so it’s a good choice for our telegraph system.'),
    ('porta', 'prewired gate bank', 'relays',
     "petzold", 'cap. 14 — Adding with Logic Gates',
     'relays that have been prewired into various logic gates'),
    ('porta', 'logic gate', 'two relays',
     "petzold", 'cap. 14 — Adding with Logic Gates',
     'each of those gates consists of two relays'),
    (None, 'oscillator', 'quartz crystals',
     "petzold", 'cap. 17 — Feedback and Flip-Flops',
     'The oscillators in real computers are somewhat more sophisticated, however, consisting of quartz crystals wired in such a way that they vibrate very consistently and very quickly.'),
    (None, 'transistor', 'base, collector, and emitter',
     "petzold", 'cap. 18 — Let’s Build a Clock!',
     'The three letters stand for base, collector, and emitter.'),
    ('registrador', 'register', '8-bit latch',
     "petzold", 'cap. 22 — Registers and Busses',
     'These latches are called registers, and a primary purpose of these registers is to store bytes as they are processed by the ALU.'),
    ('registrador', '16-bit address', 'H and L registers',
     "petzold", 'cap. 22 — Registers and Busses',
     'The H and L registers form a 16-bit address—for example, in the MOV A,M instruction. When used in this way, HL is called a register pair.'),
]

# O que se sabe que existe e ainda NÃO foi lido. Aparece na página como buraco
# declarado — mapa que esconde o que falta mente sobre o próprio tamanho.
# O que falta, agora com ESTADO por item. Antes era só (afirmação, referência),
# e isso escondia a diferença entre "ninguém abriu o livro" e "abriu, leu, e a
# frase não sustenta". As dez foram lidas em 2026-08-27: três viraram aresta,
# uma já estava no repositório, e estas seis ficaram — cada uma com o motivo.
#
# (afirmação, referência CONFERIDA, estado, motivo)
NAO_LIDO = [
    ("instrução ← sinais de controle", "Petzold cap. 23", "lida, não sustenta",
     "A frase diz que os sinais <i>“control these components to work together in "
     "executing instructions”</i>: eles <b>executam</b> a instrução, não a "
     "compõem. E essa mesma citação já é a segunda testemunha de outra aresta."),
    ("sistema operacional ← máquina", "Petzold cap. 26", "procurada, não achada",
     "O capítulo define o que um sistema operacional <b>é</b> e o que ele "
     "oferece (API, interface), mas não afirma sobre o que ele se apoia. "
     "Nenhuma frase encontrada sustenta a aresta."),
    ("interpretação × compilação", "SICP §5.5", "lida, não é aresta",
     "O contraste está sustentado com folga — <i>“compared with interpretation, "
     "compilation can provide a great increase in the efficiency of program "
     "execution”</i> —, mas <b>×</b> não é uma relação que esta escada saiba "
     "desenhar: ela liga o que é feito do quê. Fica como nota, não como seta. "
     "A referência publicada dizia §5.5.7 e está corrigida."),
]
