# -*- coding: utf-8 -*-
"""Os degraus da vida de "Olá, Mundo!", e as passagens que alguém LEU.

Regra dura deste repositório, herdada do abstraction-ladder: **um degrau só
entra com a passagem que o sustenta**, copiada da fonte, com capítulo. Não há
degrau por plausibilidade, por consenso ou por memória — nem a minha, nem a de
um modelo. O gerador aborta se um degrau vier sem citação, ou se um selo
alegar fonte e não trouxer a passagem.

Cada degrau responde UMA pergunta: o que esta camada faz com o número. O
personagem é a frase "Olá, Mundo!" (onze letras, doze bytes), e a letra "O" é
seguida na trilha do alto da página, degrau a degrau.

A página é para quem não sabe nada. Cada degrau traz, ANTES de usar, as
palavras novas que vai usar (`palavras`: o que é, por que existe). Selo, nota
e buraco são DADO do catálogo: moram no README e em pesquisa/o-que-falta.md
(gerado), nunca na página. O gerador recusa palavra técnica antes do degrau
que a explica, e qualquer palavra de método na página.

Selos de procedência (campo `selo`):
  lida      — passagem copiada da fonte, conferível caractere a caractere;
  escada    — aresta que o abstraction-ladder já sustenta com citação lida;
  derivado  — conta feita pelo autor, conferível por qualquer tabela;
  oficio    — voz do autor, sem fonte, datada (responde quem assina);
  a_ler     — buraco declarado: o degrau existe, a passagem ainda não.
"""

FONTES = {
    "petzold": ("Charles Petzold, <i>Code: The Hidden Language of Computer "
                "Hardware and Software</i>, 2ª ed. (2022)"),
    "ladder": ("abstraction-ladder — a escada de abstrações, "
               "https://github.com/mateusalkimim/abstraction-ladder"),
}

# A trilha: o nome de cada degrau e, embaixo, em texto, o que o "O" já virou.
# Só palavras: ícone na trilha é enfeite que concorre com o conteúdo.
TRILHA = [
    ("lê-se",    "sinais"),
    ("frase",    "O"),
    ("tecla",    "79"),
    ("número",   "79"),
    ("bits",     "01001111"),
    ("o á",      "C3 A1"),
    ("relés",    "oito chaves"),
    ("conta",    "+1 = P"),
    ("endereço", "0109"),
    ("ordem",    "CD 05 00"),
    ("palavra",  "CALL 5"),
    ("luz",      "pontos"),
    ("laço",     "conserva"),
]

