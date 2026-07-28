# MakerFlow — AI-Powered Production Planning Assistant
**Competition:** AIC COMPFEST 18 | **Theme:** Smart Manufacturing — AI for the Backbone of the Economy | **Spec Version:** 1.2.0

MakerFlow is an AI-powered production planning assistant designed for Indonesian creative-sector SMEs (UMKM). It automates raw material estimation, cost optimization, and material substitution advisory from curated local datasets, enabling small manufacturers without ERP tools or procurement expertise to plan production accurately before entering the factory floor.

---

## 🚀 Quick Start & Reproducibility Run Contract

### Prerequisites
- Docker Engine 20.10+
- Docker Compose v2+

### Setup & Run Commands

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Add your Gemini API key in .env
# GEMINI_API_KEY=your_actual_key_here

# 3. Launch application containers
docker compose up --build
```

- **Frontend Application:** http://localhost:3000
- **Backend API Server:** http://localhost:8000
- **Interactive API Documentation (Swagger UI):** http://localhost:8000/docs

---

## 🏛️ System Architecture

MakerFlow is structured as a decoupled monorepo with three isolated layers:

```
MakerFlow/
├── frontend/     ← Next.js 14 (App Router) + TypeScript + Tailwind CSS
├── backend/      ← FastAPI + Pydantic v2 + SQLAlchemy + SQLite
└── datasets/     ← External read-only JSON dataset layer (mounted into backend container)
```

### Key Architectural Highlights
1. **Lightweight RAG Pipeline:** Sequential two-call AI inference (`gemini-2.0-flash`). Call 1 classifies the product category; Call 2 performs material estimation & cost optimization over filtered local dataset context.
2. **Deterministic Fallback Map:** `PRODUCT_CATEGORY_MAP` guarantees zero classification failures for fixed MVP demo scenarios.
3. **Decoupled Data Layer:** Datasets are managed independently in `datasets/` root, allowing data scaling without modifying application code.

---

## 📊 Dataset Scope Statement

At MVP stage, MakerFlow operates on a manually curated dataset of **46 raw materials across 5 product categories**, supporting 7 representative demo scenarios:

| # | Product Name | Category ID | Dataset File |
|---|---|---|---|
| 1 | Gelang Macramé / Bracelet Custom | `yarn_craft` | `yarn_craft.json` |
| 2 | Kerajinan Miniatur Rajutan | `yarn_craft` | `yarn_craft.json` |
| 3 | Key Chain Rajut Custom Karakter | `yarn_craft` | `yarn_craft.json` |
| 4 | Key Chain Resin | `resin_craft` | `resin_craft.json` |
| 5 | Figura Kayu | `wood_craft` | `wood_craft.json` |
| 6 | Kemasan Gift Box | `packaging_gift` | `packaging_gift.json` |
| 7 | Totebag Canvas (Custom Draw) | `textile_craft` | `textile_craft.json` |

*Note: Aesthetic/color raw materials (such as dyes, pigments, and yarn colorways) are explicitly excluded from dataset scope as they represent subjective design choices rather than physical production planning constraints.*

---

## 🔌 API Endpoint Reference

| Method | Endpoint | Description | Request Body | Response Body |
|---|---|---|---|---|
| `POST` | `/estimate` | Full planning pipeline (classify → dataset RAG → estimate) | `EstimateRequest` | `EstimateResponse` |
| `POST` | `/plans` | Save a completed production plan to SQLite | `SavePlanRequest` | `SavePlanResponse` |
| `GET` | `/plans` | Retrieve list of all saved production plans | — | `list[PlanSummary]` |
| `GET` | `/plans/{id}` | Retrieve full detail of a single saved plan | — | `PlanDetail` |

---

## ⚖️ License & Credits

Developed for **AIC COMPFEST 18 Preliminary Round**. Built with Next.js, FastAPI, Google Generative AI, and Tailwind CSS.
