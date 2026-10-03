<!-- idioma: linha gerada por i18n.py -->
> [!NOTE]
> ### 🇧🇷 **[Leia esta página em português →](INSTALACAO.md)**

# Installation

There is no installation to **use**: `pt/index.html` is a self-contained page, opens offline in any modern browser.

## Use

**Windows** — download (Code → Download ZIP, or `git clone`), extract, and double-click `index.html`.

**Linux** — `git clone … && cd hello-world-machine && xdg-open index.html`

**macOS** — the same, with `open index.html`.

**Without Downloading** — <https://mateusalkimim.github.io/hello-world-machine/>

On the page: ← and → on the keyboard, or the buttons with the name of the neighboring step. Clicking on a station of the trail from above takes you to the step. The page remembers where you stopped.

## Regenerate the Page

Only those who need to **edit** require this. Python 3, standard library, no package.

```bash
python3 gerar_site.py        # pt/index.html, the steps
python3 gerar_placa.py       # pt/placa.html, the instrument
python3 gerar_en.py          # en/, derived from the translation table
```

The `pt/index.html` is **derived** from `degraus.py`, `figuras.py`, `pele.css`, and `visão.js`. Editing it by hand is a mistake: the next generation will overwrite it.

## Add a Step

A step only enters **after being read**. The procedure is:

1. Open the chapter in the source and find the passage where the author says what this layer does with the number;
2. Add the step in `DEGRAUS`, with the thesis (up to 25 words), the body (up to 60), the new words it uses in `palavras` (what it is, why it exists), the **literal passage** in English and the translation alongside, the source and the chapter, and the seal; a new technical word also goes into the `TECNICAS` list of `gerar_site.py`, with the step where it is born;
3. Add the figure in `figuras.py`, with the new word as a label inside it;
4. Add the station of the step in `TRILHA` (what the "o" became here);
5. If the step closes a hole, remove the corresponding line from `A_LER`;
6. `python3 gerar_site.py`.

The generator **aborts** if the passage is empty, if the figure does not exist, if the thesis or the body exceed the budget, if English is left in the visible text, if a technical word appears before the step that explains it, or if a word of method appears on the page. It is intentional: a step without a warrant is not drawn, and a page that speaks to those who already know is not published.

Verify that it still aborts:

```bash
python3 conferir_degraus.py
```

It plants each defect in a copy and demands an abort. A **check** that never failed is worthless.