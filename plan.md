# Plan: Drive the Publications page from `assets/ref/works.bib`

Status: **planning complete, nothing implemented yet.** Nothing has been created or
modified yet except this `plan.md`. Start here to continue.

## Goal

Make `_pages/publications.md` list **all** peer-reviewed publications from the BibTeX
file `assets/ref/works.bib`, **grouped by year (newest first)**, each entry showing
authors, title, journal, volume/pages/year, and a DOI link. The `.bib` is the single
source of truth; the rendered list is **generated** from it.

## Hard constraints (do not violate)

From `AGENTS.md` (already in the repo):

- This is a Jekyll + **Minimal Mistakes** site deployed via the **default GitHub Pages
  builder** (GitHub-recommended / no Actions). That builder runs with `--safe` and a fixed
  plugin whitelist: `jekyll-paginate, jekyll-sitemap, jekyll-gist, jekyll-feed,
  jekyll-include-cache`.
  - No custom Ruby, no custom Liquid filters, no jruby, no `bibtex`/`pandoc` at build
    time. So **the Pages server cannot parse the `.bib` itself** — it must be converted
    *before* Jekyll sees it.
- **Do not install Jekyll / Ruby gems, and do not run a local `jekyll build`/`jekyll
  serve`.** System Ruby is 2.6.10 (too old to install the current stack), and `bundle
  install` is broken on purpose (`Gemfile` references a `gemspec` that was removed).
  Verify results by reasoning from the files or by previewing the deployed site, **not**
  by building Jekyll locally.
- **Running a standalone `python3 scripts/convert_bib.py` is allowed** — it is just the
  local data-generation step the user chose; it does not install anything and does not
  build Jekyll. `python3` is available at `/opt/miniconda3/envs/phys/bin/python3`.

## Decisions already made (with the user)

1. **Wiring mechanism: "Local, committed data file."** A pure-Python converter reads
   `assets/ref/works.bib` and writes a Jekyll data file that the site renders. The user
   re-runs only when they add/edit a paper. (Rejected: GitHub Actions live build; rejected:
   hybrid.)
2. **Entry style: "Full references by year."** Group by year, newest first; each entry =
   authors, title, journal, volume, pages, year, DOI link. Show all ~30 entries.
3. **No custom CSS.** Render clean semantic HTML and let the `single` layout's default
   typography style it. Do **not** touch `_sass/**` or add stylesheets.
4. **Source of truth:** `assets/ref/works.bib` (currently **untracked** — must be committed;
   note `assets/ref/works.bib` was just added by the user).

## Messiness in `works.bib` that must be handled

The titles are not clean — they contain MathML and LaTeX fragments that will render
wrongly if dumped raw. The converter must clean them. Notable cases:

- MathML chemical formulas: e.g. `NH<sub>3</sub>`, `O<sub>2</sub>`, `N<sub>2</sub>`,
  `H<sub>2</sub>`, `H2CN`, `CN<sup>−</sup>`. (e.g. `Jiang_2024`, `Yuen_2023a`,
  `Yuen_2019b`, `Yuen_2018`, `Liu_2019`.)
- LaTeX in titles: `{CH}$\mathplus$` → `CH⁺` (`Jiang_2021`); `$\mathplus$`, `$\rightarrow$`
  in `Yuen_2019c`; `{NO}2` → `NO₂` (`Liu_2021`); `NH2CHOH+` → `NH₂CHOH⁺` (`Ayouz_2019`);
  `CH2NH2+` → `CH₂NH₂⁺` (`Yuen_2019a`).
- Isotope notation in `Yuen_2019c`: `16O16O + 18O → 18O16O + 16O` — generalize is risky,
  so **override this title's unicode** (e.g. `¹⁶O¹⁶O + ¹⁸O → ¹⁸O¹⁶O + ¹⁶O`).
- Also `Yuen_2018` reaction: `H2 + D* → HD + H*` → `H₂ + D* → HD + H*`.
- `Liu_2019` (`NO <sub>2</sub>`, a *spaced* subscript) may not be caught by a generic
  letter→digit subscript rule → likely needs a targeted title override too.
- Ignore non-BibTeX fields: `date-modified`, `bdsk-url-1`, `bdsk-url-2`.

**Rule of thumb:** build a general cleaner (tag strip → LaTeX→unicode → protection-brace
removal → unicode subscripts for digits → glued `+`→⁺); then **verify every cleaned title
by running the script and reading its preview output**, adding a small `TITLE_OVERRIDES`
dict (keyed by citation key) for any title the general cleaner doesn't get right (the two
known ones above). Do not eyeball it — run and inspect.

## Files to create / modify

