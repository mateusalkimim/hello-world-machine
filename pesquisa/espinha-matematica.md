# A espinha matemática

A tese deste material, fixada em 2026-10-02. O que importa não é a eletrônica
de cada camada (isso é profundidade, e mora no
[abstraction-ladder](https://github.com/mateusalkimim/abstraction-ladder)).
O que importa é responder três perguntas:

1. **como corrente elétrica vira dado;**
2. **como o dado navega em forma de corrente;**
3. **o que cada camada de abstração significa matematicamente.**

A régua que atravessa as três: a matemática se refere ao mundo **por aquilo
que se conserva**. Cada camada é uma promessa do tipo "pode esquecer o resto,
isto eu garanto". A execução é o que sobra quando todas as promessas foram
cumpridas.

## Degrau a degrau

| degrau | o que acontece | o objeto matemático | o que se conserva |
|---|---|---|---|
| 0 código | sinal ↔ significado | função com inversa (bijeção) | distinguir uma mensagem da outra |
| 1 letra → número | tabela Unicode | bijeção do alfabeto nos números | qual letra é |
| 2 número → bits | 79 = 64 + 8 + 4 + 2 + 1 | notação posicional, soma de potências de 2; 256 é o tamanho de {0,1}⁸ | o número exato |
| 2½ o á | dois bytes | código de comprimento variável, livre de prefixo | a letra, sem ambiguidade |
| 3 corrente → bit | tensão vira 0 ou 1 | **limiar: um intervalo inteiro de tensões vira um símbolo só** | o símbolo, apesar do ruído |
| 4 portas e soma | AND, OR, somador | álgebra de Boole; aritmética módulo 256 | a conta dá o mesmo que no papel |
| 4 lembrar e relógio | flip-flop, borda | estado: o próximo depende do anterior; o tempo vira contagem | o passado |
| 5 endereço | gaveta com número | a memória é uma função: endereço → byte | a ordem das letras |
| 6 número → ordem | CD é "chame" | a máquina é uma função de transição de estado; programa é dado | a matéria comum |
| 7 palavras → ordens | CALL 5 → CD 05 00 | tradução que preserva significado | o que o programa faz |
| 8 tela | 3 bytes por ponto | função da grade nas cores; a letra é um subconjunto da grade | a forma que o olho lê |

## Os dois pontos que pesam mais

**Corrente vira dado pelo limiar.** Um intervalo inteiro de tensões é lido
como "1". É por isso que o digital é confiável: muitas tensões diferentes dão
o mesmo símbolo, e o ruído some na equivalência. A matemática aqui é a de
classe de equivalência: o símbolo é a classe, a tensão é o representante. Este
é o degrau que a página de hoje pula, e é o primeiro a entrar.

**Dado "viaja" como onda de estados, não como coisa que anda.** Num
barramento nada se desloca: cada fio muda de estado, e o padrão se repete no
módulo seguinte. Os pontos em movimento dos simuladores de circuito mostram
corrente, não dado. O instrumento tem de ser honesto nisso: o byte aparece no
registrador, depois no barramento, depois na memória de vídeo, como uma onda
que se copia.

## O que isso muda na página

- cada degrau ganha uma linha **"a matemática daqui"**, com a expressão e a
  leitura em voz alta ("lê-se:"), porque passa a haver expressão visível;
- antes do primeiro símbolo entra uma **folha de convenções**: o que cada
  sinal quer dizer, em português, antes de aparecer;
- a classe vem antes do símbolo; sem quantificadores nem setas de implicação;
  letra grega nunca é o objeto principal.

## Procedência

As passagens que sustentam os degraus continuam sendo as do Petzold, lidas. A
coluna "objeto matemático" é **ofício do autor**, datada de 2026-10-02: não há
livro citado dizendo "o limiar é uma classe de equivalência". Quando houver,
a passagem entra ao lado, com o mesmo selo das outras.
