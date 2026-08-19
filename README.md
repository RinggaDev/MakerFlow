# MakerFlow — AI-Powered Production Planning Assistant

**Competition:** AIC COMPFEST 18 | **Theme:** Smart Manufacturing — AI for the Backbone of the Economy | **Spec Version:** 1.5.0

MakerFlow is an AI-powered production planning assistant designed for Indonesian creative-sector SMEs (UMKM). It automates raw material estimation, cost optimization, material substitution advisory, and reverse quantity calculation from curated local datasets, enabling small manufacturers without ERP tools or procurement expertise to plan production accurately before entering the factory floor.

---

## 🚀 Quick Start & Reproducibility Run Contract

### Prerequisites

| Requirement | Minimum Version |
|---|---|
| Docker Engine | 20.10+ |
| Docker Compose | v2+ (built-in `docker compose` CLI) |
| Gemini API Key | Required for AI inference |

> **Note:** Tidak perlu menginstall Node.js, Python, atau dependency lain secara manual. Semua sudah dikemas dalam Docker container.

### Setup & Run Commands

```bash
# 1. Clone repository (jika belum)
git clone https://github.com/RinggaDev/MakerFlow.git
cd MakerFlow

# 2. Copy environment template dan isi API key
cp .env.example .env

# 3. Edit file .env — isi dengan API key yang valid
#    GEMINI_API_KEY=your_actual_gemini_api_key_here
#    ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here  (opsional, untuk production)

# 4. Build dan jalankan seluruh container
docker compose up --build
```

Setelah berhasil, akses aplikasi di:

| Service | URL | Keterangan |
|---|---|---|
| **Frontend (UI)** | http://localhost:3000 | Halaman utama MakerFlow |
| **Backend API** | http://localhost:8000 | FastAPI server |
| **API Documentation** | http://localhost:8000/docs | Swagger UI (interactive) |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |

### Perintah Stop & Cleanup

```bash
# Stop semua container (tekan Ctrl+C pada terminal yang running, atau jalankan):
docker compose down

# Stop + hapus volumes (reset database SQLite):
docker compose down -v

# Stop + hapus semua images yang di-build:
docker compose down --rmi all

# Stop + hapus volumes DAN images (full clean reset):
docker compose down -v --rmi all
```

---

## 🐳 Docker Architecture Overview

### Container Topology

```
┌────────────────────────────────────────────────────┐
│                 Docker Compose                      │
│               makerflow_network (bridge)            │
│                                                     │
│  ┌─────────────────┐      ┌──────────────────────┐ │
│  │   frontend       │      │   backend             │ │
│  │   node:20-alpine │      │   python:3.11-slim    │ │
│  │                  │      │                       │ │
│  │   Next.js 16     │      │   FastAPI + Uvicorn   │ │
│  │   Port: 3000     │ ───► │   Port: 8000          │ │
│  │                  │      │                       │ │
│  │   npm run build  │      │   Gemini AI SDK       │ │
│  │   npm start      │      │   SQLAlchemy + SQLite │ │
│  └─────────────────┘      └──────────┬────────────┘ │
│                                       │              │
│                               ┌───────┴────────┐    │
│                               │  Volume Mounts  │    │
│                               │                 │    │
│                               │ ./datasets → :ro│    │
│                               │ ./backend/db    │    │
│                               └─────────────────┘    │
└────────────────────────────────────────────────────┘
```

### File-to-Container Mapping

| File | Location | Service | Fungsi |
|---|---|---|---|
| `docker-compose.yml` | Root `/` | Orchestrator | Mendefinisikan services, ports, volumes, network |
| `backend/Dockerfile` | `backend/` | `backend` | Build Python 3.11-slim + pip install + uvicorn |
| `frontend/Dockerfile` | `frontend/` | `frontend` | Build Node 20-alpine + npm install + next build |
| `.env.example` | Root `/` | `backend` | Template environment variables (API keys) |
| `.dockerignore` | Root `/` | Both | Exclude `.env`, `node_modules`, `__pycache__` |

### Volume Mounts

