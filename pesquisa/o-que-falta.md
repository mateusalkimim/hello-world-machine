# O que a página não mostra, e por quê

Gerado por `gerar_site.py`. A página é para quem não sabe nada e não carrega isto.

## Procedência de cada degrau

| degrau | selo | fonte | derivado |
|---|---|---|---|
| 0 A frase já é um código | lida | cap. 1 — Best Friends |  |
| ½ A tecla vira número | lida | cap. 25 — Peripherals |  |
| 1 Cada letra recebe um número | lida | cap. 13 — From ASCII to Unicode | os onze números, calculados pelo autor; qualquer tabela Unicode confere |
| 2 Cada número vira oito casas | lida | cap. 11 — Bit by Bit by Bit · cap. 12 — Bytes and Hexadecimal |  |
| 2½ O á não cabe em um byte | lida | cap. 13, com o £ (U+00A3) como exemplo; o á (U+00E1) está na mesma faixa | C3 A1, pela regra da segunda linha da tabela do cap. 13 |
| 3 Cada casa vira corrente | escada | eletroímã → relé (Petzold cap. 7) · relé → porta lógica (cap. 8), com o instrumento “dois relés viram uma porta” |  |
| 4 Os bits somam e ficam parados | escada | porta → somador (cap. 14) · porta → flip-flop (caps. 17 e 19) · flip-flop de borda → contador e registrador (cap. 20) · somador → ULA (cap. 21) |  |
| 5 Cada byte ganha um endereço | lida | cap. 19 — An Assemblage of Memory | os endereços seguem o programa do cap. 27, deslocado para a nossa frase |
| 6 Um número é lido como ordem | lida | cap. 27 — Coding · cap. 23 — CPU Control Signals |  |
| 7 As ordens são escritas com palavras | lida | cap. 27 — Coding |  |
| 8 A ordem vira pontos de luz | lida | cap. 25 — Peripherals · cap. 12 (pixel = três bytes) |  |

## Notas dos degraus

- **½ A tecla vira número**: Nesta máquina a gaveta 8200h entrega direto o número da letra, porque o navegador já fez a conta. Num teclado de verdade o código é da tecla, não da letra, e um programa pequeno faz a tradução: o livro avisa. Decisão nossa, declarada.
- **1 Cada letra recebe um número**: A passagem que define a tabela ASCII em si está no mesmo capítulo e ainda não foi copiada.
- **6 Um número é lido como ordem**: O programa do livro é de antes do Unicode; um CP/M real não mostraria o á. A versão com “Olá, Mundo!” nas gavetas é adaptação do autor.
- **8 A ordem vira pontos de luz**: Fonte tipográfica e rasterização (do 79 ao desenho do O): o Petzold não cobre. Buraco declarado.

## Buracos declarados

Mapa que esconde o que falta mente sobre o próprio tamanho. Estes são os buracos que este mapa sabe ter.

- **do 79 ao desenho do O** (fonte tipográfica e rasterização): sem passagem no Petzold; outro livro, ou ofício do autor, datado
- **a tabela ASCII em si** (Petzold cap. 13): está no capítulo e não foi copiada; os números do degrau 1 são derivados
- **o á em 1978** (Petzold cap. 27): o programa é de antes do Unicode; a versão com “Olá, Mundo!” é adaptação do autor
- **da tela à web** (Petzold cap. 27): o capítulo termina com a mesma frase em JavaScript numa página; ainda não lido

## O que cada degrau conserva e esquece, com a fonte

| degrau | conserva | esquece | fonte |
|---|---|---|---|
| 0 código | a mensagem | o meio | cap. 1 |
| ½ tecla → número | o código da letra | a chave, o dedo | cap. 25 |
| 1 letra → número | qual letra é | forma e som | cap. 13 |
| 2 número → bits | o número exato | a base dez | caps. 11, 12 |
| 2½ o á | a letra e as 128 antigas | “um byte, uma letra” | cap. 13 |
| 3 bit → corrente | 0 e 1 | a física | escada |
| 4 conta e lembrança | a aritmética | os relés | escada |
| 5 endereço | a ordem das letras | o tempo | cap. 19 |
| 6 número → ordem | a matéria comum | “o que fazer” e “sobre o quê” | caps. 23, 27 |
| 7 palavras → ordens | o significado | as palavras | cap. 27 |
| 8 ordem → luz | a forma reconhecível | o número | caps. 12, 25 |
