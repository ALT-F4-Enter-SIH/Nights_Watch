
# Night Watch

AI-Powered Threat Intelligence & Identity Correlation Platform — Hackathon Project

## Overview
ShadowLink AI analyzes authorized/synthetic identity datasets to discover relationships between digital identities. It uses AI correlation, graph analysis, and explainable confidence scoring for defensive threat intelligence work.

**Important**: This platform is designed exclusively for defensive, educational, and authorized research purposes. It uses only synthetic/mock data and does not implement attacks, exploitation, or unauthorized scanning.

## Key Features
- Identity ingestion and normalization (JSON/CSV)
- Username and alias correlation (exact + fuzzy matching)
- PGP fingerprint matching
- Cryptocurrency wallet relationship analysis
- Stylometry (writing style similarity) analysis
- Behavioral pattern correlation
- Infrastructure metadata correlation
- Graph-based relationship visualization
- Explainable AI confidence scoring
- Interactive analytics dashboard

## Tech Stack
- Frontend: React, TypeScript, Vite, Tailwind CSS, Framer Motion, React Flow, Recharts
- Backend: Python, FastAPI, SQLite, Scikit-learn, Sentence Transformers, NetworkX, Pandas, NumPy

## Quick Start
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Synthetic dataset (Phase 2)
```bash
python backend/seeds/generate_synthetic_dataset.py
python backend/seeds/load_into_sqlite.py
```

See `data/DATASET.md` for cluster design, field lists, and verification notes.

## Data Note
All datasets must be synthetic/mock/authorized only. No real-world deanonymization.
=======
# Nights_Watch
Nights Watch AI is an AI-powered threat intelligence platform that identifies potential links between fragmented digital identities using stylometry, behavioral analysis, cryptographic identifiers, metadata correlation, and graph intelligence. It provides explainable confidence scores and interactive visualizations for investigations.
>>>>>>> 583046b891ded507121066227554d633e67361bb
