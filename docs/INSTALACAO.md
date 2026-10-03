<!-- idioma: linha gerada por i18n.py -->
> [!NOTE]
> ### 🌍 **[Read this page in English →](INSTALACAO.en.md)**

# Instalação

Não há instalação para **usar**: `pt/index.html` é uma página autocontida, abre
offline em qualquer navegador moderno.

## Usar

**Windows** — baixe (Code → Download ZIP, ou `git clone`), extraia, e dê duplo
clique em `index.html`.

**Linux** — `git clone … && cd hello-world-machine && xdg-open index.html`

**macOS** — o mesmo, com `open index.html`.

**Sem baixar** — <https://mateusalkimim.github.io/hello-world-machine/>

Na página: ← e → no teclado, ou os botões com o nome do degrau vizinho. Clicar
numa estação da trilha do alto leva ao degrau. A página lembra onde você parou.

## Regerar a página

Só quem for **editar** precisa disto. Python 3, biblioteca padrão, nenhum
pacote.

```bash
python3 gerar_site.py        # pt/index.html, os degraus
python3 gerar_placa.py       # pt/placa.html, o instrumento
python3 gerar_en.py          # en/, derivado da tabela de tradução
```

O `pt/index.html` é **derivado** de `degraus.py`, `figuras.py`, `pele.css` e
`visor.js`. Editá-lo à mão é o defeito: a próxima geração apaga.

## Acrescentar um degrau

Um degrau só entra **depois de lido**. O procedimento é:

1. abra o capítulo na fonte e encontre a passagem em que o autor diz o que esta
   camada faz com o número;
2. acrescente o degrau em `DEGRAUS`, com a tese (até 25 palavras), o corpo (até
   60), as palavras novas que ele usa em `palavras` (o que é, por que existe),
   a **passagem literal** em inglês e a tradução ao lado, a fonte e o
   capítulo, e o selo; uma palavra técnica nova entra também na lista
   `TECNICAS` de `gerar_site.py`, com o degrau em que nasce;
3. acrescente a figura em `figuras.py`, com a palavra nova como rótulo dentro
   dela;
4. acrescente a estação do degrau em `TRILHA` (o que o "o" virou aqui);
5. se o degrau fechar um buraco, remova a linha correspondente de `A_LER`;
6. `python3 gerar_site.py`.

O gerador **aborta** se a passagem estiver vazia, se a figura não existir, se
a tese ou o corpo passarem do orçamento, se sobrar inglês no texto visível,
se uma palavra técnica aparecer antes do degrau que a explica, ou se uma
palavra de método aparecer na página. É proposital: degrau sem warrant não é
desenhado, e página que fala para quem já sabe não é publicada.

Confira que ele ainda aborta:

```bash
python3 conferir_degraus.py
```

Ele planta cada defeito numa cópia e exige o aborto. Conferência que nunca
reprovou não vale nada.