# Cada degrau: dict com
#   id, numero, regime, nome, titulo, tese, corpo, figura (chave em figuras.py),
#   origem (etiqueta curta na figura), regua (None | ("ouro"|"roxa"|"verde", texto)),
#   selo, fonte, ref, citacoes = [(en, pt)], notas = [str], derivado = str|None,
#   placa = dict(ciclo, diz, espera): o ciclo do traço do Olá, Mundo! que mostra
#   este degrau na placa, e o que o gerador confere nesse ciclo antes de ligar
DEGRAUS = [
    dict(
        id="d0", numero="0", regime="antes de qualquer máquina",
        nome="A frase já é um código", titulo="A frase já é um código",
        tese='Dizer <span class="frase">Olá, Mundo!</span> em voz alta é um código. '
             'Escrever é outro. Piscar uma lanterna é um terceiro.',
        corpo='Código aqui não é segredo: é um combinado sobre o que cada sinal '
              'quer dizer. Muda o meio, fica a mensagem. A lanterna já obriga a '
              'escolher: dois tipos de piscada, e nada mais.',
        palavras=[
            dict(palavra="sinal",
                 o_que_e="qualquer coisa que dá para perceber: um som, uma marca no papel, uma luz acesa.",
                 por_que="é o que viaja de quem fala até quem ouve; a mensagem em si não viaja sozinha."),
            dict(palavra="código",
                 o_que_e="um combinado sobre o que cada sinal quer dizer.",
                 por_que="para a mensagem atravessar um meio que não é a voz: o papel, a luz, o fio."),
        ],
        figura="tres_meios", origem=["Petzold, cap. 1"], regua=None,
        selo="lida", fonte="petzold", ref="cap. 1 — Best Friends",
        citacoes=[(
            "In this book, the word code usually means a system for transferring "
            "information among people, between people and computers, or within "
            "computers themselves.",
            "Neste livro, a palavra código geralmente significa um sistema para "
            "transferir informação entre pessoas, entre pessoas e computadores, "
            "ou dentro dos próprios computadores.")],
        objeto='correspondência um a um',
        matematica=[
            ('<span class="nome">código</span>: sinais → significados',
             'código leva cada sinal num significado só, e dá para voltar'),
        ],
        placa=dict(ciclo=1, diz='o primeiro passo: a máquina acorda e vai buscar o que tem de fazer',
                   espera={'fase': 'busca', 'endereco': 0}),
        notas=[], derivado=None,
    ),
    dict(
        id="d0b", numero="½", regime="tecla → número",
        nome="A tecla vira número", titulo="A tecla vira número",
        tese='Apertar a tecla O fecha uma chave. A máquina olha uma gaveta especial, '
             'a de número 8200, e encontra 79. A tecla virou número.',
        palavras=[
            dict(palavra="chave",
                 o_que_e="uma peça que abre ou fecha um caminho. O interruptor da luz é uma chave; cada tecla também.",
                 por_que="para ligar e desligar alguma coisa com um toque."),
            dict(palavra="gaveta",
                 o_que_e="um lugar dentro da máquina onde cabe um número, com um número na porta para ser achado de novo.",
                 por_que="a máquina não enxerga a tecla; ela só sabe olhar gavetas. O teclado deixa o seu número numa delas."),
        ],
        corpo='A máquina olha a gaveta o tempo todo e quase sempre encontra zero: '
              'ninguém apertou. O livro chama isso de consultar o teclado. Quando '
              'encontra 79, copia para a tela e zera a gaveta, pronta para a '
              'próxima tecla.',
        figura="tecla_vira_numero", origem=["Petzold, cap. 25"],
        regua=None, selo="lida", fonte="petzold", ref="cap. 25 — Peripherals",
        citacoes=[
            ("The accumulator would then contain a code indicating what key has "
             "been pressed.",
             "O acumulador passaria então a conter um código indicando qual tecla "
             "foi apertada."),
            ("It's tempting to assume that this code is the ASCII code for the key. "
             "But it's neither practical nor desirable to design hardware that "
             "figures out the ASCII code.",
             "É tentador supor que esse código é o código ASCII da tecla. Mas não é "
             "prático nem desejável projetar hardware que descubra o código ASCII."),
            ("One approach is for the program to check the keyboard very frequently. "
             "This approach is called polling.",
             "Uma abordagem é o programa consultar o teclado com muita frequência. "
             "Isso se chama polling."),
        ],
        objeto="uma regra do tempo nos números: 0 enquanto solta, o código enquanto apertada",
        matematica=[
            ('<span class="nome">tecla</span>(<i>t</i>) = 79 enquanto o O está apertado, e 0 depois',
             'tecla de tê é igual a setenta e nove enquanto o O está apertado, e zero depois'),
        ],
        placa=dict(programa="eco", ciclo=22, diz="a gaveta 8200 entrega o 79 à máquina; dez passos depois ele está na tela",
                   espera=dict(dado_de="teclado", dado=0x4F)),
        notas=["Nesta máquina a gaveta 8200h entrega direto o número da letra, porque o "
               "navegador já fez a conta. Num teclado de verdade o código é da tecla, "
               "não da letra, e um programa pequeno faz a tradução: o livro avisa. "
               "Decisão nossa, declarada."],
        derivado=None,
    ),
    dict(
        id="d1", numero="1", regime="letra → número",
        nome="Cada letra recebe um número", titulo="Cada letra recebe um número",
        tese='O <b>O</b> vale 79. O <b>l</b>, 108. A vírgula vale 44 e o espaço, '
             '32. A frase vira uma fila de onze números.',
        corpo='Não há nada de <b>O</b> no 79. É uma posição numa tabela que o '
              'mundo inteiro combinou usar. Por isso o mesmo <b>O</b> é 79 em '
              'qualquer máquina.',
        palavras=[
            dict(palavra="tabela",
                 o_que_e="uma lista em que cada letra tem o seu número ao lado, como uma lista de chamada.",
                 por_que="a máquina só guarda números; a tabela é o combinado que diz qual número é qual letra."),
        ],
        figura="tabela_numeros", origem=["Petzold, cap. 13"],
        regua=None, selo="lida", fonte="petzold", ref="cap. 13 — From ASCII to Unicode",
        citacoes=[(
            "The biggest advantage of UTF-8 is that it's backward compatible with "
            "ASCII. This means that a file consisting solely of 7-bit ASCII codes "
            "stored as bytes is automatically a UTF-8 file.",
            "A maior vantagem do UTF-8 é ser compatível com o ASCII: um arquivo só "
            "de códigos ASCII de 7 bits, guardados como bytes, já é automaticamente "
            "um arquivo UTF-8.")],
        objeto='correspondência um a um entre letras e números',
        matematica=[
            ('<span class="nome">número</span>(O) = 79',
             'número de O é igual a setenta e nove'),
        ],
        placa=dict(ciclo=8, diz='o número 79, escrito 4F, que é a letra O, chega à máquina',
                   espera={'dado_para': 'IL2', 'dado': 79}),
        notas=["A passagem que define a tabela ASCII em si está no mesmo capítulo "
               "e ainda não foi copiada."],
        derivado="os onze números, calculados pelo autor; qualquer tabela Unicode confere",
    ),
    dict(
        id="d2", numero="2", regime="número → bits",
        nome="Cada número vira oito casas", titulo="Cada número vira oito casas de sim ou não",
        tese='79 vira <span class="mono">01001111</span>. Oito casas, cada uma só '
             '0 ou 1. Com oito casas cabem 256 coisas diferentes.',
        corpo='É a mesma ideia de 79 = 70 + 9, só que cada casa vale o dobro da '
              'vizinha, não dez vezes. 256 é o número de combinações, não um '
              'tamanho.',
        palavras=[
            dict(palavra="casa",
                 o_que_e="uma posição na escrita de um número. Em 79, o 7 está numa casa e o 9 na outra.",
                 por_que="é a casa que diz quanto cada algarismo vale: o 7 de 79 vale setenta."),
            dict(palavra="bit",
                 o_que_e="uma casa que só aceita 0 ou 1.",
                 por_que="é a menor quantidade de informação que existe, e é o que uma chave sabe guardar: desligada ou ligada."),
            dict(palavra="byte",
                 o_que_e="oito bits lado a lado.",
                 por_que="é o tamanho de uma letra, e o pedaço que a máquina move de cada vez."),
        ],
        figura="byte_79", origem=["Petzold, caps. 11 e 12"], regua=None,
        selo="lida", fonte="petzold", ref="cap. 11 — Bit by Bit by Bit · cap. 12 — Bytes and Hexadecimal",
        citacoes=[(
            "As an 8-bit quantity, a byte can take on values from 00000000 through "
            "11111111, which can represent decimal numbers from 0 through 255, or "
            "one of 2<sup>8</sup>, or 256, different things.",
            "Como quantidade de 8 bits, um byte vai de 00000000 a 11111111, o que "
            "representa os números de 0 a 255, ou uma entre 2⁸, isto é, 256, "
            "coisas diferentes.")],
        objeto='notação posicional na base dois',
        matematica=[
            ('79 = 64 + 8 + 4 + 2 + 1',
             'setenta e nove é igual a sessenta e quatro, mais oito, mais quatro, mais dois, mais um'),
            ('2<sup>8</sup> = 256',
             'dois elevado a oito é igual a duzentos e cinquenta e seis: o tamanho do conjunto das listas de oito zeros ou uns'),
        ],
        placa=dict(ciclo=9, diz='os oito pontos da fileira de dados, acesos e apagados: 0 1 0 0 1 1 1 1',
                   espera={'dado': 79, 'dado_para': 'RAM'}),
        notas=[], derivado=None,
    ),
    dict(
        id="d3", numero="2½", regime="o degrau que o personagem trouxe",
        nome="O á não cabe em um byte", titulo="O á não cabe em um byte",
        tese='225 é maior que 127, e o combinado original só tinha 128 letras, sem '
             'acento. O <b>á</b> custa dois bytes.',
        corpo='Onze letras, doze bytes. Byte não é letra: uma letra pode custar um, '
              'dois, três ou quatro. Quem conta bytes para contar letras erra, e a '
              'web inteira já errou isso.',
        figura="bits_do_a", origem=["Petzold, cap. 13"],
        regua=None, selo="lida", fonte="petzold",
        ref="cap. 13, com o £ (U+00A3) como exemplo; o á (U+00E1) está na mesma faixa",
        citacoes=[(
            "Thus, in UTF-8 the two bytes C2h and A3h represent the British £ sign. "
            "It seems a shame to require 2 bytes to encode what is essentially just "
            "1 byte of information, but it's necessary for the rest of UTF-8 to work.",
            "Assim, em UTF-8 os dois bytes C2 e A3 representam o sinal de libra. "
            "Parece pena gastar 2 bytes para codificar o que é essencialmente 1 byte "
            "de informação, mas é necessário para o resto do UTF-8 funcionar.")],
        objeto='código de comprimento variável, sem palavra que seja começo de outra',
        matematica=[
            ('<span class="nome">bytes</span>(o) = 1, <span class="nome">bytes</span>(á) = 2',
             'bytes de o é igual a um; bytes de á é igual a dois'),
        ],
        placa=dict(ciclo=19, diz='na tela desta máquina o á cabe num byte só, E1; os dois bytes são do arquivo',
                   espera={'dado': 225, 'dado_para': 'RAM'}),
        notas=[], derivado="C3 A1, pela regra da segunda linha da tabela do cap. 13",
    ),
    dict(
        id="d4", numero="3", regime="bit → corrente",
        nome="Cada casa vira corrente", titulo="Cada casa vira corrente num relé",
        tese='O 1 é corrente passando; o 0 é corrente parada. Oito relés '
             'enfileirados seguram o <b>O</b>; noventa e seis seguram a frase.',
        palavras=[
            dict(palavra="corrente",
                 o_que_e="eletricidade andando por dentro de um fio, como água andando por um cano.",
                 por_que="é ela que faz a lâmpada acender e, aqui, a chave virar."),
            dict(palavra="relé",
                 o_que_e="uma chave que uma corrente aciona: a corrente de um fio fecha o caminho de outro.",
                 por_que="é a primeira peça que deixa uma corrente mandar em outra, sem dedo nenhum."),
            dict(palavra="limiar",
                 o_que_e="a linha que separa pouco de muito. Acima dela a corrente conta como 1; abaixo, como 0.",
                 por_que="a corrente nunca é exatamente igual; a linha é o que faz dois valores diferentes virarem o mesmo sinal."),
        ],
        corpo='O número não está no relé. O relé só sabe passar ou não passar; '
              'somos nós que combinamos que passar vale 1. Oito relés, oito '
              'casas: o <b>O</b> inteiro cabe numa fileira. Como relés viram '
              'portas e contas é a história da outra página, a escada.',
        figura="oito_reles", origem=["Petzold, caps. 7 e 8"],
        regua=("ouro", "aqui deixa de ser escrita e passa a ser eletricidade"),
        selo="escada", fonte="ladder",
        ref="eletroímã → relé (Petzold cap. 7) · relé → porta lógica (cap. 8), com o instrumento “dois relés viram uma porta”",
        citacoes=[(
            "These two relays wired in series are known as an AND gate because it is "
            "performing a Boolean AND operation.",
            "Esses dois relés ligados em série são conhecidos como porta AND, porque "
            "executam a operação booleana E.")],
        objeto='limiar: um intervalo inteiro de tensões vira um símbolo só',
        matematica=[
            ('<span class="nome">bit</span>(<i>v</i>) = 1 se <i>v</i> ≥ 2 volts, e 0 se <i>v</i> ≤ 0,8 volt',
             'bit de vê é igual a um se vê é maior ou igual a dois volts, e igual a zero se vê é menor ou igual a zero vírgula oito volt'),
        ],
        placa=dict(ciclo=9, diz='cada ponto aceso na fileira é um fio com corrente passando',
                   espera={'dado': 79}),
        notas=[], derivado=None,
    ),
    dict(
        id="d5", numero="4", regime="corrente → conta e lembrança",
        nome="Os bits somam e ficam parados", titulo="Os bits aprendem a somar e a ficar parados",
        tese='Portas ligadas de um jeito somam dois bytes. Ligadas de outro, '
             'seguram um bit depois que a entrada some.',
        palavras=[
            dict(palavra="porta lógica",
                 o_que_e="uma peça feita de chaves que responde sim ou não ao que chega nela. Duas chaves em fila só passam corrente com as duas fechadas: é uma porta.",
                 por_que="é com perguntas de sim ou não, ligadas umas às outras, que se monta uma conta."),
            dict(palavra="estado",
                 o_que_e="o jeito em que uma peça está agora: o que ela guarda neste instante.",
                 por_que="uma peça que lembra tem estado; uma que só responde não tem."),
        ],
        corpo='Somar 1 ao <b>O</b> dá <b>P</b>, a letra seguinte: a tabela foi '
              'feita para isso funcionar. Agora o número pode ser operado e pode '
              'esperar. Lembrar é o que permite o próximo degrau.',
        figura="somador_flipflop", origem=["Petzold, caps. 14, 17, 19 a 21"],
        regua=None, selo="escada", fonte="ladder",
        ref="porta → somador (cap. 14) · porta → flip-flop (caps. 17 e 19) · flip-flop de borda → contador e registrador (cap. 20) · somador → ULA (cap. 21)",
        citacoes=[(
            "A half adder is an XOR gate and an AND gate",
            "Um meio-somador é uma porta XOR e uma porta AND.")],
        objeto='aritmética módulo 256, e estado que depende do anterior',
        matematica=[
            ('(79 + 1) <span class="nome">mod</span> 256 = 80',
             'setenta e nove mais um, módulo duzentos e cinquenta e seis, é igual a oitenta'),
            ('<i>s</i><sub><i>t</i>+1</sub> = <span class="nome">f</span>(<i>s</i><sub><i>t</i></sub>, <i>x</i><sub><i>t</i></sub>)',
             'o estado no instante tê mais um é f de: o estado no instante tê, e a entrada no instante tê'),
        ],
        placa=dict(ciclo=11, diz='uma peça guarda onde a máquina está e outra soma 1: lembrar e contar',
                   espera={'nota_comeca': 'INX'}),
        notas=[], derivado=None,
    ),
    dict(
        id="d6", numero="5", regime="byte → endereço",
        nome="Cada byte ganha um endereço", titulo="Cada byte ganha um lugar com número",
        tese='Memória é uma fileira de gavetas, cada uma com um número na porta. '
             'O <b>O</b> fica na gaveta 0109; o <b>l</b>, na 010A.',
        corpo='Agora há dois números por letra: o que ela vale e onde ela está. A '
              'ordem das letras virou ordem de endereços. Ler a frase é percorrer '
              'gavetas vizinhas.',
        palavras=[
            dict(palavra="memória",
                 o_que_e="muitas gavetas em fileira, cada uma com um byte dentro.",
                 por_que="para a frase inteira ficar guardada enquanto a máquina trabalha nela, uma letra por gaveta."),
            dict(palavra="endereço",
                 o_que_e="o número na porta de uma gaveta.",
                 por_que="para achar de novo o que foi guardado, sem procurar gaveta por gaveta."),
        ],
        figura="gavetas", origem=["Petzold, cap. 19"],
        regua=None, selo="lida", fonte="petzold", ref="cap. 19 — An Assemblage of Memory",
        citacoes=[(
            "That's called writing to memory, and the value of Data In is said to "
            "be stored in memory at the address 010.",
            "Isso se chama escrever na memória, e diz-se que o valor da entrada fica "
            "guardado na memória no endereço 010.")],
        objeto='a memória é uma regra que leva cada endereço num byte',
        matematica=[
            ('<span class="nome">mem</span>(0109) = 4F',
             'mem de zero, um, zero, nove é igual a quatro-efe, que vale setenta e nove'),
        ],
        placa=dict(ciclo=9, diz='a máquina aponta a gaveta 8000 e guarda nela o 4F',
                   espera={'endereco': 32768, 'endereco_de': 'HL', 'dado_para': 'RAM'}),
        notas=[], derivado="os endereços seguem o programa do cap. 27, deslocado para a nossa frase",
    ),
    dict(
        id="d7", numero="6", regime="número → ordem",
        nome="Um número é lido como ordem", titulo="Um número é lido como ordem, não como quantidade",
        tese='Na mesma memória, ao lado das letras, moram outros bytes. '
             '<span class="mono">CD</span> não é letra: é a ordem “chame”. '
             '<span class="mono">C9</span> é “volte”.',
        palavras=[
            dict(palavra="ordem",
                 o_que_e="um número que a máquina lê como “faça isto”: some, copie, guarde, chame, volte. O livro chama de instrução.",
                 por_que="sem ordens a máquina só guardaria números; é a ordem que a põe a fazer alguma coisa com eles."),
            dict(palavra="programa",
                 o_que_e="uma fila de ordens, uma depois da outra, guardada na memória como qualquer outra coisa.",
                 por_que="é como uma pessoa diz à máquina o que fazer, de uma vez, para a máquina fazer sozinha."),
            dict(palavra="contador de programa",
                 o_que_e="uma gaveta especial da máquina que guarda o endereço da próxima ordem.",
                 por_que="para a máquina saber qual byte ler como ordem agora, e qual vem depois."),
        ],
        corpo='Nada no byte diz se ele é letra ou ordem. O que decide é para onde o '
              'contador de programa aponta, e esse contador também é um número '
              'guardado na máquina. A máquina se governa com a mesma matéria que '
              'governa.',
        figura="dezesseis_bytes", origem=["Petzold, caps. 23 e 27"],
        regua=("roxa", "aqui deixa de ser circuito e passa a ser linguagem"),
        selo="lida", fonte="petzold", ref="cap. 27 — Coding · cap. 23 — CPU Control Signals",
        citacoes=[
            ("The first 3 bytes are the LXI instruction, the next 2 are the MVI "
             "instruction, the next 3 are the CALL instruction, and the next is the "
             "RET instruction. The last 7 bytes are the ASCII characters for the five "
             "letters of “Hello,” the exclamation point, and the dollar sign.",
             "Os 3 primeiros bytes são a instrução LXI, os 2 seguintes a MVI, os 3 "
             "seguintes a CALL, e o próximo a RET. Os últimos 7 bytes são os "
             "caracteres ASCII das cinco letras de “Hello”, o ponto de exclamação e "
             "o cifrão."),
            ("A value called the program counter. This is the 16-bit value that "
             "accesses instructions. It starts at 0000h and sequentially increases "
             "until a HLT instruction.",
             "Um valor chamado contador de programa. É o valor de 16 bits que acessa "
             "as instruções. Começa em 0000 e cresce em sequência até uma instrução "
             "HLT."),
        ],
        objeto='a máquina é uma regra de passo: do estado de agora para o próximo',
        matematica=[
            ('próximo = <span class="nome">passo</span>(<i>contador</i>, <i>A</i>, mem)',
             'o próximo estado é passo de: o contador de programa, o número guardado em A, e a memória'),
        ],
        placa=dict(ciclo=7, diz='o contador de programa aponta a gaveta 0004 e o byte 36 é lido como ordem: guarde a letra',
                   espera={'dado': 54, 'dado_para': 'IL1'}),
        notas=["O programa do livro é de antes do Unicode; um CP/M real não "
               "mostraria o á. A versão com “Olá, Mundo!” nas gavetas é adaptação "
               "do autor."],
        derivado=None,
    ),
    dict(
        id="d8", numero="7", regime="palavras → ordens",
        nome="As ordens são escritas com palavras", titulo="Alguém escreve as ordens com palavras",
        tese='Ninguém decora que “chame” é <span class="mono">CD</span>. Escreve-se '
             '<span class="mono">CALL 5</span> num texto, e o montador troca cada '
             'palavra pelo byte certo.',
        palavras=[
            dict(palavra="montador",
                 o_que_e="um programa que lê um texto com as ordens escritas em palavras e troca cada palavra pelo byte certo.",
                 por_que="porque pessoa lembra palavra, e máquina só lê número. Alguém tem de fazer a troca, e um programa faz sem errar."),
            dict(palavra="sistema operacional",
                 o_que_e="um programa que já mora na máquina e faz serviços para os outros programas, como mostrar texto na tela.",
                 por_que="para cada programa novo não precisar saber como a tela funciona."),
        ],
        corpo='É aqui que a delegação começa: a pessoa escreve a intenção, a máquina '
              'executa. O sistema operacional já sabe fazer serviços, como mostrar '
              'texto, para que cada programa não precise saber.',
        figura="montador", origem=["Petzold, cap. 27"],
        regua=None, selo="lida", fonte="petzold", ref="cap. 27 — Coding",
        citacoes=[(
            "An assembler such as ASM.COM reads an assembly-language program (often "
            "called a source-code file) and writes out to a file containing machine "
            "code—an executable file.",
            "Um montador como o ASM.COM lê um programa em linguagem de montagem (o "
            "chamado arquivo-fonte) e escreve um arquivo com código de máquina: um "
            "executável.")],
        objeto='tradução que preserva significado',
        matematica=[
            ('<span class="nome">roda</span>(<span class="nome">montar</span>(texto)) = <span class="nome">significado</span>(texto)',
             'rodar o que foi montado do texto dá o mesmo que o significado do texto'),
        ],
        placa=dict(ciclo=7, diz="na listagem ao lado, MVI M, 'O' virou 36 4F; a máquina só vê os bytes",
                   espera={'dado': 54, 'dado_para': 'IL1'}),
        notas=[], derivado=None,
    ),
    dict(
        id="d9", numero="8", regime="execução → tela",
        nome="A ordem vira pontos de luz", titulo="A ordem vira pontos de luz",
        tese='A tela também é memória: cada três bytes são um ponto colorido. '
             'Mostrar o <b>o</b> é escrever números nas gavetas certas desse bloco.',
        palavras=[
            dict(palavra="pixel",
                 o_que_e="um ponto da tela, pequeno demais para ver sozinho, com uma cor só.",
                 por_que="a tela não desenha letras; ela acende pontos, e a letra é o que os pontos formam juntos."),
        ],
        corpo='Sessenta vezes por segundo a tela lê o bloco e acende. '
              '<span class="frase">Olá, Mundo!</span> volta a ser coisa que a gente '
              'lê, feita de números. Como o 79 vira o desenho do <b>O</b> é a '
              'próxima pergunta, ainda sem resposta nesta página.',
        figura="pixels", origem=["Petzold, caps. 12 e 25"],
        regua=("verde", "aqui deixa de ser número e volta a ser luz"),
        selo="lida", fonte="petzold", ref="cap. 25 — Peripherals · cap. 12 (pixel = três bytes)",
        citacoes=[
            ("The contents of the display are stored in a special block of memory, "
             "and the individual pixels of the display are refreshed sequentially, "
             "starting left to right with the row at the top, and continuing down the "
             "display.",
             "O conteúdo da tela fica guardado num bloco especial de memória, e os "
             "pixels são atualizados em sequência, da esquerda para a direita a partir "
             "da linha de cima, descendo pela tela."),
            ("For a 1920 × 1080 display, each of the 2 million pixels requires 3 bytes "
             "for the red, green, and blue components, for a total of 6 million bytes, "
             "or 6 megabytes.",
             "Numa tela de 1920 × 1080, cada um dos 2 milhões de pixels precisa de 3 "
             "bytes, para o vermelho, o verde e o azul: 6 milhões de bytes, ou 6 "
             "megabytes."),
        ],
        objeto='regra que leva cada ponto da grade numa cor',
        matematica=[
            ('<span class="nome">cor</span>(3, 4) = 16 23 3F',
             'cor de três e quatro é igual a um-seis, dois-três, três-efe: vermelho, verde e azul'),
        ],
        placa=dict(ciclo=59, diz='a última letra entra na tela e a frase inteira está lá, feita de números',
                   espera={'dado': 33, 'dado_para': 'RAM'}),
        notas=["Fonte tipográfica e rasterização (do 79 ao desenho do O): o "
               "Petzold não cobre. Buraco declarado."],
        derivado=None,
    ),
]

