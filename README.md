# SortVision Pro

A premium, interactive **Sorting Algorithm Visualizer** built with Python
Flask, Bootstrap 5, vanilla JavaScript, and Chart.js — featuring nine
fully-instrumented sorting algorithms, real-time bar animation, side-by-side
comparison, a learning hub, and downloadable execution reports.

![Theme](https://img.shields.io/badge/theme-royal%20navy%20%26%20gold-d4af37)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Flask](https://img.shields.io/badge/flask-3.0-black)

---

## Features

- **Nine algorithms**, each in its own file: Bubble, Selection, Insertion,
  Merge, Quick, Heap, Shell, Counting, and Radix Sort.
- **Array input**: type your own array, or generate a random one with a
  custom size and value range.
- **Full playback control**: Sort, Pause, Resume, Reset, and a live speed
  slider — all driven by a pre-computed step list so playback is smooth and
  interruptible at any point.
- **Six-color visualization language**: Blue (default), Red (comparing),
  Green (swapping), Yellow (current minimum), Purple (pivot), Orange
  (sorted).
- **Compare mode**: run 2+ algorithms on an identical array and see
  execution time, comparisons, swaps, and memory usage charted side by side.
- **Execution statistics**: time, comparisons, swaps, memory usage, array
  length, stability, in-place-ness, and success — for every run.
- **Automatic complexity panel**: best/average/worst-case time and space
  complexity, stability, adaptiveness, and in-place status per algorithm.
- **Learning hub**: description, working principle, advantages,
  disadvantages, real-world applications, and pseudocode for every
  algorithm.
- **Downloadable reports**: export a single run or a full comparison as a
  plain-text report.
- **Dark & light "Royal" themes**: dark navy backgrounds with gold accents
  and glassmorphism cards, toggleable and persisted across visits.
- **Fullscreen visualization mode** for presentations or focused study.

---

## Tech Stack

| Layer      | Technology                                             |
|------------|---------------------------------------------------------|
| Backend    | Python 3.13, Flask, Flask-Blueprint, Flask-CORS, Jinja2 |
| Frontend   | HTML5, CSS3, Bootstrap 5, JavaScript ES6, Chart.js, Font Awesome |
| Algorithms | Pure Python, OOP, fully type-hinted, individually instrumented |
| Deployment | Render, Railway, Docker / docker-compose, Gunicorn      |

No database is required — every run is computed on demand and returned as
JSON; nothing is persisted server-side.

---

## Installation

### 1. Clone and set up a virtual environment

```bash
git clone <your-fork-url> sortvision-pro
cd sortvision-pro
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the development server

```bash
python run.py
# or
flask --app app run --debug
```

The app is now available at **http://localhost:5000**.

> By default, canonical links/sitemap/OG tags point at `http://localhost:5000`.
> Set the `SITE_URL` environment variable once you have a real domain (see
> [docs/HOSTING.md](docs/HOSTING.md)) — no other config changes needed.

### 4. Run with Docker instead

```bash
docker compose up --build
```

The app is now available at **http://localhost:8000**.

---

## Folder Structure

```
sortvision-pro/
├── app.py                     # Flask application factory
├── run.py                     # Local dev entry point
├── config.py                  # Environment-driven configuration
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Procfile                   # Railway / generic Heroku-style deploy
├── render.yaml                # Render blueprint
│
├── algorithms/                # One file per sorting algorithm
│   ├── __init__.py            # ALGORITHM_REGISTRY + get_sorter()
│   ├── base.py                # BaseSorter, StepRecorder, SortResult
│   ├── bubble_sort.py
│   ├── selection_sort.py
│   ├── insertion_sort.py
│   ├── merge_sort.py
│   ├── quick_sort.py
│   ├── heap_sort.py
│   ├── shell_sort.py
│   ├── counting_sort.py
│   └── radix_sort.py
│
├── routes/                    # Flask Blueprints
│   ├── views.py                # HTML page routes (server-renders algorithm content)
│   ├── api.py                   # JSON API routes
│   └── seo.py                    # robots.txt + dynamic sitemap.xml
│
├── utils/                     # Shared helpers
│   ├── array_generator.py      # Random/manual array generation + validation
│   └── helpers.py               # Response envelopes + report text builders
│
├── templates/                 # Jinja2 templates
│   ├── base.html                # SEO meta, Open Graph, JSON-LD, favicons
│   ├── index.html
│   ├── visualizer.html
│   ├── compare.html
│   ├── learn.html               # All algorithm content server-rendered
│   └── 404.html
│
├── static/
│   ├── site.webmanifest
│   ├── img/
│   │   ├── favicon.svg / favicon.ico / apple-touch-icon.png / icon-512.png
│   │   └── og-image.png         # Branded 1200×630 social preview
│   ├── css/
│   │   ├── theme.css            # Design tokens (royal navy & gold)
│   │   └── style.css            # Components & layout
│   └── js/
│       ├── main.js              # Theme toggle, toasts, API helper
│       ├── charts.js            # Chart.js factory helpers
│       ├── visualizer.js        # Main dashboard logic
│       ├── compare.js           # Comparison page logic
│       └── learn.js             # Learning hub panel switcher
│
└── docs/
    └── HOSTING.md              # Full deployment + SEO checklist
```

---

## API Reference

All endpoints are prefixed with `/api` and return a consistent envelope:
`{"success": true, "data": ...}` or `{"success": false, "error": "..."}`.

| Method | Endpoint                        | Description                                  |
|--------|----------------------------------|-----------------------------------------------|
| GET    | `/api/algorithms`                | List all supported algorithms                 |
| GET    | `/api/algorithms/<key>`          | Complexity + learning metadata for one algorithm |
| POST   | `/api/array/random`              | Generate a random array (`size`, `minValue`, `maxValue`) |
| POST   | `/api/array/validate`            | Parse/validate a manually entered array (`raw`) |
| POST   | `/api/sort/<key>`                | Run a sort, returns full step list + stats (`array`) |
| POST   | `/api/compare`                   | Run 2+ algorithms on one array (`array`, `algorithms`) |
| POST   | `/api/export/report`             | Download a plain-text report for one result   |
| POST   | `/api/export/compare-report`     | Download a plain-text comparison report        |

Algorithm keys: `bubble`, `selection`, `insertion`, `merge`, `quick`,
`heap`, `shell`, `counting`, `radix`.

Two additional non-API, non-JSON routes exist for crawlers:
`GET /robots.txt` and `GET /sitemap.xml` (see `routes/seo.py`).

---

## Screenshots

> _Add screenshots of the Home, Visualizer, Compare, and Learn pages here
> once deployed — e.g. `docs/screenshots/visualizer.png`._

| Page       | Preview                        |
|------------|----------------------------------|
| Home       | `docs/screenshots/home.png`      |
| Visualizer | `docs/screenshots/visualizer.png`|
| Compare    | `docs/screenshots/compare.png`   |
| Learn      | `docs/screenshots/learn.png`     |

---

## Deployment Guide

Full, step-by-step instructions (including custom domains, HTTPS, and a
post-deploy SEO checklist) live in **[docs/HOSTING.md](docs/HOSTING.md)**.
Quick summary:

### Render

1. Push this repository to GitHub.
2. In Render, choose **New → Blueprint** and point it at your repo — it
   will read `render.yaml` automatically.
3. Or manually: **New → Web Service**, build command
   `pip install -r requirements.txt`, start command
   `gunicorn --bind 0.0.0.0:$PORT app:app`.
4. Set `SITE_URL` to your Render URL (or custom domain) so canonical
   links, the sitemap, and social previews resolve correctly.

### Railway

1. Push this repository to GitHub.
2. In Railway, **New Project → Deploy from GitHub repo**.
3. Railway auto-detects the `Procfile`; set `SECRET_KEY` and `SITE_URL` in
   the environment variables tab.

### Docker (any host)

```bash
docker build -t sortvision-pro .
docker run -p 8000:8000 -e SECRET_KEY=your-secret -e SITE_URL=https://your-domain.com sortvision-pro
```

See **[docs/HOSTING.md](docs/HOSTING.md)** for the full VPS + Nginx +
Let's Encrypt HTTPS walkthrough.

---

## SEO Features

The app is built to be crawlable and shareable out of the box, not just
functional:

- **Server-rendered content**: every algorithm's description, working
  principle, complexity, and pseudocode is rendered directly into the HTML
  on `/learn` and `/visualizer` (not fetched client-side after load), so
  search engines see full text immediately.
- **Unique per-page `<title>` and meta description** on every route,
  including a dynamically generated title/description per algorithm on
  `/visualizer?algo=<key>`.
- **Canonical URLs** on every page via a shared `canonical_url()` template
  helper, driven by the `SITE_URL` environment variable.
- **Open Graph + Twitter Card tags** (title, description, and a generated
  1200×630 branded preview image at `static/img/og-image.png`) so links
  shared on social media / Slack / Discord render a real preview card.
- **JSON-LD structured data**: `WebApplication` schema site-wide, a
  `HowTo` schema per algorithm on the visualizer page, and an `ItemList`
  schema of all nine algorithms on the learning hub — validate with
  [Google's Rich Results Test](https://search.google.com/test/rich-results).
- **`robots.txt`** and a dynamically generated **`sitemap.xml`**
  (`routes/seo.py`), listing every page plus a deep link per algorithm
  (e.g. `/visualizer?algo=quick`), so algorithm-specific searches can land
  directly on the right page.
- **Semantic heading hierarchy** (one `<h1>` per page, ordered `<h2>`/`<h3>`
  beneath it) and a proper favicon/manifest set for browser tabs and
  home-screen installs.

---

## Coding Standards

- PEP-8 compliant, fully type-hinted, and documented with docstrings.
- Object-oriented algorithm design (`BaseSorter` abstract base class) —
  every algorithm is a small, focused subclass.
- Centralized instrumentation (`StepRecorder`) so every algorithm reports
  comparisons, swaps, execution time, and memory usage identically.
- Input validation and consistent error handling on every API endpoint.
- Modular Flask Blueprints separating page rendering (`routes/views.py`)
  from the JSON API (`routes/api.py`).

---

## Contribution Guide

1. Fork the repository and create a feature branch:
   `git checkout -b feature/my-improvement`
2. Keep new algorithms consistent with `algorithms/base.py`'s `BaseSorter`
   interface, and register them in `algorithms/__init__.py`.
3. Run the app locally and verify the Visualizer, Compare, and Learn pages
   all behave correctly with your change.
4. Submit a pull request describing the change and its motivation.

---

## License

Released under the MIT License. You are free to use, modify, and
distribute this project for personal, educational, or commercial purposes.
