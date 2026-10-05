# Mapa pequeno e lido vence mapa grande e gerado

Conhecimento destilado deste repositório — vale para qualquer mapa de
conhecimento, e sobreviveria se o código aqui fosse jogado fora.

## O defeito que este repositório existe para não ter

Um mapa de domínio gerado por modelo de linguagem custa uma tarde e **parece
completo**. É essa aparência o problema: ela não distingue a aresta que alguém
verificou da aresta que soou plausível, e o leitor não tem como saber qual é
qual.

O caso é concreto, e o formato do erro importa mais que o caso. Um verbete
gerado pode afirmar que dois conjuntos com os mesmos elementos são diferentes —
a negação direta do axioma que *define* igualdade de conjuntos — e ficar no
campo "onde se trava", isto é, apresentado como *o erro que o leitor deve
evitar*. **Ensina o erro na posição da correção.**

Um erro assim passa por razão estrutural, não por descuido: quando existe
verificação, ela costuma cobrir um campo de quatro, e não é esse.

## A inversão

A resposta usual é revisar depois. Não funciona em escala: quem revisa cinquenta
verbetes plausíveis não encontra o falso, porque todos parecem iguais — a
plausibilidade é justamente o que o modelo otimiza.

A resposta deste repositório é **inverter a ordem**: a leitura humana vem
antes do conteúdo. Uma aresta só existe se alguém abriu o livro e copiou a
frase. E o gerador **aborta** se a citação estiver vazia — a regra não é
convenção que se esquece, é condição de a página existir.

O preço é um mapa pequeno. Seis arestas onde caberiam sessenta.

## As três propriedades que isso compra

**1. O leitor pode discordar.** Com a citação à vista, quem achar que a aresta
está errada vai à fonte e verifica. Sem ela, resta acreditar ou ignorar — e as
duas coisas são igualmente inúteis.

**2. O que falta fica visível.** O mapa lista as arestas que sabe existirem e
ainda não abriu, com a referência de onde estão. **Mapa que esconde o que falta
mente sobre o próprio tamanho** — e a mentira é sobre a coisa mais importante,
que é quanto do domínio ele cobre.

**3. Duas testemunhas valem mais que uma.** Quando duas fontes independentes
descrevem o mesmo objeto chegando de direções opostas — uma construindo,
a outra definindo —, a aresta deixa de depender da autoridade de um autor.
É o caso da máquina de registradores aqui.

## Como se reconhece o defeito em outro mapa

Três perguntas, e a terceira é a que raramente se faz:

- **cada aresta mostra a fonte?** Se não, o mapa afirma sem responder por quê;
- **o mapa declara o que não sabe?** Um mapa sem buracos declarados ou é o
  domínio inteiro, o que é improvável, ou está escondendo a fronteira;
- **existe um caminho pelo qual uma aresta falsa entraria sem ninguém notar?**
  Se existe, ele já foi usado. Não é hipótese: é só questão de quantas arestas
  o mapa tem.