# A folha de convenções: antecede o primeiro símbolo. Ensina a CLASSE do
# sinal, nunca o verbete. Formato: classe · o que é aqui · exemplo · lê-se.
CONVENCOES = [
    ("nome em letras retas, com parênteses",
     "uma regra com nome, aplicada ao que está entre parênteses",
     '<span class="nome">número</span>(o)', "número de o"),
    ("letra inclinada minúscula",
     "uma quantidade que varia",
     '<i>v</i>, <i>t</i>', "vê, tê"),
    ("índice embaixo",
     "em qual instante, ou em qual posição",
     '<i>s</i><sub><i>t</i></sub>', "ésse no instante tê"),
    ("número pequeno em cima",
     "quantas vezes multiplicar o número por ele mesmo",
     '2<sup>8</sup>', "dois elevado a oito"),
    ('<span class="nome">mod</span>',
     "o resto da divisão por",
     '(79 + 1) <span class="nome">mod</span> 256', "setenta e nove mais um, módulo duzentos e cinquenta e seis"),
    ("seta entre dois conjuntos",
     "uma regra que leva cada coisa da esquerda numa coisa da direita",
     'sinais → significados', "leva sinais em significados"),
    ("número em hexadecimal",
     "um número escrito com os algarismos de 0 a 9 e as letras de A a F, que valem de 10 a 15",
     '4F', "quatro-efe, que vale setenta e nove"),
]

