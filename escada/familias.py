# -*- coding: utf-8 -*-
"""As seis famílias da escada — o que cada uma FAZ com o número.

Decisão do autor em 2026-10-03: a escada deixa de ser quinze degraus soltos por
nível e passa a ser seis famílias, nomeadas pelo verbo: transistores ligam e
desligam; portas decidem; somadores fazem conta; registradores guardam número;
instruções mandam; o relógio marca o tempo. Os degraus continuam existindo:
são as peças de cada família, com os campos e as frases do livro de sempre.

A página é para quem não sabe nada. Por isso cada família traz, ANTES de usar,
as palavras novas que vai usar (o que é, por que existe), e cada peça responde
as mesmas duas perguntas. Nada de método, selo ou história do repositório na
página: isso mora no README e em pesquisa/.

Orçamento por família (o gerador aborta acima): tese ≤ 25 palavras · corpo
≤ 60 · zero inglês visível · toda expressão com "lê-se" · nenhuma palavra
técnica antes da tela que a explica · nenhuma palavra de processo.
"""

FAMILIAS = [
    dict(
        id="transistores", nome="transistores", verbo="ligam e desligam",
        titulo="Uma chave que a eletricidade aciona",
        tese="Uma máquina que só sabe se há corrente ou não precisa de uma peça que "
             "faça isso: a chave. Primeiro o relé; hoje o transistor.",
        palavras=[
            dict(palavra="corrente",
                 o_que_e="eletricidade andando por dentro de um fio, como água andando por um cano.",
                 por_que="é ela que faz a lâmpada acender, o motor girar e, aqui, a chave virar."),
            dict(palavra="chave",
                 o_que_e="uma peça que abre ou fecha o caminho da corrente. O interruptor da luz é uma chave.",
                 por_que="para ligar e desligar sem cortar o fio."),
            dict(palavra="ímã",
                 o_que_e="um pedaço de ferro que puxa outros pedaços de ferro.",
                 por_que="puxar sem encostar é o que vai deixar uma corrente mexer numa chave."),
        ],
        corpo="Uma chave que outra corrente aciona deixa uma corrente mandar em outra. "
              "Por dentro, é um eletroímã no lugar do dedo: com corrente no fio de "
              "controle, o ímã puxa a lâmina e fecha o caminho; sem corrente, a lâmina "
              "solta. O relé é assim; o transistor faz o mesmo, minúsculo. Os dois só "
              "sabem duas coisas: ligado e desligado.",
        objeto="uma linha, o limiar, separa ligado de desligado",
        matematica=[
            ('<span class="nome">chave</span>(<i>v</i>) = 1 se <i>v</i> ≥ limiar, e 0 se <i>v</i> &lt; limiar',
             'chave de vê é igual a um se vê é maior ou igual ao limiar, e zero se vê é menor que o limiar'),
        ],
        membros=["eletroima", "rele", "transistor"],
        instrumento=None, figura="chave",
        fonte="petzold", ref="cap. 7 — Telegraphs and Relays · cap. 15 — Is This for Real?",
        citacoes=[
            ("We’re interested only in the idea of a relay being a switch that can "
             "be controlled by electricity rather than by fingers.",
             "O que nos interessa é só a ideia de o relé ser uma chave que a "
             "eletricidade controla, em vez dos dedos."),
            ("Vacuum tubes were originally developed for amplification, but they "
             "could also be used for switches in logic gates. The same goes for "
             "the transistor.",
             "As válvulas nasceram para amplificar, mas também serviam de chave em "
             "portas lógicas. O mesmo vale para o transistor."),
        ],
        previsao=dict(
            pergunta="Se a corrente que manda for fraca demais para puxar a lâmina do relé, a lâmpada do outro lado…",
            opcoes=["acende mais fraca", "não acende", "acende igual"], certa=1,
            porque="A chave não tem meio-termo: ou a lâmina fecha o caminho, ou não. "
                   "É por isso que dá para confiar: correntes diferentes dão o mesmo resultado, ligado ou desligado."),
        recuperacao=dict(
            pergunta="O que o transistor e o relé têm em comum, que faz os dois serem a mesma família?",
            opcoes=["os dois amplificam som", "os dois são chaves que a eletricidade aciona", "os dois guardam um número"], certa=1,
            porque="Família é o que a peça faz: estas ligam e desligam. Amplificar foi o "
                   "primeiro uso do transistor; guardar número é outra família, a dos registradores."),
    ),
    dict(
        id="portas", nome="portas lógicas", verbo="decidem",
        titulo="Duas chaves em série decidem",
        tese="Duas chaves em série só passam corrente com as duas fechadas: é a "
             "porta E. Em paralelo, basta uma: a porta OU. Decidir virou fiação.",
        palavras=[
            dict(palavra="entrada e saída",
                 o_que_e="entrada é por onde a corrente chega numa peça; saída é por onde ela sai.",
                 por_que="daqui para cima, toda peça se descreve pelo que sai, dado o que entrou."),
            dict(palavra="em série e em paralelo",
                 o_que_e="em série, duas chaves ficam uma depois da outra no mesmo caminho; em paralelo, cada chave tem o seu caminho.",
                 por_que="é a diferença entre precisar das duas fechadas e bastar uma."),
            dict(palavra="sim ou não",
                 o_que_e="corrente na saída é sim; sem corrente é não. Também se escreve 1 e 0.",
                 por_que="é a única pergunta que uma chave sabe responder, e dá para montar qualquer outra com ela."),
        ],
        corpo="Uma porta lógica responde sim ou não a uma pergunta sobre as "
              "entradas, e a resposta é só a forma como os fios foram ligados. "
              "Com E, OU e NÃO se monta qualquer pergunta de sim ou não. É o "
              "ponto em que o assunto deixa de ser eletricidade e passa a ser "
              "lógica.",
        objeto="regras de sim ou não, que se combinam",
        matematica=[
            ('<span class="nome">E</span>(<i>a</i>, <i>b</i>) = 1 só se <i>a</i> = 1 e <i>b</i> = 1',
             'E de a e b é igual a um só se a é igual a um e b é igual a um'),
        ],
        membros=["porta"],
        instrumento="porta", figura=None,
        fonte="petzold", ref="cap. 8 — Relays and Gates",
        citacoes=[
            ("These two relays wired in series are known as an AND gate because it "
             "is performing a Boolean AND operation.",
             "Esses dois relés ligados em série são conhecidos como porta E, porque "
             "executam a operação E de Boole."),
        ],
        previsao=dict(
            pergunta="Dois relés em série, e só o relé A acionado. A lâmpada…",
            opcoes=["acende", "não acende", "acende pela metade"], certa=1,
            porque="Em série, a corrente passa pelos dois contatos; um aberto basta para "
                   "cortar. É a porta E: precisa dos dois."),
        recuperacao=dict(
            pergunta="Que arranjo de dois relés acende a lâmpada quando qualquer um dos dois é acionado?",
            opcoes=["em série", "em paralelo", "nenhum: precisa de três"], certa=1,
            porque="Em paralelo há dois caminhos, e basta um fechado. É a porta OU. Em "
                   "série é a porta E."),
    ),
    dict(
        id="somadores", nome="somadores", verbo="fazem conta",
        titulo="Portas ligadas de um jeito fazem conta",
        tese="OU-exclusivo dá a soma de dois bits; E dá o vai-um. Encadeadas, "
             "somam qualquer número. A ULA é esse arranjo com nome de função.",
        palavras=[
            dict(palavra="bit",
                 o_que_e="uma casa que só aceita 0 ou 1. É o que uma chave guarda: desligada ou ligada.",
                 por_que="é a menor quantidade de informação que existe; tudo o mais é feito de bits."),
            dict(palavra="binário",
                 o_que_e="um número escrito só com 0 e 1, em que cada casa vale o dobro da vizinha: 1, 2, 4, 8…",
                 por_que="é o jeito de contar com chaves. Dois é 10; três é 11; quatro é 100."),
            dict(palavra="byte",
                 o_que_e="oito bits lado a lado. Cabem 256 valores diferentes.",
                 por_que="é o tamanho de uma letra, e o pedaço que a máquina move de cada vez."),
            dict(palavra="vai-um",
                 o_que_e="o 1 que sobra de uma casa e vai para a casa seguinte, como no papel.",
                 por_que="sem ele, a soma para na primeira casa."),
            dict(palavra="OU-exclusivo",
                 o_que_e="uma porta que responde sim só quando as duas entradas são diferentes.",
                 por_que="é exatamente a soma de uma casa: 0 e 1 dá 1; 1 e 1 dá 0, e sobra o vai-um."),
        ],
        corpo="Somar 1 + 1 dá 10 em binário: soma 0 e vai-um 1, exatamente o que as "
              "duas portas respondem. Ligando um somador de uma casa ao da casa "
              "seguinte, soma-se qualquer número. A ULA, a calculadora da máquina, "
              "junta a soma, a subtração e as operações de sim ou não num só lugar.",
        objeto="somar em binário, casa por casa, com o vai-um",
        matematica=[
            ('1 + 1 = 10 em binário: soma 0, vai-um 1',
             'um mais um é igual a um-zero em binário: soma zero, vai-um um'),
        ],
        membros=["somador", "ula"],
        instrumento="somador", figura=None,
        fonte="petzold", ref="cap. 14 — Adding with Logic Gates",
        citacoes=[
            ("A half adder is an XOR gate and an AND gate",
             "Um meio-somador é uma porta OU-exclusivo e uma porta E."),
        ],
        previsao=dict(
            pergunta="A = 1 e B = 1 no somador. O que sai?",
            opcoes=["soma 1, vai-um 0", "soma 0, vai-um 1", "soma 1, vai-um 1"], certa=1,
            porque="Um mais um é dois, que em binário se escreve 10: a casa da soma fica 0 "
                   "e o 1 vai para a casa seguinte. OU-exclusivo de 1 e 1 é 0; E de 1 e 1 é 1."),
        recuperacao=dict(
            pergunta="Por que a ULA é da família dos somadores, e não da dos registradores?",
            opcoes=["porque guarda o resultado", "porque faz conta e não guarda nada", "porque tem relógio"], certa=1,
            porque="A ULA opera e devolve; quem guarda o resultado é outra família, a dos "
                   "registradores, que vem a seguir. Família é o que a peça faz com o número."),
    ),
    dict(
        id="registradores", nome="registradores", verbo="guardam número",
        titulo="Um circuito que lembra",
        tese="Duas portas realimentadas lembram um bit depois que a entrada some. "
             "Oito lado a lado guardam um byte. Muitos, com endereço, são a memória.",
        palavras=[
            dict(palavra="realimentado",
                 o_que_e="um circuito cuja saída volta para a própria entrada.",
                 por_que="é o que faz a peça segurar o que recebeu, mesmo depois de a entrada sumir."),
            dict(palavra="relógio e borda",
                 o_que_e="o relógio é um tique que se repete, sempre igual; a borda é o instante em que o tique sobe. A peça que faz o tique vem na última família.",
                 por_que="para todas as peças guardarem no mesmo instante, e não a qualquer momento."),
            dict(palavra="endereço",
                 o_que_e="o número na porta de uma fileira da memória.",
                 por_que="para achar de novo o que foi guardado."),
        ],
        corpo="O flip-flop é o primeiro circuito cuja saída depende do que entrou "
              "antes, não só de agora. Guardando só na borda do relógio, vira o "
              "registrador, que segura um byte e o devolve quando mandam; em "
              "fileiras com endereço, vira a memória; ligado em fila, conta. "
              "Tudo é a mesma família: guardar número.",
        objeto="o estado de agora depende do estado de antes",
        matematica=[
            ('<i>s</i><sub><i>t</i>+1</sub> = <span class="nome">f</span>(<i>s</i><sub><i>t</i></sub>, <i>x</i><sub><i>t</i></sub>)',
             'o estado no instante tê mais um é f de: o estado no instante tê, e a entrada no instante tê'),
        ],
        membros=["flipflop", "flipflop_b", "registrador", "contador", "memoria"],
        instrumento="flipflop", figura=None,
        fonte="petzold", ref="cap. 19 — An Assemblage of Memory",
        citacoes=[
            ("the level-triggered D-type flip-flop, which is made from an inverter, "
             "two AND gates, and two NOR gates",
             "o flip-flop tipo D disparado por nível, que é feito de um inversor, "
             "duas portas E e duas portas NÃO-OU"),
            ("This configuration of flip-flops, decoder, and selector is sometimes "
             "known as read/write memory",
             "Esse arranjo de flip-flops, decodificador e seletor é às vezes chamado "
             "de memória de leitura e escrita"),
        ],
        previsao=dict(
            pergunta="Aperte S e solte. Depois aperte R e solte. Nos dois momentos a entrada voltou a (0, 0). A saída…",
            opcoes=["é a mesma nos dois", "é diferente nos dois", "fica apagada"], certa=1,
            porque="Com a mesma entrada, saídas diferentes: a saída depende do que veio "
                   "antes. É isso que lembrar quer dizer, e nenhuma porta sozinha faz."),
        recuperacao=dict(
            pergunta="A memória e o contador estão na família do flip-flop porque…",
            opcoes=["todos são feitos de flip-flops e guardam número", "todos fazem conta", "todos precisam de teclado"], certa=0,
            porque="Os três são feitos de flip-flops. O contador também soma um a cada "
                   "tique, mas o que ele conserva é o número guardado."),
    ),
    dict(
        id="instrucoes", nome="instruções", verbo="mandam",
        titulo="Um número lido como ordem",
        tese="Ao lado dos dados moram bytes que a máquina lê como ordens; o "
             "contador de programa aponta qual. Daí sobem montador, interpretador "
             "e compilador.",
        palavras=[
            dict(palavra="instrução",
                 o_que_e="uma ordem que a máquina sabe cumprir, guardada na memória como um byte: some, copie, guarde, pule.",
                 por_que="sem ordens, a máquina só guardaria e somaria ao acaso."),
            dict(palavra="programa",
                 o_que_e="uma fila de instruções, uma depois da outra.",
                 por_que="é como uma pessoa diz à máquina o que fazer, de uma vez, para a máquina fazer sozinha."),
            dict(palavra="contador de programa",
                 o_que_e="um contador que guarda o endereço da próxima instrução.",
                 por_que="para a máquina saber qual byte ler como ordem agora, e qual vem depois."),
            dict(palavra="controlador",
                 o_que_e="a parte que lê a instrução e manda nas outras peças, uma de cada vez.",
                 por_que="peça solta não faz nada em ordem; alguém tem de dizer quem trabalha agora."),
        ],
        corpo="Nada no byte diz se ele é dado ou ordem; o que decide é onde o "
              "contador de programa aponta. A máquina de registradores é esse "
              "arranjo: registradores, operações e um controlador que diz a ordem. "
              "O montador troca palavras por bytes; o interpretador executa um "
              "texto; o compilador o traduz de uma vez.",
        objeto="a máquina é uma regra de passo: do estado de agora para o próximo",
        matematica=[
            ('próximo = <span class="nome">passo</span>(<i>PC</i>, <i>A</i>, mem)',
             'o próximo estado é passo de: o contador de programa, o registrador A, e a memória'),
        ],
        membros=["maquina", "assembler", "avaliador", "compilador", "paradigma"],
        instrumento=None, figura="ordem",
        fonte="sicp", ref="§5.1 — Designing Register Machines · Petzold, cap. 23 — CPU Control Signals",
        citacoes=[
            ("To design a register machine, we must design its data paths (registers "
             "and operations) and the controller that sequences these operations.",
             "Para projetar uma máquina de registradores, projetamos os caminhos de "
             "dados (registradores e operações) e o controlador que sequencia essas "
             "operações."),
        ],
        previsao=dict(
            pergunta="Na memória há o byte 4F. Ele é uma letra ou uma ordem?",
            opcoes=["sempre uma letra", "sempre uma ordem", "depende de o contador de programa apontar para ele"], certa=2,
            porque="O byte é o mesmo nos dois casos. Quem decide é o apontador: se o contador "
                   "de programa chega nele, é lido como ordem."),
        recuperacao=dict(
            pergunta="Qual destas peças não é da família das instruções?",
            opcoes=["o montador", "o compilador", "o somador"], certa=2,
            porque="O somador faz conta e não sabe o que é uma ordem. Montador e "
                   "compilador vivem de traduzir ordens."),
    ),
    dict(
        id="relogio", nome="relógio", verbo="marca o tempo",
        titulo="O circuito que anda sozinho",
        tese="Um relé ligado à própria saída liga e desliga sozinho: o oscilador. "
             "Contar as voltas dele é medir o tempo, por isso se chama relógio.",
        palavras=[
            dict(palavra="tique",
                 o_que_e="uma volta completa do relógio: sobe e desce.",
                 por_que="é a unidade de tempo da máquina; tudo acontece de tique em tique."),
            dict(palavra="período e frequência",
                 o_que_e="período é quanto dura um tique; frequência é quantos tiques cabem num segundo.",
                 por_que="a frequência diz a velocidade da máquina."),
        ],
        corpo="Todo computador tem um oscilador que faz tudo o mais se mover em "
              "sincronia. É ele que entra no flip-flop de borda e diz quando "
              "guardar, e no contador diz quando avançar. Sem relógio, os "
              "registradores não saberiam o instante de guardar, e a máquina "
              "não teria um passo.",
        objeto="o tempo vira contagem: 0, 1, 2, …",
        matematica=[
            ('frequência = 1 ÷ período: 1 ÷ 0,02 s = 50 por segundo',
             'frequência é igual a um dividido pelo período: um dividido por zero vírgula zero dois segundo é igual a cinquenta por segundo'),
        ],
        membros=["oscilador"],
        instrumento=["flipflop_b", "contador"], figura=None,
        fonte="petzold", ref="cap. 17 — Feedback and Flip-Flops",
        citacoes=[
            ("All computers have some kind of oscillator that makes everything else "
             "move in synchronicity.",
             "Todo computador tem algum tipo de oscilador que faz tudo o mais se "
             "mover em sincronia."),
            ("For that reason, an oscillator is sometimes referred to as a clock "
             "because by counting the number of oscillations you can tell time "
             "(kind of).",
             "Por isso, um oscilador é às vezes chamado de relógio: contando as "
             "oscilações dá para dizer as horas (mais ou menos)."),
        ],
        previsao=dict(
            pergunta="O oscilador dá 50 voltas por segundo. Em um segundo, o contador ligado a ele mostra…",
            opcoes=["50", "1", "depende do dado"], certa=0,
            porque="O contador avança um a cada volta do relógio. Contar voltas é medir "
                   "tempo: é exatamente por isso que o oscilador se chama relógio."),
        recuperacao=dict(
            pergunta="O que o flip-flop de borda faz com o relógio?",
            opcoes=["ignora", "guarda o dado só no instante em que o relógio sobe", "guarda o dado o tempo todo"], certa=1,
            porque="Na borda, e só nela. O de nível guarda enquanto o relógio está alto, e "
                   "por isso vaza. O instrumento desta família mostra os dois lado a lado."),
    ),
]

