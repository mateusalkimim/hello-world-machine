# -*- coding: utf-8 -*-
"""As figuras, uma por degrau. SVG inline ou tabela; a palavra nova entra como
RÓTULO dentro da figura (contiguidade), nunca como glossário ao lado. Cores por
token do tema (var(--...)), nunca literal, para valer no claro e no escuro."""

FIGURAS = {
    "tecla_vira_numero": r"""<svg viewBox="0 0 520 150" role="img" aria-label="A tecla O fecha uma chave; a gaveta 8200h passa a valer 4F; o acumulador lê 4F">
      <text x="20" y="14" font-family="Inter, sans-serif" font-size="11" fill="var(--bronze)" font-weight="600" letter-spacing="1">TECLA · uma chave que o dedo fecha · a gaveta 8200h guarda o código</text>
      <g transform="translate(20,34)">
        <rect x="0" y="0" width="70" height="70" rx="8" fill="var(--card)" stroke="var(--linha)"/>
        <text x="35" y="46" text-anchor="middle" font-family="Cormorant Garamond, serif" font-size="34" fill="var(--ink)">O</text>
        <text x="35" y="90" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="var(--muted)">a tecla</text>
      </g>
      <g transform="translate(120,54)">
        <line x1="0" y1="24" x2="30" y2="24" stroke="var(--bit1)" stroke-width="2"/>
        <circle cx="30" cy="24" r="3" fill="var(--bit1)"/>
        <line x1="30" y1="24" x2="62" y2="24" stroke="var(--bit1)" stroke-width="2"/>
        <circle cx="62" cy="24" r="3" fill="var(--bit1)"/>
        <line x1="62" y1="24" x2="92" y2="24" stroke="var(--bit1)" stroke-width="2"/>
        <text x="46" y="60" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="var(--muted)">chave fechada = corrente</text>
      </g>
      <g transform="translate(236,34)">
        <rect x="0" y="0" width="110" height="46" fill="var(--card)" stroke="var(--bronze)"/>
        <text x="55" y="20" text-anchor="middle" font-family="Spline Sans Mono, monospace" font-size="12" fill="var(--muted)">8200h</text>
        <text x="55" y="38" text-anchor="middle" font-family="Spline Sans Mono, monospace" font-size="16" fill="var(--ink)">4F</text>
        <text x="55" y="90" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="var(--muted)">a gaveta do teclado</text>
      </g>
      <g transform="translate(360,57)"><line x1="0" y1="0" x2="40" y2="0" stroke="var(--bronze)" stroke-width="2"/><path d="M 36 -4 L 44 0 L 36 4 Z" fill="var(--bronze)"/><text x="22" y="-8" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" fill="var(--muted)">LDA 8200h</text></g>
      <g transform="translate(412,34)">
        <rect x="0" y="0" width="90" height="46" fill="var(--card)" stroke="var(--linha)"/>
        <text x="45" y="20" text-anchor="middle" font-family="Spline Sans Mono, monospace" font-size="12" fill="var(--muted)">A</text>
        <text x="45" y="38" text-anchor="middle" font-family="Spline Sans Mono, monospace" font-size="16" fill="var(--ink)">4F</text>
        <text x="45" y="90" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="var(--muted)">o acumulador</text>
      </g>
      <text x="260" y="140" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" fill="var(--muted)">79 é o O; 0 é “ninguém apertou”. O programa pergunta à gaveta o tempo todo: polling.</text>
    </svg>""",

    "tres_meios": r"""<svg viewBox="0 0 520 130" role="img" aria-label="A mesma frase em três meios: voz, papel, lanterna">
      <g font-family="Inter, sans-serif" font-size="11" fill="var(--bronze)" font-weight="600" letter-spacing="1">
        <text x="20" y="18">CÓDIGO 1 · VOZ</text><text x="200" y="18">CÓDIGO 2 · PAPEL</text><text x="372" y="18">CÓDIGO 3 · LANTERNA</text>
      </g>
      <text x="20" y="60" font-family="Cormorant Garamond, serif" font-style="italic" font-size="24" fill="var(--ink)">Olá, Mundo!</text>
      <text x="200" y="60" font-family="Inter, sans-serif" font-size="20" fill="var(--ink)">Olá, Mundo!</text>
      <g fill="var(--bronze)">
        <circle cx="380" cy="50" r="5"/><circle cx="396" cy="50" r="5"/><circle cx="412" cy="50" r="5"/><rect x="428" y="45" width="22" height="10" rx="5"/><circle cx="466" cy="50" r="5"/>
        <rect x="380" y="68" width="22" height="10" rx="5"/><circle cx="420" cy="73" r="5"/><rect x="436" y="68" width="22" height="10" rx="5"/>
      </g>
      <g font-family="Inter, sans-serif" font-size="11" fill="var(--muted)">
        <text x="20" y="110">som no ar</text><text x="200" y="110">traço na folha</text><text x="372" y="110">só dois sinais: curto e longo</text>
      </g>
      <g stroke="var(--linha)"><line x1="175" y1="8" x2="175" y2="118"/><line x1="350" y1="8" x2="350" y2="118"/></g>
    </svg>""",

    "tabela_numeros": r"""<p class="rotulo">tabela Unicode: o mesmo combinado em toda máquina do planeta</p>
    <div class="tabela"><table class="mono">
      <tr><th>letra</th><td>O</td><td>l</td><td>á</td><td>,</td><td>␣</td><td>M</td><td>u</td><td>n</td><td>d</td><td>o</td><td>!</td></tr>
      <tr><th>número</th><td>79</td><td>108</td><td>225</td><td>44</td><td>32</td><td>77</td><td>117</td><td>110</td><td>100</td><td>111</td><td>33</td></tr>
    </table></div>""",

    "byte_79": r"""<svg viewBox="0 0 520 165" role="img" aria-label="O número 79 decomposto em oito casas que valem 128, 64, 32, 16, 8, 4, 2, 1">
      <text x="24" y="14" font-family="Inter, sans-serif" font-size="11" fill="var(--bronze)" font-weight="600" letter-spacing="1">UM BYTE = OITO BITS · cada casa vale o dobro da vizinha</text>
      <g font-family="Spline Sans Mono, monospace" font-size="13" fill="var(--muted)" text-anchor="middle">
        <text x="48" y="36">128</text><text x="108" y="36">64</text><text x="168" y="36">32</text><text x="228" y="36">16</text><text x="288" y="36">8</text><text x="348" y="36">4</text><text x="408" y="36">2</text><text x="468" y="36">1</text>
      </g>
      <g font-family="Spline Sans Mono, monospace" font-size="26" text-anchor="middle">
        <rect x="24" y="46" width="48" height="48" fill="var(--bit0)"/><text x="48" y="80" fill="var(--bit0-ink)">0</text>
        <rect x="84" y="46" width="48" height="48" fill="var(--bit1)"/><text x="108" y="80" fill="var(--card)">1</text>
        <rect x="144" y="46" width="48" height="48" fill="var(--bit0)"/><text x="168" y="80" fill="var(--bit0-ink)">0</text>
        <rect x="204" y="46" width="48" height="48" fill="var(--bit0)"/><text x="228" y="80" fill="var(--bit0-ink)">0</text>
        <rect x="264" y="46" width="48" height="48" fill="var(--bit1)"/><text x="288" y="80" fill="var(--card)">1</text>
        <rect x="324" y="46" width="48" height="48" fill="var(--bit1)"/><text x="348" y="80" fill="var(--card)">1</text>
        <rect x="384" y="46" width="48" height="48" fill="var(--bit1)"/><text x="408" y="80" fill="var(--card)">1</text>
        <rect x="444" y="46" width="48" height="48" fill="var(--bit1)"/><text x="468" y="80" fill="var(--card)">1</text>
      </g>
      <text x="260" y="128" text-anchor="middle" font-family="Inter, sans-serif" font-size="15" fill="var(--ink)">64 + 8 + 4 + 2 + 1 = 79 = <tspan font-family="Cormorant Garamond, serif" font-size="19">O</tspan></text>
      <text x="260" y="152" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" fill="var(--muted)">bit = uma casa · as casas pintadas somam, as vazias não contam</text>
    </svg>""",

    "bits_do_a": r"""<p class="rotulo">começar com 110 e 10 é a marca de "vem em dupla"; o 0 na frente do o diz "vem sozinho"</p>
    <div class="tabela"><table class="mono">
      <tr><th>letra</th><th>bytes</th><th>em bits</th></tr>
      <tr><td>O</td><td>1</td><td><span class="bits"><i class="z">0</i><i class="u">1</i><i class="z">0</i><i class="z">0</i><i class="u">1</i><i class="u">1</i><i class="u">1</i><i class="u">1</i></span></td></tr>
      <tr><td>l</td><td>1</td><td><span class="bits"><i class="z">0</i><i class="u">1</i><i class="u">1</i><i class="z">0</i><i class="u">1</i><i class="u">1</i><i class="z">0</i><i class="z">0</i></span></td></tr>
      <tr><td>á</td><td>2</td><td><span class="bits"><i class="u">1</i><i class="u">1</i><i class="z">0</i><i class="z">0</i><i class="z">0</i><i class="z">0</i><i class="u">1</i><i class="u">1</i></span>&nbsp;<span class="bits"><i class="u">1</i><i class="z">0</i><i class="u">1</i><i class="z">0</i><i class="z">0</i><i class="z">0</i><i class="z">0</i><i class="u">1</i></span></td></tr>
    </table></div>""",

    "oito_reles": r"""<svg viewBox="0 0 520 100" role="img" aria-label="Oito relés, um por bit do O">
      <text x="20" y="14" font-family="Inter, sans-serif" font-size="11" fill="var(--bronze)" font-weight="600" letter-spacing="1">RELÉ · chave fechada = corrente = 1 · chave aberta = 0</text>
      <g font-family="Spline Sans Mono, monospace" font-size="12" text-anchor="middle">
        <g transform="translate(20,24)"><rect width="48" height="40" fill="var(--bit0)" stroke="var(--linha)"/><line x1="8" y1="30" x2="28" y2="14" stroke="var(--bit0-ink)" stroke-width="2"/><circle cx="8" cy="30" r="3" fill="var(--bit0-ink)"/><circle cx="40" cy="30" r="3" fill="var(--bit0-ink)"/><text x="24" y="64" fill="var(--muted)">0</text></g>
        <g transform="translate(80,24)"><rect width="48" height="40" fill="var(--card)" stroke="var(--bit1)"/><line x1="8" y1="30" x2="40" y2="30" stroke="var(--bit1)" stroke-width="2"/><circle cx="8" cy="30" r="3" fill="var(--bit1)"/><circle cx="40" cy="30" r="3" fill="var(--bit1)"/><text x="24" y="64" fill="var(--ink)">1</text></g>
        <g transform="translate(140,24)"><rect width="48" height="40" fill="var(--bit0)" stroke="var(--linha)"/><line x1="8" y1="30" x2="28" y2="14" stroke="var(--bit0-ink)" stroke-width="2"/><circle cx="8" cy="30" r="3" fill="var(--bit0-ink)"/><circle cx="40" cy="30" r="3" fill="var(--bit0-ink)"/><text x="24" y="64" fill="var(--muted)">0</text></g>
        <g transform="translate(200,24)"><rect width="48" height="40" fill="var(--bit0)" stroke="var(--linha)"/><line x1="8" y1="30" x2="28" y2="14" stroke="var(--bit0-ink)" stroke-width="2"/><circle cx="8" cy="30" r="3" fill="var(--bit0-ink)"/><circle cx="40" cy="30" r="3" fill="var(--bit0-ink)"/><text x="24" y="64" fill="var(--muted)">0</text></g>
        <g transform="translate(260,24)"><rect width="48" height="40" fill="var(--card)" stroke="var(--bit1)"/><line x1="8" y1="30" x2="40" y2="30" stroke="var(--bit1)" stroke-width="2"/><circle cx="8" cy="30" r="3" fill="var(--bit1)"/><circle cx="40" cy="30" r="3" fill="var(--bit1)"/><text x="24" y="64" fill="var(--ink)">1</text></g>
        <g transform="translate(320,24)"><rect width="48" height="40" fill="var(--card)" stroke="var(--bit1)"/><line x1="8" y1="30" x2="40" y2="30" stroke="var(--bit1)" stroke-width="2"/><circle cx="8" cy="30" r="3" fill="var(--bit1)"/><circle cx="40" cy="30" r="3" fill="var(--bit1)"/><text x="24" y="64" fill="var(--ink)">1</text></g>
        <g transform="translate(380,24)"><rect width="48" height="40" fill="var(--card)" stroke="var(--bit1)"/><line x1="8" y1="30" x2="40" y2="30" stroke="var(--bit1)" stroke-width="2"/><circle cx="8" cy="30" r="3" fill="var(--bit1)"/><circle cx="40" cy="30" r="3" fill="var(--bit1)"/><text x="24" y="64" fill="var(--ink)">1</text></g>
        <g transform="translate(440,24)"><rect width="48" height="40" fill="var(--card)" stroke="var(--bit1)"/><line x1="8" y1="30" x2="40" y2="30" stroke="var(--bit1)" stroke-width="2"/><circle cx="8" cy="30" r="3" fill="var(--bit1)"/><circle cx="40" cy="30" r="3" fill="var(--bit1)"/><text x="24" y="64" fill="var(--ink)">1</text></g>
      </g>
    </svg>""",

    "somador_flipflop": r"""<svg viewBox="0 0 520 110" role="img" aria-label="Dois arranjos de portas: o somador e o flip-flop">
      <g font-family="Inter, sans-serif" font-size="13" fill="var(--ink)">
        <rect x="20" y="14" width="220" height="82" fill="var(--card)" stroke="var(--bronze)"/>
        <text x="30" y="34" font-size="11" fill="var(--bronze)" font-weight="600" letter-spacing="1">SOMADOR · faz conta</text>
        <text x="130" y="60" text-anchor="middle" font-family="Spline Sans Mono, monospace" font-size="13">01001111 + 00000001</text>
        <text x="130" y="82" text-anchor="middle" font-family="Spline Sans Mono, monospace" font-size="13" fill="var(--bronze)">= 01010000 = P</text>
        <rect x="280" y="14" width="220" height="82" fill="var(--card)" stroke="var(--azul)"/>
        <text x="290" y="34" font-size="11" fill="var(--azul)" font-weight="600" letter-spacing="1">FLIP-FLOP · lembra</text>
        <text x="390" y="60" text-anchor="middle" font-size="12" fill="var(--ink2)">entrou 1, a entrada sumiu,</text>
        <text x="390" y="82" text-anchor="middle" font-size="12" fill="var(--azul)">a saída continua 1</text>
      </g>
    </svg>""",

    "gavetas": r"""<svg viewBox="0 0 520 128" role="img" aria-label="Doze gavetas de memória: conteúdo em cima, endereço embaixo">
      <text x="8" y="12" font-family="Inter, sans-serif" font-size="11" fill="var(--bronze)" font-weight="600" letter-spacing="1">GAVETA · dentro, o conteúdo · na porta, o endereço</text>
      <g font-family="Spline Sans Mono, monospace" font-size="12" text-anchor="middle">
        <g transform="translate(8,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">4F</text><text x="20" y="62" font-size="11" fill="var(--muted)">0109</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">O</text></g>
        <g transform="translate(50,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">6C</text><text x="20" y="62" font-size="11" fill="var(--muted)">010A</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">l</text></g>
        <g transform="translate(92,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--bronze)"/><text x="20" y="29" font-size="15" fill="var(--ink)">C3</text><text x="20" y="62" font-size="11" fill="var(--muted)">010B</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">á</text></g>
        <g transform="translate(134,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--bronze)"/><text x="20" y="29" font-size="15" fill="var(--ink)">A1</text><text x="20" y="62" font-size="11" fill="var(--muted)">010C</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">·</text></g>
        <g transform="translate(176,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">2C</text><text x="20" y="62" font-size="11" fill="var(--muted)">010D</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">,</text></g>
        <g transform="translate(218,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">20</text><text x="20" y="62" font-size="11" fill="var(--muted)">010E</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">␣</text></g>
        <g transform="translate(260,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">4D</text><text x="20" y="62" font-size="11" fill="var(--muted)">010F</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">M</text></g>
        <g transform="translate(302,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">75</text><text x="20" y="62" font-size="11" fill="var(--muted)">0110</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">u</text></g>
        <g transform="translate(344,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">6E</text><text x="20" y="62" font-size="11" fill="var(--muted)">0111</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">n</text></g>
        <g transform="translate(386,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">64</text><text x="20" y="62" font-size="11" fill="var(--muted)">0112</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">d</text></g>
        <g transform="translate(428,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">6F</text><text x="20" y="62" font-size="11" fill="var(--muted)">0113</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">o</text></g>
        <g transform="translate(470,20)"><rect width="40" height="46" fill="var(--card)" stroke="var(--linha)"/><text x="20" y="29" font-size="15" fill="var(--ink)">21</text><text x="20" y="62" font-size="11" fill="var(--muted)">0114</text><text x="20" y="84" font-family="Cormorant Garamond, serif" font-size="18" fill="var(--bronze)">!</text></g>
      </g>
      <text x="260" y="122" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="var(--muted)">4F é o 79 em hexadecimal: oito bits abreviados em dois símbolos · o á ocupa duas gavetas vizinhas</text>
    </svg>""",

    "dezesseis_bytes": r"""<svg viewBox="0 0 520 150" role="img" aria-label="Os dezesseis bytes do programa Hello do Petzold: nove ordens e sete letras na mesma memória">
      <g font-family="Inter, sans-serif" font-size="11" font-weight="600" letter-spacing="1">
        <text x="10" y="14" fill="var(--azul)">ORDENS · 9 bytes</text><text x="304" y="14" fill="var(--bronze)">LETRAS · 7 bytes</text>
      </g>
      <g font-family="Spline Sans Mono, monospace" font-size="13" text-anchor="middle">
        <rect x="10" y="22" width="286" height="40" fill="var(--card)" stroke="var(--azul)"/>
        <text x="153" y="47" fill="var(--azul)">11 09 01  0E 09  CD 05 00  C9</text>
        <rect x="304" y="22" width="206" height="40" fill="var(--card)" stroke="var(--bronze)"/>
        <text x="407" y="47" fill="var(--bronze)">48 65 6C 6C 6F 21 24</text>
      </g>
      <g font-family="Inter, sans-serif" font-size="12" fill="var(--muted)" text-anchor="middle">
        <text x="153" y="82">carregue · mova · chame · volte</text>
        <text x="407" y="82">H e l l o ! $</text>
      </g>
      <path d="M 30 125 L 30 105 L 290 105" fill="none" stroke="var(--azul)" stroke-width="1.5"/>
      <path d="M 286 101 L 294 105 L 286 109 Z" fill="var(--azul)"/>
      <text x="40" y="140" font-family="Inter, sans-serif" font-size="12" fill="var(--ink2)">CONTADOR DE PROGRAMA: percorre só o lado azul; o lado bronze ele aponta, como dado</text>
    </svg>""",

    "montador": r"""<p class="rotulo">montador: uma linha, uma ordem</p>
    <div class="tabela"><table>
      <tr><th>o que a pessoa escreve</th><th>o que vira</th><th>o que faz</th></tr>
      <tr><td class="mono">LXI DE,Text</td><td class="mono">11 09 01</td><td>aponte para a frase</td></tr>
      <tr><td class="mono">MVI C,9</td><td class="mono">0E 09</td><td>peça o serviço 9: mostrar texto</td></tr>
      <tr><td class="mono">CALL 5</td><td class="mono">CD 05 00</td><td>chame o sistema</td></tr>
      <tr><td class="mono">RET</td><td class="mono">C9</td><td>volte</td></tr>
      <tr><td class="mono">DB 'Hello!$'</td><td class="mono">48 65 6C 6C 6F 21 24</td><td>a frase, byte a byte</td></tr>
    </table></div>""",

    "pixels": r"""<svg viewBox="0 0 520 175" role="img" aria-label="A letra O desenhada numa grade de pixels; cada pixel tem três bytes">
      <text x="20" y="12" font-family="Inter, sans-serif" font-size="11" fill="var(--bronze)" font-weight="600" letter-spacing="1">PIXEL · um ponto da tela · três bytes: vermelho, verde, azul</text>
      <g transform="translate(0,8)">
        <rect x="20" y="10" width="150" height="150" fill="var(--card)" stroke="var(--linha)"/>
        <g fill="var(--ink)">
          <rect x="65" y="25" width="15" height="15"/><rect x="80" y="25" width="15" height="15"/><rect x="95" y="25" width="15" height="15"/><rect x="110" y="25" width="15" height="15"/>
          <rect x="50" y="40" width="15" height="15"/><rect x="125" y="40" width="15" height="15"/>
          <rect x="35" y="55" width="15" height="15"/><rect x="140" y="55" width="15" height="15"/>
          <rect x="35" y="70" width="15" height="15"/><rect x="140" y="70" width="15" height="15"/>
          <rect x="35" y="85" width="15" height="15"/><rect x="140" y="85" width="15" height="15"/>
          <rect x="35" y="100" width="15" height="15"/><rect x="140" y="100" width="15" height="15"/>
          <rect x="50" y="115" width="15" height="15"/><rect x="125" y="115" width="15" height="15"/>
          <rect x="65" y="130" width="15" height="15"/><rect x="80" y="130" width="15" height="15"/><rect x="95" y="130" width="15" height="15"/><rect x="110" y="130" width="15" height="15"/>
        </g>
        <g stroke="var(--linha)" stroke-width=".5" opacity=".7">
          <line x1="35" y1="10" x2="35" y2="160"/><line x1="50" y1="10" x2="50" y2="160"/><line x1="65" y1="10" x2="65" y2="160"/><line x1="80" y1="10" x2="80" y2="160"/><line x1="95" y1="10" x2="95" y2="160"/><line x1="110" y1="10" x2="110" y2="160"/><line x1="125" y1="10" x2="125" y2="160"/><line x1="140" y1="10" x2="140" y2="160"/><line x1="155" y1="10" x2="155" y2="160"/>
          <line x1="20" y1="25" x2="170" y2="25"/><line x1="20" y1="40" x2="170" y2="40"/><line x1="20" y1="55" x2="170" y2="55"/><line x1="20" y1="70" x2="170" y2="70"/><line x1="20" y1="85" x2="170" y2="85"/><line x1="20" y1="100" x2="170" y2="100"/><line x1="20" y1="115" x2="170" y2="115"/><line x1="20" y1="130" x2="170" y2="130"/><line x1="20" y1="145" x2="170" y2="145"/>
        </g>
        <rect x="35" y="55" width="15" height="15" fill="none" stroke="var(--bronze)" stroke-width="2"/>
        <path d="M 50 62 L 200 62" stroke="var(--bronze)" stroke-width="1.2" fill="none"/>
        <g font-family="Inter, sans-serif" font-size="13" fill="var(--ink)">
          <text x="210" y="56" font-weight="600">este pixel</text>
          <text x="210" y="76" font-family="Spline Sans Mono, monospace">16 23 3F</text>
          <text x="210" y="94" fill="var(--muted)" font-size="12">cada um de 0 a 255</text>
          <text x="210" y="124" fill="var(--ink2)" font-size="12">tela de 1920 × 1080 pontos</text>
          <text x="210" y="142" font-family="Spline Sans Mono, monospace" font-size="12">1920 × 1080 × 3 = 6 220 800 bytes</text>
          <text x="210" y="160" fill="var(--muted)" font-size="12">lidos 60 vezes por segundo</text>
        </g>
      </g>
    </svg>""",

}