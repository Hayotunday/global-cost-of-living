# 🌍 Global Cost of Living API

> A production-grade REST API powering real-world cost of living comparisons for cities and countries across the globe — built to support [GlobalRelocate](https://globalrelocate.com/), a multilingual relocation platform serving individuals and organizations moving internationally.

[![Live API](https://img.shields.io/badge/Live%20API-online-brightgreen?style=flat-square)](https://global-cost-of-living.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46e3b7?style=flat-square)](https://render.com)
[![Auto-Update](https://img.shields.io/badge/Dataset-Auto--Updated%20Monthly-orange?style=flat-square&logo=github-actions)](/.github/workflows/monthly-update.yml)

---

## 📌 What It Does

The **Global Cost of Living API** provides structured, queryable cost of living data for hundreds of cities and countries worldwide. Given a city and country, it returns **55 standardized cost categories** — from grocery prices and restaurant meals to rent, transportation, education, and average salaries — all normalized in USD.

**Live API:** [https://global-cost-of-living.onrender.com](https://global-cost-of-living.onrender.com)  
**Interactive Docs:** [https://global-cost-of-living.onrender.com/docs](https://global-cost-of-living.onrender.com/docs)

---

## 🎯 The Problem It Solves

Relocating internationally is complex. People and organizations making cross-border moves need reliable, structured cost-of-living comparisons — not scraped web pages or paywalled reports. Existing solutions are:

- **Scattered** across inconsistent sources with no unified query interface
- **Not developer-friendly** — no clean API for integration into products
- **Not multilingual** — most data is English-only, excluding German-speaking markets

This API solves all three by exposing a clean, programmable interface over a comprehensive dataset, with built-in English/German localization support.

---

## 🧑‍💻 My Contribution

This API was built as the **data backbone** for [GlobalRelocate](https://globalrelocate.com/), a multilingual relocation platform I contributed to as a **Frontend & Product Improvement Developer** during its final production phase.

My specific contributions to this project include:

| Area | Contribution |
|---|---|
| **API Design** | Architected all FastAPI endpoints with proper validation, normalization, and error handling |
| **Multilingual Support** | Implemented the full EN/DE bilingual column mapping system (55 categories × 2 languages) |
| **Data Pipeline** | Built the Kaggle dataset ingestion pipeline with path-safe, cross-platform resolution |
| **CI/CD Automation** | Set up GitHub Actions workflow for automated monthly dataset refresh and auto-commit |
| **Deployment** | Configured full Render deployment with auto-deploy on push and environment management |
| **Caching Architecture** | Designed dual-mode caching strategy (in-memory LRU + Redis-ready) for scalability |
| **String Normalization** | Implemented hyphen/case-insensitive matching to handle city name inconsistencies (e.g., `Port-au-Prince` vs `Port au Prince`) |

**Broader context on GlobalRelocate:**  
Beyond this API, I also worked on the React/Next.js frontend across modules covering country taxation, tourism info, city recommendations, country comparison, news aggregation, and an AI-powered country assistant — all serving English and German users.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT / FRONTEND                        │
│              (GlobalRelocate — React / Next.js)              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP POST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌─────────────┐  ┌───────────────┐  ┌──────────────────┐  │
│  │  /city_data │  │ String Normal │  │  Column Mapping  │  │
│  │  (POST)     │  │  -ization     │  │  (EN / DE i18n)  │  │
│  └──────┬──────┘  └───────────────┘  └──────────────────┘  │
│         │                                                    │
│  ┌──────▼──────────────────────────────────────────────┐    │
│  │            Pandas CSV Query Engine                   │    │
│  │   Load → Clean NaN/Inf → Normalize → Filter → Map   │    │
│  └──────┬──────────────────────────────────────────────┘    │
│         │                                                    │
│  ┌──────▼──────────────┐   ┌──────────────────────────┐    │
│  │  data/cost-of-      │   │  cache.py (dual-mode)     │    │
│  │  living_v2.csv      │   │  In-memory LRU / Redis    │    │
│  └─────────────────────┘   └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                         │
         ┌───────────────▼────────────────┐
         │   GitHub Actions (CI/CD)        │
         │   Scheduled: 1st of each month  │
         │   → Kaggle download             │
         │   → Auto-commit updated CSV     │
         │   → Push to repo → Render       │
         │     auto-deploys                │
         └────────────────────────────────┘
```

### Data Flow

1. **Client** sends `POST /city_data` with `{ city, country, language }`
2. **FastAPI** validates inputs and normalizes strings (lowercase, hyphen → space)
3. **Pandas** loads the CSV, cleans `NaN`/`Inf` values, and filters matching rows
4. **Column mapping** renames the raw `x1`–`x55` column codes to human-readable labels in the requested language (EN or DE)
5. Response returned as a JSON array of records

---

## ⚙️ Technologies

| Layer | Technology | Purpose |
|---|---|---|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com) | High-performance async Python API framework |
| **Server** | [Uvicorn](https://www.uvicorn.org/) | ASGI server with WebSocket support |
| **Data Processing** | [Pandas](https://pandas.pydata.org/) + [NumPy](https://numpy.org/) | CSV ingestion, NaN cleaning, filtered queries |
| **Dataset** | [Kaggle API](https://www.kaggle.com/datasets/mvieira101/global-cost-of-living) | Programmatic dataset download |
| **Deployment** | [Render](https://render.com) | PaaS with auto-deploy on git push |
| **CI/CD** | [GitHub Actions](https://github.com/features/actions) | Automated monthly dataset refresh |
| **Caching** (ready) | LRU Cache + Redis | In-memory caching; Redis-ready for scale |
| **Runtime** | Python 3.11 | Modern async runtime |

---

## 🔑 Key Features

- **🌐 Global Dataset** — Covers hundreds of cities across multiple continents
- **📊 55 Cost Categories** — Comprehensive coverage from coffee prices to mortgage interest rates
- **🌍 Bilingual Support** — Response labels available in English (`en`) and German (`de`)
- **🔍 Fuzzy-Tolerant Matching** — Handles hyphenated vs spaced city names (e.g., `Port-au-Prince`)
- **🧹 Clean Data Contract** — `NaN` and `Inf` values are sanitized before returning (no JSON parse errors on client)
- **🤖 Automated Data Freshness** — GitHub Actions refreshes the dataset on the 1st of every month at 3AM UTC
- **⚡ Auto-Deploy Pipeline** — Render redeploys automatically on every push
- **📖 Auto-Generated API Docs** — Swagger UI and ReDoc available out of the box
- **🏥 Health Endpoint** — `/health` confirms dataset availability before serving traffic
- **♻️ Redis-Ready Caching** — `cache.py` provides a dual-mode caching layer (LRU in-memory, upgradeable to Redis with env var)

---

## 📡 API Reference

### Base URL

```
https://global-cost-of-living.onrender.com
```

---

### `GET /` — Live Check

```http
GET /
```

**Response:**
```json
{
  "message": "Global Cost of Living API is live!",
  "status": "ready"
}
```

---

### `GET /health` — Health Check

```http
GET /health
```

Confirms API status and whether the dataset CSV is present.

**Response:**
```json
{
  "status": "healthy",
  "dataset_loaded": true,
  "endpoints": ["/city_data (POST)", "/health (GET)"]
}
```

---

### `POST /city_data` — Get City Cost of Living Data

```http
POST /city_data
Content-Type: application/json
```

**Request Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | `string` | ✅ | City name (e.g., `"Paris"`, `"Port-au-Prince"`) |
| `country` | `string` | ✅ | Country name (e.g., `"France"`) |
| `language` | `string` | ❌ | `"en"` (default) or `"de"` for German labels |

**Example — English:**
```json
{
  "city": "Tokyo",
  "country": "Japan",
  "language": "en"
}
```

**Example — German:**
```json
{
  "city": "Berlin",
  "country": "Germany",
  "language": "de"
}
```

**Response** *(abbreviated)*:
```json
[
  {
    "country": "Japan",
    "city": "Tokyo",
    "Meal, Inexpensive Restaurant": 8.50,
    "Meal for 2 People, Mid-range Restaurant, Three-course": 50.00,
    "Cappuccino (regular)": 4.20,
    "Apartment (1 bedroom) in City Centre": 1400.00,
    "Average Monthly Net Salary (After Tax)": 2800.00,
    "Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate": 1.20
  }
]
```

**Error Responses:**

| Code | Reason |
|---|---|
| `400` | Missing or invalid `city` / `country` field, or unsupported language |
| `404` | No data found for the specified city/country combination |
| `500` | Dataset CSV not found — run `python scripts/update_dataset.py` |

---

## 📂 Data Categories

The 55 cost categories (`x1`–`x55`) are organized across these groups:

| Group | Codes | Examples |
|---|---|---|
| **Dining & Restaurants** | x1–x8 | Inexpensive meal, mid-range dinner for 2, cappuccino |
| **Groceries** | x9–x26 | Milk, bread, eggs, chicken, fruit & vegetables |
| **Tobacco** | x27 | Cigarettes (Marlboro 20-pack) |
| **Transportation** | x28–x35 | Transit pass, taxi, gasoline, new car prices |
| **Utilities** | x36–x38 | Electricity/water bundle, mobile plan, broadband |
| **Leisure & Education** | x39–x43 | Gym, tennis court, cinema, preschool, international school |
| **Clothing** | x44–x47 | Jeans, summer dress, Nike shoes, leather business shoes |
| **Housing (Rent)** | x48–x51 | 1-bed & 3-bed apartments, city centre vs outside |
| **Real Estate** | x52–x53 | Price per sq ft to buy, city centre vs outside |
| **Salaries & Finance** | x54–x55 | Average net monthly salary, 20-year mortgage rate |

All prices are denominated in **USD**.

---

## 🗂️ Project Structure

```
global-cost-of-living/
├── .github/
│   └── workflows/
│       └── monthly-update.yml   # Scheduled GitHub Actions dataset refresh
├── data/
│   └── cost-of-living_v2.csv    # Kaggle dataset (auto-updated monthly)
├── scripts/
│   └── update_dataset.py        # CLI script to fetch/refresh Kaggle dataset
├── src/
│   ├── main.py                  # FastAPI app: routes, validation, column mapping
│   └── cache.py                 # Dual-mode caching layer (LRU / Redis-ready)
├── render.yaml                  # Render PaaS deployment configuration
├── startup.sh                   # Build phase: install deps + download dataset
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🚀 Setup Instructions

### Prerequisites

- Python **3.11+**
- A [Kaggle account](https://www.kaggle.com/) with an API key (`kaggle.json`)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/global-cost-of-living.git
cd global-cost-of-living
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Kaggle credentials

Place your `kaggle.json` file (from [kaggle.com/settings](https://www.kaggle.com/settings)) at:

- **Linux/macOS:** `~/.kaggle/kaggle.json`
- **Windows:** `C:\Users\<You>\.kaggle\kaggle.json`

Then restrict permissions (Linux/macOS only):
```bash
chmod 600 ~/.kaggle/kaggle.json
```

### 4. Download the dataset

```bash
python scripts/update_dataset.py
```

This fetches the [`global-cost-of-living`](https://www.kaggle.com/datasets/mvieira101/global-cost-of-living) dataset from Kaggle and saves it to `data/cost-of-living_v2.csv`.

### 5. Start the API

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

| URL | Purpose |
|---|---|
| `http://localhost:8000` | Live check |
| `http://localhost:8000/health` | Health check |
| `http://localhost:8000/docs` | Swagger UI (interactive docs) |
| `http://localhost:8000/redoc` | ReDoc documentation |

### Development (auto-reload)

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ☁️ Deployment

This project is configured for one-click deployment on [Render](https://render.com).

### How it works

1. `render.yaml` defines a Python web service pointing to `src.main:app`
2. The **build command** runs `startup.sh`, which installs dependencies and downloads the Kaggle dataset
3. The **start command** launches Uvicorn on Render's dynamic `$PORT`
4. **Auto-deploy** is enabled — every push to the main branch triggers a redeploy

### Deploy steps

1. Push this repo to GitHub
2. Create a new **Web Service** on Render and link your repository
3. Add the following **environment secrets** in Render:
   - `KAGGLE_USERNAME` — your Kaggle username
   - `KAGGLE_KEY` — your Kaggle API key
4. Render reads `render.yaml` and configures everything automatically

---

## 🤖 CI/CD: Automated Dataset Refresh

The [`.github/workflows/monthly-update.yml`](.github/workflows/monthly-update.yml) workflow runs automatically on the **1st of every month at 3:00 AM UTC**.

```
Cron: 0 3 1 * *
```

**What it does:**
1. Checks out the repository
2. Installs `kaggle` and `pandas`
3. Configures Kaggle credentials from GitHub Secrets (`KAGGLE_USERNAME`, `KAGGLE_KEY`)
4. Downloads the latest dataset via `update_dataset.py`
5. Commits and pushes the updated CSV with a datestamped message
6. Render detects the push → auto-redeploys with fresh data

Can also be triggered manually via **workflow_dispatch** in the GitHub Actions UI.

---

## 🧩 What Makes This Technically Interesting

### 1. Bilingual Column Mapping (`x1`–`x55`)
The raw Kaggle CSV uses opaque column codes (`x1`, `x2`, ..., `x55`). Rather than hard-coding English labels, the API uses a complete bidirectional `COLUMN_MAP` dictionary that maps each code to both English and German labels. A single `language` parameter controls which set of labels the response uses — enabling the same data pipeline to power multilingual frontends without duplicating any logic.

### 2. String Normalization for Robust City Matching
City names in the dataset use inconsistent hyphenation (e.g., `Port-au-Prince` vs `Port au Prince`). The `normalize_string()` function strips, lowercases, and replaces hyphens with spaces — applied to both the query input and the dataset on the fly — ensuring robust lookups without requiring a fuzzy search library.

### 3. NaN/Inf Sanitization for a Reliable Data Contract
Pandas produces `NaN` and `Inf` float values for missing or extreme data points. These are not valid JSON and would crash client parsers silently. The `load_and_clean_csv()` function explicitly replaces all such values with `None` before any response is built, guaranteeing the API always returns valid, parseable JSON.

### 4. Dual-Mode Caching Architecture
`cache.py` is designed to support two caching strategies without changing application code:
- **In-memory LRU cache** (default, zero-dependency) via Python's `functools.lru_cache`
- **Redis** (distributed, enterprise-scale) activated by setting a `REDIS_URL` environment variable

This means the API can scale from a free-tier single instance to a distributed deployment without architectural rework.

### 5. Fully Automated Data Freshness Pipeline
The dataset stays current entirely through automation — no manual intervention needed. GitHub Actions handles the Kaggle download and git commit; Render auto-deploys on push. The API self-maintains as upstream cost of living data updates monthly.

---

## 🧗 Challenges & Solutions

| Challenge | Solution |
|---|---|
| **Raw column codes** (`x1`–`x55`) are unusable in API responses | Built a complete bilingual column mapping dictionary covering all 55 categories in EN and DE |
| **City name inconsistencies** (hyphenated vs spaced) across the dataset | `normalize_string()` normalizes both the query input and the dataset column values before comparison |
| **`NaN`/`Inf` values crash JSON serialization** | Replaced all non-finite values with `None` during CSV load before any response is constructed |
| **Dataset needs to stay current** without manual effort | GitHub Actions cron job pulls the latest CSV and commits it; Render auto-redeploys on push |
| **Kaggle credentials needed at build time** on a cloud host | Stored as GitHub Secrets and Render env vars; `startup.sh` wires them into the build environment |
| **Cross-platform path resolution** | Used `pathlib.Path(__file__).resolve().parent.parent` for reliable root-relative paths on any OS |

---

## 📦 Dependencies

```
fastapi            # Async Python web framework with built-in validation & docs
uvicorn[standard]  # Production-grade ASGI server
pandas             # CSV ingestion, filtering, and column manipulation
kaggle             # Programmatic Kaggle dataset download
```

---

## 📄 License

[MIT License](LICENSE)

---

## 🙏 Data Source

Dataset: [Global Cost of Living](https://www.kaggle.com/datasets/mvieira101/global-cost-of-living) by mvieira101 on Kaggle.

---

## 💬 Support

For bugs, questions, or feature requests, please [open an issue](../../issues).