| Host Path | Container Path | Mode | Keterangan |
|---|---|---|---|
| `./datasets/` | `/app/datasets/` | `ro` (read-only) | Dataset JSON bahan baku (5 file kategori + index) |
| `./backend/db/` | `/app/db/` | `rw` (read-write) | SQLite database file (`makerflow.db`) — auto-generated |

### Environment Variables

| Variable | Diteruskan Ke | Sumber | Keterangan |
|---|---|---|---|
| `GEMINI_API_KEY` | `backend` | `.env` root | API key Google Gemini untuk AI inference (Call 1 & 2) |
| `ANTHROPIC_API_KEY` | `backend` | `.env` root | API key Anthropic Claude (untuk production/release) |
| `NEXT_PUBLIC_API_URL` | `frontend` | `docker-compose.yml` | URL backend API (default: `http://localhost:8000`) |

---

## 🔧 Docker Commands Reference (Lengkap)

### Build & Run

```bash
# Build dan jalankan seluruh stack (foreground — log muncul di terminal)
docker compose up --build

# Build dan jalankan di background (detached mode)
docker compose up --build -d

# Jalankan tanpa rebuild (jika sudah pernah build)
docker compose up

# Jalankan tanpa rebuild di background
docker compose up -d

# Build ulang hanya satu service
docker compose build backend
docker compose build frontend

# Build ulang tanpa cache (force fresh build)
docker compose build --no-cache
docker compose build --no-cache backend
docker compose build --no-cache frontend
```

### Monitoring & Logs

```bash
# Lihat log semua container (realtime)
docker compose logs -f

# Lihat log backend saja
docker compose logs -f backend

# Lihat log frontend saja
docker compose logs -f frontend

# Lihat 100 baris terakhir log backend
docker compose logs --tail=100 backend

# Cek status container yang sedang berjalan
docker compose ps

# Cek resource usage (CPU, Memory)
docker stats
```

### Stop & Cleanup

```bash
# Stop semua container
docker compose down

# Stop + hapus volumes (RESET DATABASE)
docker compose down -v

# Stop + hapus images yang di-build
docker compose down --rmi all

# Stop + hapus volumes DAN images (FULL RESET)
docker compose down -v --rmi all

# Stop satu service saja
docker compose stop backend
docker compose stop frontend

# Restart satu service
docker compose restart backend
docker compose restart frontend
```

### Debugging & Akses Shell

```bash
# Masuk ke shell container backend (untuk debugging)
docker compose exec backend bash

# Masuk ke shell container frontend
docker compose exec frontend sh

# Test endpoint backend dari dalam container
docker compose exec backend curl http://localhost:8000/

# Jalankan command Python di container backend
docker compose exec backend python -c "from db.database import engine; print('DB OK')"

# Lihat isi file database SQLite
docker compose exec backend ls -la /app/db/

# Lihat isi datasets yang di-mount
docker compose exec backend ls -la /app/datasets/

# Cek environment variables yang aktif di backend
docker compose exec backend env | grep -E "GEMINI|ANTHROPIC"
```

### Rebuild Skenario Umum

```bash
# Skenario 1: Setelah mengubah requirements.txt (backend dependencies)
docker compose build --no-cache backend
docker compose up -d

# Skenario 2: Setelah mengubah package.json (frontend dependencies)
docker compose build --no-cache frontend
docker compose up -d

# Skenario 3: Setelah mengubah source code saja (tanpa dependency change)
docker compose up --build -d

# Skenario 4: Reset database (hapus makerflow.db dan buat ulang)
docker compose down -v
docker compose up --build -d

# Skenario 5: Full clean rebuild dari awal
docker compose down -v --rmi all
docker compose up --build -d
```

---

## 🏛️ System Architecture

MakerFlow is structured as a decoupled monorepo with three isolated layers:

```
MakerFlow/
├── frontend/     ← Next.js (App Router) + TypeScript + Tailwind CSS
├── backend/      ← FastAPI + Pydantic v2 + SQLAlchemy + SQLite
└── datasets/     ← External read-only JSON dataset layer (mounted into backend container)
```

### Key Architectural Highlights

