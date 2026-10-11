# WardSync: GenAI Civic Issue Discovery, Intelligence & Action Platform

An integrated, production-oriented civic intelligence system that automates the entire lifecycle of urban civic failures: from multi-source signal ingestion and AI verification, to semantic clustering, statutory authority mapping, and community volunteer mobilization.

---

## 1. Connected Architecture Overview

WardSync connects three dedicated sub-projects located in this repository:

```
wardsync/
├── civic_engine/               # Multi-provider GenAI Civic Discovery & Action Engine
│   ├── app/
│   │   ├── api/v1/             # REST endpoints (/sources, /issues, /stakeholders, /opportunities, /analytics)
│   │   ├── ingestion/          # Multi-format connectors (News, Web, RSS, PDF, DOCX, CSV, TXT, OCR)
│   │   ├── matching/           # Hybrid deduplication (Semantic, Haversine, Temporal, Category)
│   │   ├── stakeholders/       # Statutory authority directory (KMC, BBMP, BMC, Jal Board)
│   │   ├── opportunities/      # Action generator (Volunteer drives, Petitions, RTIs, Audits)
│   │   └── providers/          # Multi-provider AI (Gemini, OpenAI, Anthropic, Mock)
│   └── tests/                  # 29 passed unit & integration tests
│
├── civic_pipeline/             # Multi-Signal Verification & NGO Dispatch Engine
│   ├── app/
│   │   ├── routes/             # Ingestion, NGO feeds, volunteer events, public map clusters
│   │   ├── ai/                 # Gemini 1.5 Flash verification, text-embedding-004 clustering
│   │   ├── models/             # Strict Pydantic schemas (Signals, Credibility 0-100, Action Blueprints)
│   │   └── database.py         # Stateful repository with in-memory & pgvector modes
│   └── tests/                  # 8 passed unit & integration tests
│
├── wardsync-frontend/          # Full React 19 + Vite 8 + TypeScript Application
│   ├── src/
│   │   ├── components/         # Map pins, Nearby issues grid, Dashboards, Modals (Citizen, NGO, Gov)
│   │   ├── services/api.ts     # Live network client syncing state with Unified Backend
│   │   ├── types/              # Rich data models (Issue, EvidenceSource, VolunteerSlot, NgoEvent)
│   │   └── App.tsx             # Main interactive application
│   └── vite.config.ts          # Vite dev server with proxy routing /api -> http://127.0.0.1:8000
│
├── unified_server.py           # Unified Backend Gateway connecting both engines & frontend
├── run.py                      # Single-command launcher for unified backend
├── start_all.bat               # Windows batch launcher (launches backend & frontend)
├── start_all.ps1               # PowerShell launcher (launches backend & frontend)
└── test_unified.py             # End-to-end integration test suite
```

---

## 2. How the Three Folders Connect

```
                        ┌────────────────────────────────────────────────────────┐
                        │          wardsync-frontend (Port 5173)                 │
                        │   - Interactive Map with Ward Pins                     │
                        │   - Citizen Reporting Modal                            │
                        │   - Volunteer Registration & NGO Mobilization Modals   │
                        │   - Multi-persona Dashboards (Citizen, NGO, Govt)      │
                        └───────────────────────────┬────────────────────────────┘
                                                    │
                                  Vite Proxy: /api -> http://127.0.0.1:8000
                                                    │
                        ┌───────────────────────────▼────────────────────────────┐
                        │            unified_server.py (Port 8000)               │
                        │               Unified Backend Gateway                  │
                        ├───────────────────────────┬────────────────────────────┤
                        │  Frontend Adapter Bridge  │  System Health & Telemetry │
                        │  - GET  /api/public/issues│  - GET  /health            │
                        │  - POST /api/public/issues│  - GET  /api/health        │
                        │  - POST /api/donations    │                            │
                        │  - PATCH /api/issues/status│                           │
                        └─────────────┬─────────────────────────────┬────────────┘
                                      │                             │
          ┌───────────────────────────▼──┐               ┌──────────▼────────────────────┐
          │        civic_pipeline        │               │         civic_engine          │
          ├──────────────────────────────┤               ├───────────────────────────────┤
          │ - POST /api/ingest/multi-src │               │ - POST /api/v1/sources (Docs) │
          │ - GET  /api/public/map-clust │               │ - GET  /api/v1/issues         │
          │ - POST /api/events/publish   │               │ - GET  /api/v1/stakeholders   │
          │ - POST /api/events/register  │               │ - POST /api/v1/opportunities  │
          │ - GET  /api/ngos/{id}/feed   │               │ - GET  /api/v1/analytics      │
          │ - Gemini Credibility Scoring │               │ - Multi-Provider (Gemini/OAI) │
          │ - Vector-based Clustering    │               │ - Authority Escalation & SLAs │
          └──────────────────────────────┘               └───────────────────────────────┘
```

