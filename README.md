# Blockspace Forum

Static website for the Blockspace Forum -- an education and research initiative focused on Ethereum's transaction journey and block construction pipeline.

Vanilla HTML/CSS/JS. Python build script generates pages from markdown. Hosted on GitHub Pages.

## Quick Start

```bash
pip install pyyaml markdown
python3 build.py
python3 -m http.server 8000
```

## How It Works

Source markdown lives in `content/`. Build output goes to `generated/`. Static assets live in `assets/`. Root-level HTML files are app shells generated from `templates/`.

Everything renders client-side: `build.py` produces `generated/config.js` with site data, and `js/main.js` reads it to render nav, footer, post lists, events, research, and tooling.

## Contributing

Read **[STYLE.md](STYLE.md)** before making changes. It covers architecture, writing rules, visual design, and the full content pipeline.

## License
MIT + Apache-2.0
