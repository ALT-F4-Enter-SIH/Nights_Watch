# ShadowLink AI — Threat Intelligence & Identity Correlation Platform

> Defensive security research · Synthetic dataset only · Educational hackathon demo

---

## 1. Project Overview

**ShadowLink AI** is a defensive, educational AI platform that demonstrates how synthetic identity datasets can be analyzed using correlation algorithms, stylometry, graph intelligence, and machine learning to discover potential relationships — for authorized threat intelligence, security research, and educational purposes only.

Built for the hackathon demo as a complete 14-phase implementation, the project showcases:

- Multi-modal AI correlation engine (8 weighted signals)
- Stylometric fingerprinting (TF-IDF, semantic embeddings, n-grams)
- NetworkX multimodal graph analysis (7 node types / 6 edge types, 5 algorithms)
- Premium dark-themed React frontend with cinematic animations
- Interactive investigation workspace with replay capability
- Professional report generation with exports

---

## 2. Problem Statement

Identity correlation across synthetic and authorized datasets requires:

- **Explainable AI** — black-box scores are unacceptable for defensive work
- **Multi-signal integration** — writing style, behavior, cryptography, infrastructure, aliases
- **Visual explanation** — analysts must understand *why* a correlation exists
- **Synthetic-only safety** — no exposure of real-world identity data
- **Demo-ready polish** — must impress in 3 minutes

Existing tools either over-rely on single signals or fail to provide visual, explainable outputs.

---

## 3. Solution

ShadowLink AI delivers a **complete defensive pipeline**:

1. **Synthetic dataset** (`data/shadowlink_synthetic_dataset.json`) — mock identities with aliases, PGP keys, wallets, writing profiles, behavioral categories, infrastructure metadata
2. **Correlation engine** (8 signals, configurable weights, direct endpoint) — scores identity pairs with explainability
3. **Stylometry service** — TF-IDF cosine, sentence-transformer embeddings, n-gram overlap, punctuation profiles
4. **Graph intelligence** — NetworkX graph with connected components, shortest path, centrality, cluster detection, strongest relationships
5. **Dashboard** — aggregated analytics with animated counters, charts, network mini-graph
6. **Investigation workspace** — 7-tab analyst workflow connected to all features
7. **Replay engine** — cinematic 7-step timeline showing how AI discovered a link
8. **Report generator** — structured document with JSON/CSV export and print

---

## 4. Features (14 Phases)

| Phase | Feature | Status |
|---|---|---|
| 1 | Project scaffolding (FastAPI + React + SQLite) | ✅ Complete |
| 2 | Synthetic dataset generator / loader | ✅ Complete |
| 3 | SQLAlchemy models (Identity, Relation, Investigation) | ✅ Complete |
| 4 | **AI Correlation Engine** — 8 weighted signals | ✅ Complete |
| 5 | **Stylometry** — TF-IDF / cosine / embeddings / n-grams | ✅ Complete |
| 6 | **Behavioral analysis** — temporal patterns, clusters | ✅ Complete |
| 7 | **Graph Intelligence** — NetworkX multimodal | ✅ Complete |
| 8 | **Premium Frontend** — dark theme / routing / components | ✅ Complete |
| 9 | **Intelligence Dashboard** — analytics / charts | ✅ Complete |
| 10 | **Interactive Graph** — SVG interactive / side panel | ✅ Complete |
| 11 | **AI Correlation Page** — animated sequence / reveal | ✅ Complete |
| 12 | **Investigation Workspace** — 7 tabs / workflow | ✅ Complete |
| 13 | **Investigation Replay** — cinematic timeline / play | ✅ Complete |
| 14 | **Report Generation** — structured / exports / print | ✅ Complete |

---

## 5. Architecture

```
shadowlink-ai/
├── backend/
│   ├── routers/          # FastAPI endpoints (correlation, graph, dashboard, investigations)
│   ├── services/         # Business logic (correlation_engine, graph_service, dashboard_service)
│   ├── ml/               # Stylometry (TF-IDF, embeddings, cosine)
│   ├── schemas/          # Pydantic request/response models
│   ├── models/           # SQLAlchemy (Identity, Relation, Investigation)
│   ├── database.py       # SQLite connection
│   └── seeds/            # Synthetic dataset generator / loader
├── frontend/
│   ├── src/
│   │   ├── pages/        # 14 route pages (Dashboard, GraphPage, CorrelationPage, etc.)
│   │   ├── components/   # Layout (Sidebar, TopNavbar, PageHeader), UI (MetricCard, RiskBadge, LoadingSkeleton), Analytics (charts, AnimatedNumber)
│   │   └── App.tsx       # React Router with 10+ routes
│   └── tailwind.config.js # Dark intelligence palette (ink/cyan/violet/success/warning/critical)
└── data/
    └── shadowlink_synthetic_dataset.json
```

**Data flow:** Synthetic JSON → SQLite loader → SQLAlchemy models → Backend services → FastAPI routers → React frontend (fetch /API) → Interactive visualization.

---

## 6. AI Methodology