1. **Signal Aggregation & Proactive Discovery**:
   - `civic_pipeline` ingests raw public signals (social media posts, citizen grievance tickets, news reports).
   - `civic_engine` ingests rich unstructured media (government gazettes, municipal reports, PDFs, CSVs, RSS feeds).

2. **Synthesis & Credibility Scoring**:
   - Uses Google Gemini 1.5 Flash (or configured AI provider) to extract structured problem summaries, categorize issues, and compute 0–100 authenticity scores.
   - When independent news corroborates citizen reports, credibility is boosted dynamically.

3. **Deduplication & Semantic Clustering**:
   - Compares incoming signals using vector embeddings (`text-embedding-004`) and Haversine geo-distance to merge duplicate reports into consolidated civic issues while preserving full evidence provenance.

4. **Stakeholder Mapping & NGO Dispatching**:
   - Matches verified problems with statutory municipal authorities (KMC, BBMP, BMC) and local registered NGOs based on ward boundaries.

5. **Action Generation & Citizen Mobilization**:
   - Generates actionable volunteer blueprints with pre-packaged tasks, safety guidelines, and coordination slots.
   - The frontend renders these live on the interactive map, allowing citizens to RSVP, donate, or track resolution status.

---

## 3. Quick Start Guide

### Step 1: Start the Unified Backend
From the `wardsync` root directory:
```powershell
python run.py
```
*The backend server will start at `http://127.0.0.1:8000` with Swagger documentation at `http://127.0.0.1:8000/docs`.*

### Step 2: Start the Frontend Application
In a separate terminal window:
```powershell
cd wardsync-frontend
npm run dev
```
*The interactive frontend will start at `http://localhost:5173`.*

> **Windows One-Click Shortcut**:
> Double-click `start_all.bat` or run `.\start_all.ps1` in PowerShell to automatically launch both the backend and frontend in separate consoles!

---

## 4. Testing & Verification

### Run End-to-End Unified Integration Tests:
```powershell
python test_unified.py
```
*Tests health checks, issue retrieval, citizen reporting, multi-source signal ingestion, donations, status updates, and analytics.*

### Run Subsystem Unit Tests:
- **Civic Engine (29 tests)**:
  ```powershell
  cd civic_engine
  python -m pytest tests
  ```
- **Civic Pipeline (8 tests)**:
  ```powershell
  cd civic_pipeline
  python -m pytest tests
  ```
- **Frontend Type & Build Verification**:
  ```powershell
  cd wardsync-frontend
  npm run build
  ```

---

## 5. Deployment Guide: GitHub & Render

### Step 1: Push to GitHub