1. **Lightweight RAG Pipeline:** Sequential two-call AI inference. Call 1 (`gemini-2.0-flash-lite`) classifies the product category; Call 2 (`gemini-2.0-flash`) performs material estimation & cost optimization over filtered local dataset context.
2. **Deterministic Fallback Map:** `PRODUCT_CATEGORY_MAP` guarantees zero classification failures for all 11 demo scenarios (7 single-category + 4 cross-category).
3. **Decoupled Data Layer:** Datasets are managed independently in `datasets/` root, mounted read-only into the backend container, enabling data scaling without modifying application code.
4. **Reverse Quantity Calculation:** When budget is insufficient, AI proactively calculates the maximum affordable production quantity based on estimated HPP per unit.

### Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Frontend Framework | Next.js (App Router) | 16.x |
| Frontend Language | TypeScript | 5.x |
| Frontend Styling | Tailwind CSS | 4.x |
| Backend Framework | FastAPI | 0.111.0 |
| Backend Language | Python | 3.11 |
| Backend Server | Uvicorn | 0.29.0 |
| Data Validation | Pydantic v2 | 2.7.1 |
| ORM | SQLAlchemy | 2.0.30 |
| Database | SQLite | Single file |
| AI Provider (MVP) | Google Gemini | `google-genai` SDK |
| Containerization | Docker + Docker Compose | v2 |

---

## 📊 Dataset Scope Statement

At MVP stage, MakerFlow operates on a manually curated dataset of **~53 raw materials across 5 product categories**, supporting **11 representative demo scenarios** including 4 advanced cross-category products:

| # | Product Name | Category ID(s) | Dataset File(s) |
|---|---|---|---|
| 1 | Gelang Macramé / Bracelet Custom | `yarn_craft` | `yarn_craft.json` |
| 2 | Kerajinan Miniatur Rajutan | `yarn_craft` | `yarn_craft.json` |
| 3 | Key Chain Rajut Custom Karakter | `yarn_craft` | `yarn_craft.json` |
| 4 | Key Chain Resin | `resin_craft` | `resin_craft.json` |
| 5 | Figura Kayu | `wood_craft` | `wood_craft.json` |
| 6 | Kemasan Gift Box | `packaging_gift` | `packaging_gift.json` |
| 7 | Totebag Canvas (Custom Draw) | `textile_craft` | `textile_craft.json` |
| 8 | **Gantungan Kunci Resin Kayu Premium + Rumbai** | `resin_craft`, `wood_craft`, `yarn_craft`, `packaging_gift` | Multi-category merge |
| 9 | **Pouch Kanvas Resleting dengan Gantungan Resin** | `textile_craft`, `resin_craft`, `packaging_gift` | Multi-category merge |
| 10 | **Paket Kado Figura Kayu & Boneka Rajut** | `wood_craft`, `yarn_craft`, `packaging_gift` | Multi-category merge |
| 11 | **Totebag Kanvas dengan Tali Makrame & Pegangan Resin** | `textile_craft`, `yarn_craft`, `resin_craft`, `packaging_gift` | Multi-category merge |

The system employs a **Strict Grounded RAG** approach, forbidding the AI from hallucinating external materials. Color/aesthetic materials (dyes, pigments, yarn colorways) are explicitly excluded — this is a deliberate product design decision, not a data gap.

---

## 🔌 API Endpoint Reference

| Method | Endpoint | Description | Request Body | Response Body |
|---|---|---|---|---|
| `GET` | `/` | Health check | — | `{ status, message }` |
| `POST` | `/estimate` | Full planning pipeline: LLM classify → dataset RAG → LLM estimate | `EstimateRequest` | `EstimateResponse` (includes `estimated_affordable_qty` if budget insufficient) |
| `POST` | `/plans` | Save a completed production plan to SQLite | `SavePlanRequest` | `{ plan_id: int, created_at: string }` |
| `GET` | `/plans` | Retrieve list of all saved production plans | — | `list[PlanSummary]` |
| `GET` | `/plans/{id}` | Retrieve full detail of a single saved plan | — | `PlanDetail` |

> **Note:** There is no separate `/classify` endpoint. Both AI calls (classification + estimation) are orchestrated inside `POST /estimate`. The frontend makes a single call and receives the complete `EstimateResponse`.