### Correlation Engine (Phase 4)
- **Signals:** Stylometry · PGP Fingerprint · Wallet Prefix · Behavioral · Infrastructure · Alias Overlap · Time Pattern · Topic Overlap
- **Weights:** Configurable per signal (defaults sum to 1.0)
- **Scoring:** Normalized weighted average with explainability (per-signal scores shown)
- **Endpoint:** `POST /api/correlation/analyze-two`

### Stylometry (Phase 5)
- **TF-IDF** + cosine similarity on text samples
- **Sentence-transformer embeddings** (384-d) — semantic comparison
- **N-gram overlap** — structural pattern detection
- **Punctuation profile** — stylistic fingerprint
- **Direct endpoint:** `POST /api/stylometry/compare` (returns 3-tuple for direct use; DB path uses legacy 6-tuple for compatibility)

### Behavioral (Phase 6)
- **Time-series clustering** — posting cadence, time-of-day bias, session length
- **Topic drift** — vocabulary change tracking
- **Anomaly detection** — unsupervised outliers

### Graph Intelligence (Phase 7)
- **Node types:** Identity · Alias · PGP Key · Wallet · Writing Profile · Behavioral Cluster · Infrastructure
- **Edge types:** Shared Identifier · Writing Similarity · Behavioral Similarity · Wallet Relationship · Metadata Similarity
- **Algorithms:** Connected Components · Shortest Path · Centrality (degree + betweenness) · Cluster Detection · Strongest Relationships
- **Endpoint:** `GET /api/graph`

---

## 7. Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 · FastAPI · SQLAlchemy · SQLite |
| ML / AI | scikit-learn (TF-IDF) · sentence-transformers · NetworkX |
| Frontend | React 18 · TypeScript · Vite · Tailwind CSS |
| Animation | Framer Motion |
| Icons | lucide-react |
| Graph (SVG) | Custom SVG interactive (no external dependency — works without npm install) |

---

## 8. Installation

```bash
# Clone / navigate
cd "sih main"

# Backend setup (Python venv recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install fastapi sqlalchemy pydantic networkx scikit-learn sentence-transformers

# Seed synthetic dataset
python backend/seeds/generate_synthetic_dataset.py
python backend/seeds/load_into_sqlite.py

# Frontend setup
cd frontend
npm install
```

---

## 9. Running Frontend

```bash
cd frontend
npm run dev        # Vite dev server (default port 5173)
npm run build      # Production build
npm run preview    # Preview built files
```

**Routes accessible:**
- `/` — Intelligence Dashboard (Phase 9)
- `/graph` — Interactive Graph (Phase 10)
- `/correlation` — AI Correlation Page (Phase 11)
- `/replay` — Investigation Replay (Phase 13)
- `/investigations` — Investigation Workspace (Phase 12)
- `/reports` — Professional Report (Phase 14)
- Plus: `/stylometry`, `/behavior`, `/infrastructure`, `/evidence`, `/settings`

---

## 10. Running Backend

```bash
# From repo root
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**API endpoints:**
- `GET /api/dashboard`
- `GET /api/graph?min_confidence=0.0`
- `POST /api/correlation/analyze-two`
- `POST /api/stylometry/compare`
- `GET /api/investigations`
- `GET /api/investigations/{id}`
- `GET /api/reports/{report_id}`

---

## 11. Demo Flow (3-Minute Hackathon Pitch)

1. **Open Dashboard** (`/`) — show 4 animated counters + timeline + confidence chart + network mini-graph
2. **Click Investigations** — show operation header + metric cards + tab navigation
3. **Click Graph** — interact with SVG graph: drag nodes, zoom, click node to open intelligence panel (entity details + related + analyze button)
4. **Click Correlation** — type `NightTrader` / `DarkPhoenix`, click `RUN AI CORRELATION`, watch 7-step animated sequence → dramatic `87%` reveal with signal bars
5. **Click Replay** — press `PLAY`, watch cinematic timeline with evidence appearing, finish at final result banner
6. **Click Reports** — show structured document with export buttons (JSON / CSV / Print)

All data is synthetic; defensive disclaimers visible throughout.

---

## 12. Limitations

- **Synthetic data only** — no real-world identity ingestion
- **No live scanning** — no unauthorized network or darknet access
- **AI scores are statistical** — not legal evidence; require human verification
- **Graph visualization** — SVG-based (not full Cytoscape/React Flow — sufficient for demo, no npm dependency required)
- **No persistent storage** — SQLite demo database; production would need PostgreSQL + authentication
- **No external API integrations** — all analysis is self-contained

---

## 13. Ethics

- **Defensive only** — designed for authorized security research, educational use, and synthetic dataset analysis
- **No unauthorized scanning** — all outputs include methodology explanations
- **No deanonymization** — synthetic identities have no real-world mapping
- **Transparency** — every score includes per-signal breakdown; every report includes disclaimer
- **Human verification required** — AI outputs labeled as analytical hypotheses

> "This platform demonstrates how synthetic identity datasets can be analyzed using AI to discover potential correlations — for authorized threat intelligence and educational purposes only."

---

*ShadowLink AI — Phase 1–14 Complete · Defensive Security Research · Synthetic Data Only*