1. **`scripts/convert_bib.py`** (new) — the generator. Pure Python stdlib only
   (`re`, `sys`), **no** `yaml`/`bibtexparser` dependency. Behavior:
   - **Parser:** brace-aware. Find each `@type{key, fields ...}` record by matching
     balanced braces (depth counting), then parse the body into a `name = value` dict.
     Values may be `{...}` (brace-balanced), `"..."` (quoted, backslash-escaped), or a
     bareword (until `,`/`}`). Skip `@Comment`/{`@comment`} records.
   - **Per record**, extract: `key`, `authors`, `title`, `journal`, `volume`, `pages`,
     `year`, `doi`; ignore everything else.
     - `authors`: strip braces, split on `\s+and\s+`, join with `", "`.
     - `title`: clean per the messiness section; apply `TITLE_OVERRIDES` by key if present.
     - `journal`: strip literal-protection braces, collapse spaces.
     - `year`: digits only → int (for grouping/sort).
     - `volume`/`pages`: strip braces; turn `--` into en dash `–`.
     - `doi`/`url`: `url = "https://doi.org/" + doi` (build from `doi`, ignore any `url`
       field that is percent-encoded).
   - **Ordering/grouping:** sort records by `year` descending; preserve `.bib` file order
     within a year. Group into a list of `{ year, entries: [...] }`.
   - **Output:** write `_data/publications.yml` (see structure below). Header comment:
     `# AUTO-GENERATED from assets/ref/works.bib by scripts/convert_bib.py — DO NOT EDIT
     BY HAND. Re-run the script after changing the .bib.` Emit strings as **double-quoted
     YAML scalars** with `\` and `"` escaped; `year`/`volume`/`pages` as bare numbers when
     numeric. Make it idempotent (safe to re-run) and print a preview table to stdout
     (`year | authors | journal | doi` plus the raw vs cleaned titles) so it can be
     verified without a Jekyll build.
2. **`_data/publications.yml`** (new, generated) — structure:
   ```yaml
   - year: 2026
     entries:
       - key: Yuen_2026c
         authors: "Yuen, Chi-Hong, Hosseini-Zavareh, Sajed, ..."
         title: "Identification of molecular isomers using laser-induced electron diffraction"
         journal: "Communications Chemistry"
         volume: "2"     # omit when absent
         pages: "123"    # omit when absent
         doi: "10.1038/s42004-026-02189-y"
         url: "https://doi.org/10.1038/s42004-026-02189-y"
   ```
3. **`_includes/publications.html`** (new) — renders the list from `site.data.publications`:
   ```liquid
   {% for group in site.data.publications %}
     <h3 class="page__title-sm">{{ group.year }}</h3>
     <ul class="publications__list">
       {% for e in group.entries %}
         <li class="publications__item">
           <strong class="publications__authors">{{ e.authors }}</strong>,
           <a class="publications__title" href="{{ e.url | relative_url }}" target="_blank" rel="noopener">{{ e.title }}</a>
           <div class="publications__journal">{{ e.journal }}{% if e.volume %}, <strong>{{ e.volume }}</strong>{% endif %}{% if e.pages %}, {{ e.pages }}{% endif %} ({{ e.year }})</div>
           <a class="publications__doi" href="{{ e.url | relative_url }}" target="_blank" rel="noopener">DOI</a>
         </li>
       {% endfor %}
     </ul>
   {% endfor %}
   ```
   (`relative_url` on an absolute `https://doi.org/...` URL passes it through unchanged.)
4. **`_pages/publications.md`** (modify) — keep the front matter (`title`,
   `permalink: /publications/`, `layout: single`, `author_profile: true`) and the Google
   Scholar link; **replace** the hand-written "Selected Recent Work" / "Additional Research
   Contributions" sections with an intro line + `{% include publications.html %}`.
   Suggested intro: *"All of my peer-reviewed publications are listed below, grouped by
   year. A complete, continuously updated citation record (with citation counts) is on
   [Google Scholar](…)."*
5. **`AGENTS.md`** (modify) — add to the workflow notes: `.bib → _data/publications.yml`
   via `python3 scripts/convert_bib.py`; "do not hand-edit the generated
   `_data/publications.yml`; the `.bib` is the source." (Keep the "don't install Jekyll"
   guardrail intact.)
6. **Commit** `assets/ref/works.bib` (currently untracked), `scripts/convert_bib.py`,
   `_data/publications.yml`, `_includes/publications.html`, updated `_pages/publications.md`
   and `AGENTS.md`, plus this `plan.md`. `git add` these explicitly; do **not** sweep in
   any unrelated untracked files.

## Verification (no Jekyll build)

- Run `python3 scripts/convert_bib.py`; read its stdout preview and the written
  `_data/publications.yml`. **Confirm all ~30 titles are clean** (no `<mml>`, no `$`, no
  stray braces, subscripts/superscripts correct). Fix any bad title via `TITLE_OVERRIDES`
  and re-run until all are clean.
- Sanity-check the Liquid in `_includes/publications.html` by inspection (nested
  `site.data.publications` → `group.entries`). No local Jekyll build.
- Optionally preview the **already-deployed** page later, or after pushing via GitHub Pages.

## Open / confirm during execution

- Within-year ordering: plan preserves `.bib` file order (fine for a "by year" list);
  switch to sort-by-key or author if the user prefers.
- Whether to include the `number`/issue field (currently: volume + pages only, not the
  issue number, to keep it clean).
- `TITLE_OVERRIDES` final contents once the cleaned preview is inspected.

## Notes for a fresh session

- Working dir: the repo root (a git repo, branch `master`, remote
  `https://github.com/Isaacych/website.git`). `baseurl: /website` (GitHub Pages project
  site), live at `https://isaacych.github.io/website/`.
- `python3` (miniconda `phys` env) is available; `node`/`pandoc`/`bib2x` are **not**;
  `bibtex` exists at `/Library/TeX/texbin/bibtex` but is **not** to be used.
- The `single` layout renders `{{ content }}` with default styling; semantic HTML is enough.
- The current `assets/ref/works.bib` has one entry per year from 2016→2026 (~28–30
  records); re-read it at execution time for the exact set.