# O fecho: a tabela do que cada degrau conserva e esquece. Não é degrau — é a
# régua que atravessa todos: cada camada é uma promessa "pode esquecer o resto,
# isto eu garanto".
FECHO = dict(
    id="d10", nome="O laço",
    titulo="Em cada degrau, uma coisa se conserva e uma se esquece",
    tese='A matemática se refere ao mundo por aquilo que se conserva. Cada camada '
         'é uma promessa: “pode esquecer o resto, isto eu garanto”.',
    corpo='A escada inteira é a cadeia dessas promessas, e a execução é o que '
          'sobra quando todas foram cumpridas.',
    origem=[],
    linhas=[
        ("0 código", "a mensagem", "o meio", "cap. 1"),
        ("½ tecla → número", "o código da letra", "a chave, o dedo", "cap. 25"),
        ("1 letra → número", "qual letra é", "forma e som", "cap. 13"),
        ("2 número → bits", "o número exato", "a base dez", "caps. 11, 12"),
        ("2½ o á", "a letra e as 128 antigas", "“um byte, uma letra”", "cap. 13"),
        ("3 bit → corrente", "0 e 1", "a física", "escada"),
        ("4 conta e lembrança", "a aritmética", "os relés", "escada"),
        ("5 endereço", "a ordem das letras", "o tempo", "cap. 19"),
        ("6 número → ordem", "a matéria comum", "“o que fazer” e “sobre o quê”", "caps. 23, 27"),
        ("7 palavras → ordens", "o significado", "as palavras", "cap. 27"),
        ("8 ordem → luz", "a forma reconhecível", "o número", "caps. 12, 25"),
    ],
)

# Buracos declarados: o que o mapa sabe que falta e ainda não abriu. Mapa que
# esconde o que falta mente sobre o próprio tamanho.
A_LER = [
    ("do 79 ao desenho do O", "fonte tipográfica e rasterização",
     "sem passagem no Petzold; outro livro, ou ofício do autor, datado"),
    ("a tabela ASCII em si", "Petzold cap. 13",
     "está no capítulo e não foi copiada; os números do degrau 1 são derivados"),
    ("o á em 1978", "Petzold cap. 27",
     "o programa é de antes do Unicode; a versão com “Olá, Mundo!” é adaptação do autor"),
    ("da tela à web", "Petzold cap. 27",
     "o capítulo termina com a mesma frase em JavaScript numa página; ainda não lido"),
]
