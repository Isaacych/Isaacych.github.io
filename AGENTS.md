# AGENTS.md

Guidance for AI agents working in this repository. Read this before making changes.

## What this repository is

A personal research website for **Dr. Chi-Hong Isaac Yuen**, built with
[Jekyll](https://jekyllrb.com/) and the **Minimal Mistakes** theme. It is a
**project site** published on GitHub Pages.

- Repo / remote: `Isaacych/isaacych.github.io` (`https://isaacyuen.com/`)
- Live URL: `https://isaacyuen.com/`
- Deploy: the default branch (`master`) auto-deploys on every push via GitHub Pages.
  There is **no CI workflow, Dockerfile, or local build step** — the build happens on
  GitHub. Do not invent a local build pipeline.
- The theme is **vendored in-repo** (`_layouts`, `_includes`, `_sass`), **not** pulled
  as a gem/`remote_theme`. `_config.yml` intentionally has no `theme:` line.

## Do NOT install Jekyll, Ruby gems, or run a local build

This is the most important guardrail. **Do not** attempt to `gem install`/`bundle install`
Jekyll or its dependencies, and do not try to build or serve the site locally.

Reasons:

- The local machine has **system Ruby 2.6.10**, which is too old for the current
  `jekyll`/`rouge`/`public_suffix` stack (they require Ruby ≥ 2.7 / ≥ 3.2). Any
  `gem install` attempt will fail and will leave stray artifacts (e.g. a new
  `~/.gem` directory) that then have to be cleaned up.
- `bundle install` is **broken** on purpose: `Gemfile` says `source; gemspec`, but the
  referenced gemspec no longer exists, so bundler aborts.
- The user has explicitly asked **not to** install Jekyll on this computer.
- Changes take effect via the GitHub Pages build, not through a local run.

**Instead**, verify changes by reasoning about the Jekyll theme from the files themselves
(layouts, includes, `_config.yml`, `_data`). If a live check is truly needed, preview the
already-deployed site at `https://isaacyuen.com/`.
Never write to the system Ruby gem dir (`/Library/Ruby/Gems/...`) or create per-user
gem directories.

## Directory layout

```
index.md            Homepage. Use `layout: home`. (See "Homepage naming" below.)
_pages/             Content pages (Markdown, `layout: single` by default via _config.yml):
                    group.md, news.md, publications.md, research.md
_layouts/           Minimal Mistakes layouts (theme). key ones:
  home.html         Homepage layout — renders ONLY `{{ content }}` (Recent Posts was removed).
  archive.html      Parent of home.html; renders hero + sidebar + content.
  default.html      Outermost layout (html/head/body shell) — everything chains to it.
  single.html       Layout for content pages and posts.
  splash.html       Full-bleed hero layout (no sidebar).
_includes/          ~50 partials used by the layouts (theme). Prefer not to edit unless needed.
_sass/              Minimal Mistakes styles + skins (theme).
_data/
  navigation.yml    Site navigation / menu items.
  ui-text.yml       i18n UI labels (e.g. "Recent posts", pagination). Multi-language.
  publications.yml  AUTO-GENERATED from assets/ref/works.bib by scripts/convert_bib.py.
                    DO NOT EDIT BY HAND — re-run the script after changing the .bib.
assets/             css/, js/, images/ — static site assets and header images.
                    assets/ref/ holds the .bib source of truth; Jekyll ignores it.
scripts/            Local generators (e.g. convert_bib.py); Jekyll ignores the dir.
_config.yml         Site configuration (do not delete; see "Key config" below).
Gemfile, Rakefile   Upstream theme build tooling — NOT functional locally. See above.
package.json        Upstream theme artifact (uglify-js devDep). Not used for the site build.
staticman.yml       Optional comment backend (comments are currently disabled).
```

There is currently **no `_posts/` directory** (the site has no blog posts yet). Post
front matter defaults (`layout: single`, `author_profile`, `read_time`, `share`,
`related`) are declared in `_config.yml` `defaults:`.

## Key config (`_config.yml`)

- `url: https://isaacyuen.com/`, `baseurl: ""` — a GitHub Pages **project**
  site, so all URLs are rooted at `""`.
- `repository: Isaacych/isaacych.github.io` — used by jekyll-paginate/sitemap.
- Theme source is vendored; `minimal_mistakes_skin: "air"`.
- `plugins: [jekyll-paginate, jekyll-sitemap, jekyll-gist, jekyll-feed, jekyll-include-cache]`,
  mirrored in `whitelist:` for GitHub Pages (which builds with `--safe`, loading only
  whitelisted plugins).
- `paginate: 5` / `paginate_path: /page:num/` — **currently unused** (the Recent Posts
  rendering that consumed it was removed from `home.html`). Safe to delete these and the
  `jekyll-paginate` entries later, but harmless as-is.
- Author details (name, email, avatar, bio, social/footer links) live under the top-level
  `author:`, `footer:`, and `social:` blocks.

## Homepage naming (do not revert)

The homepage is `index.md`, **not** `index.html`. Jekyll only runs Markdown→HTML on
`markdown_ext` files, so an `index.html` would have rendered its Markdown literally.
Do not rename `index.md` back to `index.html`, and do not create a competing
`index.html` at the repo root.

## How to make typical changes

- **Homepage content:** edit `index.md` body (below the front matter). Front matter uses
  `layout: home`, `author_profile: true`, an explicit `title:` (e.g. `Home`), and a
  `header.image` + `image_description`. The explicit `title` is REQUIRED: without it,
  GitHub Pages' always-on `jekyll-titles-from-headings` plugin infers the page title
  from the first heading (`## Welcome`), and `archive.html` then renders an
  `<h1 class="page__title">` that duplicates the in-body `## Welcome` heading
  (two "Welcome"s). Never rely on the inferred title for `index.md`.
- **New page:** add a Markdown file to `_pages/` with a `layout: single` (and usually
  `author_profile: true`) front matter and a `permalink:` (e.g. `/research/`).
- **Edit existing pages:** `_pages/news.md`, `research.md`, `publications.md`,
  `group.md` (all `layout: single`, custom `permalink`).
- **Navigation menu:** `_data/navigation.yml`.
- **Site-wide CSS overrides:** `assets/css/main.scss` — site-wide font size
  (`$doc-font-size: 12px`, set before the theme imports) and custom overrides
  appended after the imports (hero caption, masthead sizes, the research
  page's `figure.tunneling-sequence` gap-less gallery, etc.). This is the
  supported place for style tweaks; don't edit `_sass/` partials for site-
  specific changes.
- **Site-wide text/labels:** `_data/ui-text.yml`; author/footer/social: `_config.yml`.
- **Labels/strings** are i18n-aware: look up `site.data.ui-text[locale]` in includes;
  `site.locale` is `en-US`.

### Figures, sizing, floats, and math

Recurring patterns used on the content pages (especially `_pages/research.md`):

- **Embed a single image/GIF:** use the theme's figure include, e.g.
  `{% include figure image_path="/assets/images/foo.gif" class="..." alt="..." caption="..." %}`.
  Animated GIFs auto-play in the browser — no extra code needed. Keep GIFs
  small: the 800×800 research GIF was compressed 17 MB → 8.3 MB with
  `ffmpeg`'s two-pass palette mode (256 colours, `fps=5`); scaling down or
  fewer colours made it *larger*, so native size + fewer fps won.
- **Embed a video (MP4):** the theme's `figure` include only emits `<img>` —
  it has no `<video>` support — so write the `<figure><video>…</video></figure>`
  as raw HTML in the Markdown (Jekyll renders it; keep `relative_url` on the
  `src`). Use `autoplay loop muted playsinline` so it plays inline and
  automatically like a GIF: browsers block autoplay unless `muted` (fine —
  `N2p.mp4` has no audio track), and `playsinline` stops iOS going fullscreen.
  Add `preload="metadata"` so the page doesn't download the whole file up front.
- **Two media side by side with text wrapping the pair:** wrap both `<figure>`s
  in `<div class="media-cluster align-right">…</div>` placed **above** the text
  that should wrap (a float only wraps later content). `.media-cluster` (defined
  in `main.scss`) is a flex row floated right at two-thirds width, its two media
  splitting the width evenly (each ~one-third); it stacks full-width below the
  `$small` breakpoint. The Research page uses this for `N2p.mp4` + the GIF.
  Add `{: .cf}` under the next heading so it clears the float.
- **Float a single figure right at one-third width so text wraps its left:**
  `class="align-right one-third"` on the figure include, placed above the text
  to wrap. `figure.one-third` is defined in `assets/css/main.scss`; `align-right`
  ships with the theme (floats right at `$small`). Add `{: .cf}` under the next
  heading so it clears the float. (Superseded on the Research page by
  `.media-cluster`, but the pattern and class remain available.)
- **All figure captions are 12px** via a global `figure figcaption { font-size: 1em }`
  override in `main.scss` (the theme default is `$type-size-6` ≈ 9.6px).
- **Sub/superscripts & chemical/state symbols:** there is **no MathJax/KaTeX**
  on the site, so `$...$` never renders — do NOT use it. Use inline HTML
  instead: `<sub>`/`<sup>` for sub/superscripts, `<em>` for italic state
  letters, and Unicode for Greek, e.g. `N<sub>2</sub><sup>+</sup>` → N₂⁺ and
  `<em>X</em><sup>2</sup>Σ<sub>g</sub><sup>+</sup>` → *X*²Σ_g⁺.
- Front matter variables such as `relative_url`, `post.url`, `site.xxx` are rendered by
  GitHub Pages — write Liquid, don't pre-resolve paths yourself.

## Publications page (generated from a .bib)

The Publications page (`_pages/publications.md`) does not hand-list papers. The list is
generated from the BibTeX source of truth `assets/ref/works.bib`:

```
assets/ref/works.bib  ──( python3 scripts/convert_bib.py )──▶  _data/publications.yml
                                                                   │
                 _includes/publications.html  renders  site.data.publications
```

Workflow when a paper is added/edited:

1. Edit `assets/ref/works.bib` (the only source of truth).
2. Run **`python3 scripts/convert_bib.py`** (pure stdlib — no installs, no Jekyll build).
   It writes `_data/publications.yml` and prints a preview + a "problem check" so you can
   eyeball the cleaned titles (the .bib titles carry MathML/`$LaTeX$` chemical formulas
   that the script normalises; a few keys are hard-coded in `TITLE_OVERRIDES`).
3. Commit the regenerated `_data/publications.yml` **and** the `.bib` together, plus
   `scripts/convert_bib.py` if it changed.

Guardrails:

- **Do NOT hand-edit `_data/publications.yml`.** It is marked "AUTO-GENERATED / DO NOT
  EDIT BY HAND" at the top; any manual change is overwritten on the next run.
- Running `python3 scripts/convert_bib.py` is fine — it neither installs gems nor builds
  Jekyll, unlike the forbidden local Jekyll steps above. `python3` is expected to exist
  (a miniconda env is on the `phys` path); the script needs only the stdlib.
- The `.bib`, the generator, and this planning doc are **excluded from the Jekyll build**
  (`_config.yml` `exclude:` lists `scripts`, `assets/ref`, `plan.md`), so they stay in the
  repo but are never published to the live site.

## Conventions and cautions

- Files under `_layouts/`, `_includes/`, `_sass/` are **upstream Minimal Mistakes theme
  code**. Prefer changing user content (`index.md`, `_pages/`, `_config.yml`, `_data/`).
  When a theme file must change, keep edits minimal and consistent with the existing
  Liquid style, and remember the change affects every page that chains through that layout.
- `_config.yml` excludes a lot of theme dev cruft (`vendor`, `_docs`, `_test`,
  `Gemfile`, `node_modules`, etc.); don't reintroduce it.
- `_site/`, `Gemfile.lock`, `node_modules`, `*.gem`, `.DS_Store` are gitignored — never
  commit generated output.
- The Rakefile tasks (`rake preview`, `js`, `version`, …) run under bundler and will fail
  locally for the reasons above; ignore them.

## Committing

- Work on `master`; push to `origin` — GitHub Pages deploys automatically.
- Keep commits scoped and described in the imperative mood.
