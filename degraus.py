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

# A trilha: o que o "o" já virou em cada degrau. `tok` é HTML curto.
TRILHA = [
    ("símbolos", '<span class="tok serif">lê-se</span>'),
    ("frase",    '<span class="tok serif">O</span>'),
    ("número",   '<span class="tok">79</span>'),
    ("bits",     '<span class="tok">01001111</span>'),
    ("o á",      '<span class="tok">C3 A1</span>'),
    ("relés",    '<span class="tok"><span class="rl"><i></i><i class="u"></i><i></i><i></i><i class="u"></i><i class="u"></i><i class="u"></i><i class="u"></i></span></span>'),
    ("conta",    '<span class="tok">+1 = P</span>'),
    ("endereço", '<span class="tok">0109</span>'),
    ("ordem",    '<span class="tok">CD 05 00</span>'),
    ("palavra",  '<span class="tok">CALL 5</span>'),
    ("luz",      '<span class="tok"><span class="px"><i class="v"></i><i></i><i></i><i></i><i class="v"></i><i></i><i class="v"></i><i class="v"></i><i class="v"></i><i></i><i></i><i class="v"></i><i class="v"></i><i class="v"></i><i></i><i></i><i class="v"></i><i class="v"></i><i class="v"></i><i></i><i class="v"></i><i></i><i></i><i></i><i class="v"></i></span></span>'),
    ("laço",     '<span class="tok serif">∞</span>'),
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
        placa=dict(ciclo=1, diz='o primeiro ciclo: o PC põe 0000h no barramento e a RAM entrega o primeiro byte',
                   espera={'fase': 'busca', 'endereco': 0}),
        notas=[], derivado=None,
    ),
    dict(
        id="d1", numero="1", regime="letra → número",
        nome="Cada letra recebe um número", titulo="Cada letra recebe um número",
        tese='O <b>O</b> vale 79. O <b>l</b>, 108. A vírgula vale 44 e o espaço, '
             '32. A frase vira uma fila de onze números.',
        corpo='Não há nada de <b>O</b> no 79. É uma posição numa tabela que o '
              'mundo inteiro combinou usar. Por isso o mesmo <b>O</b> é 79 em '
              'qualquer máquina.',
        figura="tabela_numeros", origem=["Petzold, cap. 13", "números: derivados, conferíveis"],
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
        placa=dict(ciclo=8, diz='o byte 4F, que é a letra O, chega ao Instruction Latch 2',
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
        placa=dict(ciclo=9, diz='os oito pontos do barramento de dados: 0 1 0 0 1 1 1 1',
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
        figura="bits_do_a", origem=["Petzold, cap. 13", "bytes do á: derivados pela mesma regra"],
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
        placa=dict(ciclo=19, diz='o á entra na tela como um byte só, E1: a célula é nossa, o UTF-8 é do arquivo',
                   espera={'dado': 225, 'dado_para': 'RAM'}),
        notas=[], derivado="C3 A1, pela regra da segunda linha da tabela do cap. 13",
    ),
    dict(
        id="d4", numero="3", regime="bit → corrente",
        nome="Cada casa vira corrente", titulo="Cada casa vira corrente num relé",
        tese='O 1 é corrente passando; o 0 é corrente parada. Oito relés '
             'enfileirados seguram o <b>O</b>; noventa e seis seguram a frase.',
        corpo='O número não está no relé. O relé só sabe passar ou não passar; '
              'somos nós que combinamos que passar vale 1. Daqui para cima, a '
              'escada que já existe sobe com citação e instrumento.',
        figura="oito_reles", origem=["Petzold, caps. 7 e 8", "já na escada: eletroímã → relé → porta"],
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
        placa=dict(ciclo=9, diz='cada ponto aceso no barramento é um fio com corrente; o medidor de limiar ainda vem',
                   espera={'dado': 79}),
        notas=[], derivado=None,
    ),
    dict(
        id="d5", numero="4", regime="corrente → conta e lembrança",
        nome="Os bits somam e ficam parados", titulo="Os bits aprendem a somar e a ficar parados",
        tese='Portas ligadas de um jeito somam dois bytes. Ligadas de outro, '
             'seguram um bit depois que a entrada some.',
        corpo='Somar 1 ao <b>O</b> dá <b>P</b>, a letra seguinte: a tabela foi '
              'feita para isso funcionar. Agora o número pode ser operado e pode '
              'esperar. Lembrar é o que permite o próximo degrau.',
        figura="somador_flipflop", origem=["Petzold, caps. 14, 17, 19 a 21", "já na escada, com cinco instrumentos"],
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
        placa=dict(ciclo=11, diz='HL guarda o endereço e o incrementador soma 1: lembrar e contar',
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
        figura="gavetas", origem=["Petzold, cap. 19", "endereços: derivados do programa do cap. 27"],
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
        placa=dict(ciclo=9, diz='HL põe 8000h no barramento de endereços e a RAM guarda o 4F nessa gaveta',
                   espera={'endereco': 32768, 'endereco_de': 'HL', 'dado_para': 'RAM'}),
        notas=[], derivado="os endereços seguem o programa do cap. 27, deslocado para a nossa frase",
    ),
    dict(
        id="d7", numero="6", regime="número → ordem",
        nome="Um número é lido como ordem", titulo="Um número é lido como ordem, não como quantidade",
        tese='Na mesma memória, ao lado das letras, moram outros bytes. '
             '<span class="mono">CD</span> não é letra: é a ordem “chame”. '
             '<span class="mono">C9</span> é “volte”.',
        corpo='Nada no byte diz se ele é letra ou ordem. O que decide é para onde o '
              'contador de programa aponta, e esse contador também é um número '
              'guardado na máquina. A máquina se governa com a mesma matéria que '
              'governa.',
        figura="dezesseis_bytes", origem=["Petzold, caps. 23 e 27", "programa real, para um Intel 8080 de 1978"],
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
            ('próximo = <span class="nome">passo</span>(<i>PC</i>, <i>A</i>, mem)',
             'o próximo estado é passo de: o contador de programa, o registrador A, e a memória'),
        ],
        placa=dict(ciclo=7, diz='o PC aponta 0004h e o byte 36 é lido como ordem: escreva em [HL]',
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
        corpo='É aqui que a delegação começa: a pessoa escreve a intenção, a máquina '
              'executa. O sistema operacional já sabe fazer serviços, como mostrar '
              'texto, para que cada programa não precise saber.',
        figura="montador", origem=["Petzold, cap. 27", "já na escada: máquina → assembler, avaliador, compilador"],
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
        corpo='Sessenta vezes por segundo a tela lê o bloco e acende. '
              '<span class="frase">Olá, Mundo!</span> volta a ser coisa que a gente '
              'lê, feita de números. Como o 79 vira o desenho do <b>O</b> é o '
              'buraco declarado deste mapa.',
        figura="pixels", origem=["Petzold, caps. 12 e 25", "do 79 ao desenho do O: a ler"],
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
     '<i>s</i><sub><i>t</i></sub>', "o estado no instante tê"),
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
     "um byte escrito com dois símbolos; de A a F valem de 10 a 15",
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
    origem=["régua: a tese “matemática como linguagem”"],
    linhas=[
        ("0 código", "a mensagem", "o meio", "cap. 1"),
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
    ("do teclado ao número", "Petzold cap. 25 — Peripherals",
     "deve cobrir; não copiado ainda"),
    ("a tabela ASCII em si", "Petzold cap. 13",
     "está no capítulo e não foi copiada; os números do degrau 1 são derivados"),
    ("o á em 1978", "Petzold cap. 27",
     "o programa é de antes do Unicode; a versão com “Olá, Mundo!” é adaptação do autor"),
    ("da tela à web", "Petzold cap. 27",
     "o capítulo termina com a mesma frase em JavaScript numa página; ainda não lido"),
]