# A folha de convenções: antecede o primeiro símbolo. Ensina a CLASSE do sinal.
CONVENCOES = [
    ("nome em letras retas, com parênteses", "uma regra com nome, aplicada ao que está entre parênteses",
     '<span class="nome">E</span>(<i>a</i>, <i>b</i>)', "E de a e b"),
    ("letra inclinada minúscula", "uma quantidade que varia", '<i>v</i>, <i>t</i>', "vê, tê"),
    ("índice embaixo", "em qual instante", '<i>s</i><sub><i>t</i></sub>', "o estado no instante tê"),
    ("número em binário", "um número escrito só com 0 e 1; cada casa vale o dobro da vizinha", '10', "um-zero, que vale dois"),
    ("≥ e &lt;", "maior ou igual; menor", '<i>v</i> ≥ limiar', "vê é maior ou igual ao limiar"),
    ("÷", "dividido por", '1 ÷ 0,02', "um dividido por zero vírgula zero dois"),
]

# As cores das famílias, uma por família, claras no escuro desta página.
COR = {
    "transistores": "#c1704f",
    "portas":       "#5b8fc9",
    "somadores":    "#7fa3dc",
    "registradores":"#4fb3a5",
    "instrucoes":   "#a883c9",
    "relogio":      "#c9a266",
}