1. Create a new repository on [GitHub](https://github.com/new) (e.g. `wardsync`).
2. Run these commands from your local `wardsync` root directory:
   ```bash
   # Initialize and stage all files (respecting .gitignore)
   git init
   git add .
   git commit -m "Initial commit: WardSync Civic Issue Discovery & Action Engine"

   # Link to your remote GitHub repository and push
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/wardsync.git
   git push -u origin main
   ```

---

### Step 2: Deploy on Render

This repository includes a `render.yaml` blueprint for automated deployment of both the **Backend API** and **Frontend Static Site**.

#### Method A: 1-Click Blueprint (Recommended)
1. Go to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** → **Blueprint**.
3. Connect your `wardsync` GitHub repository.
4. Render will read `render.yaml` and configure:
   - **`wardsync-api`** (Python Web Service)
   - **`wardsync-frontend`** (Static Site)
5. Under Environment Variables for `wardsync-api`, enter your `GEMINI_API_KEY` (or select `mock` for `AI_PROVIDER` if testing without keys).
6. Click **Apply**. Both services will build and deploy automatically!

#### Method B: Manual Deployment

##### 1. Deploy the Backend (`wardsync-api` Web Service):
* **New +** → **Web Service** → Connect your repository.
* **Name**: `wardsync-api`
* **Runtime**: `Python 3`
* **Build Command**: `pip install -r requirements.txt`
* **Start Command**: `uvicorn unified_server:app --host 0.0.0.0 --port $PORT`
* **Environment Variables**:
  - `AI_PROVIDER`: `gemini` (or `mock`)
  - `GEMINI_API_KEY`: `<your_gemini_api_key>`
  - `DATABASE_URL`: `sqlite:///./civic_engine.db`

##### 2. Deploy the Frontend (`wardsync-frontend` Static Site):
* **New +** → **Static Site** → Connect your repository.
* **Name**: `wardsync-frontend`
* **Root Directory**: `wardsync-frontend`
* **Build Command**: `npm install && npm run build`
* **Publish Directory**: `dist`
* **Environment Variables**:
  - `VITE_API_URL`: `https://wardsync-api.onrender.com` (Your backend Render URL)

---

## 6. Open Civic Dataset (Mumbai & Thane)

WardSync includes a 22-attribute standardized dataset for Mumbai & Thane civic failures:
* CSV: `data/mumbai_thane_civic_issues.csv`
* JSON: `data/mumbai_thane_civic_issues.json`
* Live API Endpoints:
  - `GET /api/dataset/mumbai-thane`: Raw 22-column JSON dataset
  - `GET /api/dataset/mumbai-thane/csv`: Downloadable CSV file

---

## 7. API Reference Summary

| Endpoint | Method | Subsystem | Description |
|---|---|---|---|
| `/health` | GET | Unified | System health across all subsystems |
| `/api/public/issues` | GET | Unified Bridge | All verified issues formatted for frontend map & cards |
| `/api/public/issues` | POST | Unified Bridge | Citizen reports new issue with AI verification |
| `/api/dataset/mumbai-thane` | GET | Civic Dataset | Raw 22-column civic dataset in JSON |
| `/api/dataset/mumbai-thane/csv` | GET | Civic Dataset | Raw 22-column civic dataset in CSV |
| `/api/public/map-clusters`| GET | Civic Pipeline | Geo-clusters with active volunteer events |
| `/api/ingest/multi-source`| POST | Civic Pipeline | Multi-source signal ingestion & vector clustering |
| `/api/events/publish` | POST | Civic Pipeline | NGO publishes mobilization event blueprint |
| `/api/events/register` | POST | Civic Pipeline | Citizen registers for volunteer slot |
| `/api/ngos/{id}/actionable-feed` | GET | Civic Pipeline | NGO ward-matched priority feed |
| `/api/donations` | POST | Unified Bridge | Citizen donation recorded |
| `/api/issues/{id}/status` | PATCH | Unified Bridge | Government dashboard status update |
| `/api/v1/sources` | POST/GET | Civic Engine | Ingestion of files (PDF, CSV, RSS, News URLs) |
| `/api/v1/issues` | GET | Civic Engine | List consolidated issues & deduplication |
| `/api/v1/issues/{id}/intelligence` | GET | Civic Engine | Comprehensive Civic Intelligence Dossier |
| `/api/v1/opportunities` | GET/POST | Civic Engine | Generate volunteer, RTI, petition blueprints |
| `/api/v1/analytics/categories` | GET | Civic Engine | Category distribution & priority metrics |
