# A forma de um degrau

Conhecimento destilado deste repositório. Vale para qualquer material que
explique uma transformação, passo a passo, a quem não sabe nada.

## O defeito que a primeira versão tinha

A primeira página tinha, em cada degrau, cinco blocos fixos: a tese, a figura,
um glossário, um par "conserva / esquece" e a citação do livro em inglês com o
selo de procedência. Medida: de 125 a 278 palavras por degrau, e 308 palavras
em inglês no corpo. Para quem não sabe nada, isso é um muro.

O glossário era o pior dos cinco, por uma razão estrutural: palavra nova
explicada **ao lado** da figura obriga o leitor a ir e voltar entre as duas.
É o efeito de atenção dividida de Chandler e Sweller (1992): a integração
física do rótulo com o diagrama reduz a carga; o texto que repete o que a
figura já mostra prejudica.

## As regras, com as fontes

1. **O nível novo aparece com o anterior ainda visível.** Bret Victor, *Up and
   Down the Ladder of Abstraction*: o abstrato só se sustenta se o concreto
   continua desenhado sobre ele. Aqui é a trilha do alto da página: o "o" fica
   ao lado do 111, do 01101111, dos oito relés, da gaveta 0109. Ben Eater faz o
   mesmo com um LED em cada fio do seu computador de 8 bits.
   <http://worrydream.com/LadderOfAbstraction/> · <https://eater.net/8bit>

2. **Varia uma coisa por degrau, e o leitor controla o passo.** Victor
   ("não ser escravo do tempo real"); Nicky Case (uma mecânica por vez);
   Mayer, princípio da segmentação. Nada roda sozinho.
   <https://blog.ncase.me/explorable-explanations/>

3. **Um degrau é uma tese e uma figura.** The Pudding: cada ponto tem o seu
   gráfico e um texto curto apontando o que ver; antes de cada passo, "qual é o
   ponto deste passo?". Amit Patel: um conceito por diagrama.
   <https://pudding.cool/process/how-to-make-dope-shit-part-3/> ·
   <https://www.redblobgames.com/making-of/little-things/>

4. **A palavra nova é rótulo dentro da figura.** Chandler e Sweller (1992),
   atenção dividida e redundância; Mayer, contiguidade espacial.
   <https://www.davidlewisphd.com/courses/EDD8121/readings/1992-ChandlerSweller-SplitAttention.pdf>

5. **O que antes do como; o como abre sob demanda, um nível só.** Nand to
   Tetris: todo chip tem interface (o que faz) e implementação (como faz).
   Nielsen Norman Group, *progressive disclosure*: no máximo dois níveis.
   <https://www.nand2tetris.org/> ·
   <https://www.nngroup.com/articles/progressive-disclosure/>

6. **A prova existe e fica fechada por padrão.** Gwern, sobre notas laterais:
   a nota de rodapé na web degrada em nota final, que ninguém lê; a citação tem
   de estar a um gesto, não fora do caminho. Victor: contexto a um clique, para
   checar as afirmações do autor sem sair do fluxo.
   <https://gwern.net/sidenote> · <http://worrydream.com/ExplorableExplanations/>

7. **Símbolo real, sem metáfora boba.** Petzold, no prefácio da segunda
   edição: a linguagem e os símbolos dos engenheiros de verdade. A gaveta com
   número na porta passa, porque é como o livro desenha a memória.
   <https://codehiddenlanguage.com/>

8. **Um personagem com um problema puxa cada código.** Petzold abre com dois
   amigos e lanternas; aqui, "olá mundo" quer chegar à tela.

9. **Cor semântica constante** do texto à figura ao número (Patel; Mayer,
   sinalização). O bronze é sempre a letra; o azul, sempre a ordem.

10. **No celular, empilha e tira o hover** (The Pudding, *responsive
    scrollytelling*).
    <https://pudding.cool/process/responsive-scrollytelling/>

## O orçamento que saiu disso

Por degrau: tese de até 25 palavras; uma figura; parágrafo de até 60; zero
inglês no texto visível. O gerador mede e aborta acima disso. A régua de
comparação foi um deck didático do autor, com mediana de 123 palavras por folha
e quatro blocos fixos, que já funcionava com o mesmo leitor.

## Como se reconhece o defeito em outro material

- a palavra nova é explicada **ao lado** da figura, e não dentro dela?
- o passo anterior **some** quando o seguinte aparece?
- a prova está **no corpo**, obrigando quem só quer entender a ler quem só
  quer conferir?

Se sim às três, o material é denso pelo motivo errado: não por ter muito a
dizer, mas por dizer tudo no mesmo lugar.