---

## 📁 Directory Structure

```
MakerFlow/
│
├── docker-compose.yml              ← Container orchestration
├── .env.example                     ← Environment template (GEMINI_API_KEY, ANTHROPIC_API_KEY)
├── .env                             ← Actual keys (gitignored)
├── .dockerignore                    ← Docker build exclusions
├── README.md                        ← This file
├── Makerflow-SPEC.md                ← Technical specification (single source of truth)
│
├── datasets/                        ← READ-ONLY data layer
│   ├── index.json                   ← Category registry & file routing
│   ├── yarn_craft.json              ← Yarn/string materials (10 items)
│   ├── resin_craft.json             ← Resin materials (6 items)
│   ├── wood_craft.json              ← Wood materials (7 items)
│   ├── packaging_gift.json          ← Packaging materials (8 items)
│   └── textile_craft.json           ← Textile materials (7 items)
│
├── frontend/                        ← Next.js UI (no business logic)
│   ├── Dockerfile                   ← Node 20-alpine container
│   ├── package.json
│   ├── next.config.ts
│   └── src/
│       ├── app/                     ← Pages (home, plan, result, history)
│       ├── components/              ← UI components (PlanForm, MaterialTable, etc.)
│       ├── lib/api.ts               ← All fetch calls to backend
│       └── types/index.ts           ← TypeScript interfaces
│
└── backend/                         ← FastAPI business logic
    ├── Dockerfile                   ← Python 3.11-slim container
    ├── requirements.txt
    ├── main.py                      ← App instantiation + router registration
    ├── api/routes/                  ← HTTP routes (estimate, plans)
    ├── services/                    ← Business logic (AI, dataset, CRUD)
    ├── models/                      ← Pydantic schemas (request, response)
    ├── prompts/                     ← LLM prompt templates
    └── db/                          ← SQLAlchemy models + SQLite file
```

---

## 🔄 Core Data Flow

```
User Input (PlanForm - 6 fields)
        │
        ▼
  POST /estimate
        │
        ├── Call 1: Gemini Flash-Lite → Product Classification
        │   Output: category_ids[] + category_labels[]
        │   Fallback: PRODUCT_CATEGORY_MAP (deterministic)
        │
        ├── Dataset Retrieval: Load & merge .json files by category_ids
        │   Filter by product keywords + mandatory material
        │   Hard cap: 45 items max
        │
        ├── Call 2: Gemini Flash → Material Estimation + Cost Optimization
        │   Input: filtered materials + user params
        │   Output: materials_needed, costs, budget_status, substitutions
        │   + reverse calculation (estimated_affordable_qty) if insufficient
        │
        └── Response Assembly → EstimateResponse (Pydantic validated)
                │
                ▼
        Result Page (6 sections: A-G)
                │
                ▼
        "Simpan Rencana" → POST /plans → SQLite
```

---

## ⚠️ Troubleshooting

### Container gagal start

```bash
# Cek log error
docker compose logs backend
docker compose logs frontend

# Pastikan port tidak digunakan aplikasi lain
netstat -ano | findstr "3000"
netstat -ano | findstr "8000"
```

### Backend error "AI service error"

```bash
# Cek apakah API key sudah benar di .env
cat .env | grep GEMINI_API_KEY

# Test koneksi ke Gemini API dari container
docker compose exec backend python -c "
from google import genai
import os
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
print('API Key valid!')
"
```

### Database reset

```bash
# Hapus database dan buat ulang
docker compose down -v
docker compose up --build -d
```

### Frontend tidak bisa connect ke backend

```bash
# Pastikan kedua container running
docker compose ps

# Test backend health dari host
curl http://localhost:8000/

# Cek network connectivity
docker network inspect makerflow_makerflow_network
```

---

## ⚖️ License & Credits

Developed for **AIC COMPFEST 18 Preliminary Round** (Deadline: August 25, 2026, 23:55 WIB).

Built with Next.js, FastAPI, Google Generative AI (Gemini), SQLAlchemy, SQLite, and Tailwind CSS.
