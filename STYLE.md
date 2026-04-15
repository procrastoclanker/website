# Blockspace Forum -- Style & Architecture Guide

Reference for anyone working on this repo. Read this before making changes.


## Architecture

```
blockspace-forum/
├── content/                     Source of truth (human-authored markdown)
│   ├── _banner.yaml             Site-wide announcement banner config
│   └── learn/
│       ├── pbs-101.md           Standalone learn pages
│       ├── pbs-201.md
│       ├── pbs-301.md
│       ├── events/
│       │   └── cannes-2026.md   Event recap pages
│       └── series/
│           └── *.md             Blog-style series posts (ordered by date)
│
├── generated/                   ALL build output (safe to delete and rebuild)
│   ├── config.js                Site config: links, posts, events, research, tooling
│   └── learn/
│       ├── pbs-*.html
│       ├── events/*.html
│       └── series/*.html
│
├── assets/                      ALL static media (human-authored)
│   ├── favicon.ico
│   ├── logo.jpg
│   ├── og-image.png
│   └── learn/
│       ├── *.mp4                Video assets for learn pages
│       └── events/*.png|gif     Images for event recaps
│
├── templates/                   HTML shells used by build.py
│   ├── post.html                Series post template
│   ├── learn-page.html          Standalone learn page template
│   ├── index.html               Landing page
│   ├── learn.html               Learn listing
│   ├── events.html              Events listing
│   ├── research.html            Research listing
│   └── blog.html                Redirect to learn
│
├── css/style.css                Single stylesheet
├── js/
│   ├── main.js                  Nav, footer, all dynamic rendering, banner
│   ├── hex-texture.js           Hero background texture data
│   ├── block-auction.js         Canvas animation (block auction)
│   └── blockspace-viz.js        Canvas animation (blockspace)
│
├── tools/
│   └── animations/              Manim source for video assets
│       └── *.py                 (media/ subdir is gitignored build cache)
│
├── build.py                     Static site builder
├── index.html                   Generated (must stay at root for GitHub Pages)
├── learn.html                   Generated app shell
├── events.html                  Generated app shell
├── research.html                Generated app shell
├── blog.html                    Generated redirect
├── 404.html                     Static error page
├── sitemap.xml                  Generated
└── robots.txt                   Static
```

### Key principle

Source content lives in `content/` and `assets/`. Build output lives in `generated/` (plus root-level HTML shells required by GitHub Pages routing). Never mix the two.


## Build Pipeline

```
content/*.md + templates/*.html
        |
    build.py (python3, needs pyyaml + markdown)
        |
    generated/config.js
    generated/learn/**/*.html
    index.html, learn.html, events.html, research.html, blog.html
    sitemap.xml
```

Run: `python3 build.py`
Clean first: `python3 build.py --clean`

CI (.github/workflows/build.yml) runs on push to main when content/, templates/, or build.py change. Commits generated files back.


## Data Flow

All dynamic content renders client-side:

1. `build.py` reads `content/` markdown and `_banner.yaml`
2. Generates `generated/config.js` containing `SITE_CONFIG` object (posts, events, research, tooling, links, banner)
3. Every page loads `generated/config.js` then `js/main.js`
4. `main.js` reads `SITE_CONFIG` and renders nav, footer, post lists, event cards, research cards, tooling grids, banner

Templates use `{{variable}}` substitution. The `{{base}}` variable handles relative path depth from any generated page back to root.


## Writing Rules

### Language
- No em dashes. Use periods, colons, commas, or parentheses.
- "open source" -- no hyphen, even as adjective.
- "blockspace" is lowercase when used as a noun. "Blockspace Forum" is the brand (capitalized).
- "consensus client" not "beacon client."
- "transaction pipeline" not "MEV supply chain."
- No MEV vocabulary: no "front-running", "sandwiching", "stealing", "MEV strategies", "MEV revenue". "MEV-Boost" is OK only when naming the actual software.
- Relays are auction facilitators, not trust mediators. Frame relays as where the auction happens.
- Drop "relay" from compound terms when possible: "block merging" not "relay block merging."
- Builders are facilitators, not extractors.
- Neutral framing throughout. No grandiose statements. Use concrete mechanisms.
- Don't reveal the punchline early. Build toward conclusions.
- No oversimplified causality.
- Soften unverified statistics.

### Tone
Between academic and developer-oriented. Evidence-led, neutral, precise. Clarity over brevity.

### Content types
- **Series posts** (`content/learn/series/`): Date-ordered educational threads. Frontmatter: title, subtitle, date, source (optional), order.
- **Learn pages** (`content/learn/`): Standalone progressive guides (101/201/301). Frontmatter: title, series, subtitle, order, prev, next.
- **Event recaps** (`content/learn/events/`): Workshop writeups. Frontmatter: title, series, subtitle, order.

### Stat callouts
```markdown
:::stat 84% | of fees in winning blocks come from exclusive transactions:::
```
Renders as large mono number + description. Use sparingly.

### Image captions
Images followed by `*italic text*` are auto-wrapped in `<figure>/<figcaption>`. Also triggers on paragraphs starting with "Source:" or "Data provided by".


## Visual Design

### Palette
- Background: #000000 (primary), #060606 (secondary), #0a0a0a (cards), #0d0d0d (surface)
- Text: #e8e8e8 (primary), #777777 (secondary), #3d3d3d (muted)
- Borders: #161616 (default), #222222 (light)
- Accent: #e8e8e8

### Typography
- Body: Inter
- Headings, nav, stats, labels, meta: JetBrains Mono
- Base: 16px, line-height 1.75

### Breakpoints
- Mobile-first
- 640px, 1024px, 1440px

### UI features
- Auto-generated table of contents on posts with 3+ h2 headings
- Reading time from word count
- 1px scroll progress bar at top of posts
- Subtle fade-up page load animation
- Dark custom scrollbar
- Dismissable announcement banner (config in `content/_banner.yaml`, sessionStorage dismiss)

### Canvas animations
Hero section uses canvas-based background animations. Prefer canvas animations over static images for key visuals.


## Adding Content

### New series post
1. Create `content/learn/series/my-post.md` with frontmatter (title, subtitle, date, order)
2. Run `python3 build.py`
3. Post auto-appears in listings with prev/next navigation

### New learn page
1. Create `content/learn/my-page.md` with frontmatter (title, series, subtitle, order, prev, next)
2. Add navigation links in `js/main.js` `renderLearnIntro()` if it should appear on the learn page
3. Run `python3 build.py`

### New event recap
1. Create `content/learn/events/my-event.md`
2. Add images to `assets/learn/events/`
3. Add event entry to the `events` array in `build.py` `build_config()`
4. Update `content/_banner.yaml` if announcing it
5. Run `python3 build.py`

### New media assets
Place in `assets/learn/` (or `assets/learn/events/` for event media). Reference from markdown using relative paths from the generated HTML location.

### Updating links and metadata
Edit `generated/config.js` directly for links (they're preserved across builds). For events, research, tooling -- edit the hardcoded arrays in `build.py` `build_config()`.


## Deployment

GitHub Pages serves from repo root on main branch. No build step on GitHub's side -- generated HTML is committed. Local dev: `python3 -m http.server 8000`.
