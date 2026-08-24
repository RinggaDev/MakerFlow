# 🏭 MakerFlow — AI-Powered Production Planning Assistant

**Competition:** AIC COMPFEST 18 | **Theme:** Smart Manufacturing — AI for the Backbone of the Economy | **Spec Version:** 1.5.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-v1.5.0--MVP-blue.svg)](https://github.com/RinggaDev/MakerFlow)
[![Frontend](https://img.shields.io/badge/Next.js-16.0%20(React%2019)-black.svg?logo=next.js)](https://nextjs.org/)
[![Backend](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![AI Engine](https://img.shields.io/badge/Google%20GenAI-Gemini%202.0%20Flash-4285F4.svg?logo=google)](https://ai.google.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6.svg?logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB.svg?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose%20v2-2496ED.svg?logo=docker)](https://www.docker.com/)

---

## 📌 Executive Summary

**MakerFlow** is an intelligent, domain-grounded production planning platform built specifically for Indonesia's creative-sector Micro, Small, and Medium Enterprises (UMKM / SMEs). 

In traditional manufacturing, enterprise ERP systems (like SAP or Oracle) are cost-prohibitive, while static spreadsheets lack automated domain intelligence. Small artisans and craft manufacturers often face inaccurate material estimations, unvalidated budget risks, and zero visibility into cost-saving material substitutions before production begins.

MakerFlow solves this by operating directly at the **pre-production planning phase**. Powered by a sequential two-call Large Language Model (LLM) pipeline and a **Lightweight Grounded RAG** architecture over curated Indonesian raw material datasets, MakerFlow transforms high-level product specifications into complete Bill of Materials (BOM), budget sufficiency diagnostics, supplier procurement channels, and reverse affordable quantity calculations in under 10 seconds.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE MAKERFLOW PROMISE                                   │
├───────────────────────────────┬───────────────────────────────┬─────────────────────────┤
│    ⚡ Sub-10s Planning       │   🛡️ Zero Hallucination       │   🔄 Reverse QTY Logic  │
│  Instant material breakdown   │  Strict grounding on 53 local │  Calculates affordable  │
│  & cost forecast per project. │  SME materials (IDR pricing). │  output if budget fails.│
└───────────────────────────────┴───────────────────────────────┴─────────────────────────┘
```

---

## 🎯 Key Features & Capabilities

### 🤖 **AI & Decision Intelligence Engine**
- **Dual-Call Sequential Pipeline**:
  - **Call 1 (Product Classification)**: Maps single or multi-domain craft inputs into exact category registries (`gemini-3.1-flash-lite`).
  - **Call 2 (Estimation & Optimization)**: Generates granular per-unit & total BOM, cost bounds, and sourcing guidance (`gemini-3.5-flash`).
- **Lightweight Grounded RAG**: Deterministic retrieval and context injection of verified local raw material datasets without vector database overhead.
- **Reverse Quantity Calculation (Task 7)**: Proactively answers *"How many units can I actually manufacture with my current budget?"* whenever capital is insufficient.
- **Graph-Based Material Substitution**: Suggests cheaper or higher-grade alternative materials using pre-mapped substitution relationships to keep projects within budget.

### 📦 **Curated Localized SME Knowledge Base**
- **53 Verified Raw Materials**: Covers 5 core creative industries (Yarn/Macramé, Resin, Woodwork, Gift Packaging, Textiles).
- **IDR Price Bracket Bounds (`min`–`max`)**: Accounts for local market price fluctuations across Indonesian suppliers instead of misleading point estimates.
- **E-Commerce & Supplier Integration**: Actionable procurement channels mapped to Tokopedia, Shopee, and local craft suppliers.

### 💻 **Full-Stack SME Production Suite**
- **Interactive Production Result Dashboard**: 7 visual result sections (A to G) featuring summary cards, horizontal material badges, full BOM breakdown tables, and substitution advice.
- **Production Plan Persistence (CRUD)**: Save generated production plans to local SQLite database with full history inspection and tracking.
- **Cross-Category Hybrid Support**: Native multi-domain planning for complex hybrid crafts (e.g., *Totebag Kanvas dengan Tali Makrame & Pegangan Resin*).

### 🛡️ **Reliability & Enterprise Quality Assurance**
- **Deterministic Category Fallback**: `PRODUCT_CATEGORY_MAP` fallback mechanism guarantees a 0% failure rate across all demo products.
- **Dual-Sided Data Contract (Pydantic v2 & TypeScript)**: Strict end-to-end schema synchronization between FastAPI models and Next.js frontend interfaces.
- **Robust JSON Parsing & Fence Sanitization**: Regex-powered response sanitizers eliminate LLM markdown fence hallucination.

---

## 🏗️ Architecture Overview

MakerFlow adopts a decoupled, multi-tier containerized monorepo architecture separating the data layer, application logic, and presentation interface.

```
                    ┌───────────────────────────────────────────────┐
                    │               CLIENT BROWSER                  │
                    │      Next.js 16 (React 19 + Tailwind v4)      │
                    └───────────────────────┬───────────────────────┘
                                            │ HTTP / JSON (REST)
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │               FASTAPI BACKEND                 │
                    │        (Python 3.11 / Uvicorn Server)         │
                    └───────┬───────────────────────────────┬───────┘
                            │                               │
             ┌──────────────┴──────────────┐ ┌──────────────┴──────────────┐
             │       AI SERVICE LAYER      │ │     DATASET SERVICE LAYER   │
             │  • Gemini 2.0 Flash / Lite  │ │  • Deterministic Routing    │
             │  • Strict Grounded RAG      │ │  • Multi-Domain JSON Merge  │
             │  • Regex Fence Stripping    │ │  • Hard Cap (45 items max)  │
             └──────────────┬──────────────┘ └──────────────┬──────────────┘
                            │                               │
                            ▼                               ▼
             ┌─────────────────────────────┐ ┌─────────────────────────────┐
             │      SQLITE DATABASE        │ │     DATASETS VOLUME (RO)    │
             │  • SQLAlchemy 2.0 ORM       │ │  • 5 Curated JSON Files     │
             │  • Production Plans CRUD    │ │  • Local IDR Price Bounds   │
             └─────────────────────────────┘ └─────────────────────────────┘
```

### End-to-End Execution Flow

```
[User Input Form] (6 fields: product, target_qty, budget, mandatory_material, allow_sub)
       │
       ▼  POST /estimate
[FastAPI Backend - dataset_service.py]
       │
       ├──► 1. AI Call 1: Classify product_name → category_ids & category_labels
       │      └─ Validated against KNOWN_CATEGORY_IDS (Fallback to deterministic map if invalid)
       │
       ├──► 2. Dataset Retrieval & Merging: Load /datasets/{category_id}.json
       │      └─ Filter materials by keyword match + mandatory material lock (capped at 45 items)
       │
       ├──► 3. AI Call 2: Ingest filtered materials into Prompt Context (Grounded RAG)
       │      ├─ Estimate per-unit & total material consumption
       │      ├─ Compute total_cost_min and total_cost_max
       │      ├─ Evaluate budget status (sufficient / insufficient)
       │      └─ Task 7: Reverse Calculation if insufficient:
       │           HPP_per_unit = AVG(min, max) / target_qty
       │           estimated_affordable_qty = FLOOR(budget / HPP_per_unit)
       │
       ├──► 4. Output Validation & Assembly:
       │      └─ Regex fence stripping + Pydantic EstimateResponse serialization
       │
       ▼  200 OK (JSON)
[Next.js Frontend]
       │
       ├──► Visual Sections Rendered (Summary, Status Card, Material Cards, BOM Table, Substitutions, Sourcing)
       └──► Action: Save Production Plan (POST /plans) ──► Persist in SQLite
```

---

## 🛠️ Technology Stack

| Layer | Technology | Version | Purpose & Strategic Rationale |
|---|---|---|---|
| **Frontend Framework** | [Next.js](https://nextjs.org/) | 16.x (React 19) | Modern App Router, optimized SSR/Client hydration, fast UI development |
| **Frontend Styling** | [Tailwind CSS](https://tailwindcss.com/) | 4.x | Utility-first, responsive SME dashboard styling with modern color tokens |
| **Frontend Language** | [TypeScript](https://www.typescriptlang.org/) | 5.x | Strict end-to-end type safety mirroring backend Pydantic contracts |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) | 0.111.0 | Asynchronous execution, native OpenAPI docs generation, high-throughput |
| **Backend Language** | [Python](https://www.python.org/) | 3.11 / 3.12 | Industry standard for AI orchestration and data processing |
| **AI Inference (Dev/MVP)** | [Google Gemini](https://ai.google.dev/) | 2.0 Flash / Lite | Low latency, high token efficiency, official `google-genai` SDK |
| **AI Inference (Release)**| [Anthropic Claude](https://www.anthropic.com/) | Sonnet 4.6 | High-precision structured JSON adherence for enterprise release |
| **Data Validation** | [Pydantic](https://docs.pydantic.dev/) | v2.7.1 | Strict schema validation, business constraint enforcement, request parsing |
| **ORM & Database** | [SQLAlchemy](https://www.sqlalchemy.org/) + [SQLite](https://www.sqlite.org/) | 2.0.30 / 3.x | Lightweight, zero-config, portable relational database for production plans |
| **Containerization** | [Docker Compose](https://docs.docker.com/compose/) | v2+ | Single-command reproducible multi-container orchestration |

---

## 📁 Directory Structure

```
MakerFlow/
├── docker-compose.yml              # Container orchestration & network bridge
├── .env.example                     # Environment template (API keys)
├── .env                             # Active environment configuration (gitignored)
├── .dockerignore                    # Build exclusion rules
├── README.md                        # Primary platform documentation
│
├── datasets/                        # READ-ONLY Data Layer (Mounted as Volume)
│   ├── index.json                   # Category registry & demo product mappings
│   ├── yarn_craft.json              # Yarn & string craft materials (16 items)
│   ├── resin_craft.json             # Resin casting materials (10 items)
│   ├── wood_craft.json              # Woodworking & framing materials (6 items)
│   ├── packaging_gift.json          # Gift boxes & decorative packaging (7 items)
│   └── textile_craft.json           # Textile, canvas & pouch materials (14 items)
│
├── frontend/                        # Next.js 16 Client Application
│   ├── Dockerfile                   # Node 20-alpine container definition
│   ├── package.json                 # NPM dependencies & scripts
│   ├── next.config.ts               # Next.js configuration
│   └── src/
│       ├── app/                     # Next.js App Router pages
│       │   ├── page.tsx             # Landing hero & value proposition
│       │   ├── plan/page.tsx        # Interactive 6-field production planning form
│       │   ├── plan/result/page.tsx # Comprehensive 7-section result dashboard
│       │   └── history/page.tsx     # Saved production plans repository
│       ├── components/              # Reusable React components
│       │   ├── PlanForm.tsx         # Planning form with dynamic conditional fields
│       │   ├── MaterialTable.tsx    # Granular BOM breakdown table
│       │   └── HistoryList.tsx      # Saved plans inspection list
│       ├── lib/
│       │   └── api.ts               # Typed backend API client wrapper
│       └── types/
│           └── index.ts             # TypeScript interfaces (mirroring Pydantic models)
│
├── backend/                         # FastAPI Application Backend
│   ├── Dockerfile                   # Python 3.11-slim container definition
│   ├── requirements.txt             # Python dependencies
│   ├── main.py                      # FastAPI initialization, CORS & router registry
│   ├── api/
│   │   └── routes/                  # API Endpoint controllers
│   │       ├── estimate.py          # POST /estimate (orchestrates dual AI calls)
│   │       ├── plans.py             # POST/GET /plans & GET /plans/{id}
│   │       └── classify.py          # Standalone classification route (internal)
│   ├── services/                    # Core business logic layer
│   │   ├── gemini_service.py        # Gemini AI API caller & JSON extractor
│   │   ├── claude_service.py        # Claude AI client implementation (Release)
│   │   ├── dataset_service.py       # Deterministic routing, JSON merge & filters
│   │   └── plan_service.py          # Production plan CRUD operations
│   ├── models/                      # Pydantic v2 Schema validation
│   │   ├── request.py               # EstimateRequest, SavePlanRequest
│   │   └── response.py              # EstimateResponse, PlanSummary, PlanDetail
│   ├── prompts/                     # Strictly engineered prompt templates
│   │   ├── classify_prompt.py       # Call 1 classifier prompt template
│   │   └── estimate_prompt.py       # Call 2 grounded estimation prompt template
│   └── db/                          # Database persistence layer
│       ├── database.py              # SQLite engine & session maker
│       ├── models.py                # SQLAlchemy ProductionPlan DB schema
│       └── makerflow.db             # Auto-generated SQLite database file
│
└── docs/                            # Architectural specifications & proposals
    ├── Makerflow-SPEC.md            # Canonical technical specification
    ├── Proposal_MakerFlow_AIC_COMPFEST18.md # Academic technical proposal
    └── README_Reference.md          # Architectural documentation benchmark
```

---

## 🚀 Quick Start & Reproducibility Run Contract

### Prerequisites

| Requirement | Minimum Version | Note |
|---|---|---|
| **Docker Engine** | 20.10+ | Required for container runtime |
| **Docker Compose** | v2.0+ (built-in CLI) | Orchestrates frontend and backend |
| **Gemini API Key** | — | Required for AI inference ([Get Key](https://aistudio.google.com/)) |

> 💡 **Zero Local Tooling Required:** You do not need to install Node.js, Python, or SQLite on your host machine. Everything runs isolated in Docker.

### 1. Setup & Launch in 4 Steps

```bash
# Step 1: Clone the repository
git clone https://github.com/RinggaDev/MakerFlow.git
cd MakerFlow

# Step 2: Copy the environment configuration template
cp .env.example .env

# Step 3: Configure your Gemini API Key in .env
# Open .env in your text editor and set:
# GEMINI_API_KEY=your_actual_gemini_api_key_here

# Step 4: Build and launch all services
docker compose up --build
```

### 2. Available Services & Port Mappings

Once started, access MakerFlow services at:

| Service | URL | Description |
|---|---|---|
| **Frontend Web App** | [http://localhost:3000](http://localhost:3000) | Main MakerFlow UI & Planning Dashboard |
| **Backend API Server** | [http://localhost:8000](http://localhost:8000) | FastAPI REST API root |
| **Swagger Interactive Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive Swagger UI API explorer |
| **ReDoc Documentation** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Alternative formatted OpenAPI documentation |

---

## 🔧 Comprehensive Docker Reference Guide

### Build & Execution Commands

```bash
# Build and run containers in foreground (live streaming logs)
docker compose up --build

# Build and run in detached mode (background)
docker compose up --build -d

# Start existing containers without rebuilding
docker compose up -d

# Rebuild a single service only
docker compose build backend
docker compose build frontend

# Clean rebuild without Docker build cache
docker compose build --no-cache
```

### Monitoring, Logs & Health Checks

```bash
# Stream combined logs from all containers
docker compose logs -f

# Stream logs for backend or frontend individually
docker compose logs -f backend
docker compose logs -f frontend

# Inspect running container status
docker compose ps

# Real-time resource usage statistics (CPU, Memory, I/O)
docker stats

# Backend health check from host
curl http://localhost:8000/
```

### Container Shell Access & Debugging

```bash
# Open interactive bash shell in backend container
docker compose exec backend bash

# Open shell in frontend container
docker compose exec frontend sh

# Test SQLite database connection from inside backend
docker compose exec backend python -c "from db.database import engine; print('DB Connection OK!')"

# Inspect mounted read-only datasets in container
docker compose exec backend ls -la /app/datasets/

# Verify active AI environment variables in container
docker compose exec backend env | grep -E "GEMINI|ANTHROPIC"
```

### Teardown & Reset Scenarios

```bash
# Stop containers gracefully
docker compose down

# Stop and wipe SQLite database volume (Database Reset)
docker compose down -v

# Full system reset (Wipe containers, volumes, and built images)
docker compose down -v --rmi all
```

---

## 📊 Dataset Scope & 11 Demo Scenarios

MakerFlow operates on **53 curated raw material items across 5 core categories**, supporting **11 standardized demo scenarios** spanning single-domain and multi-domain cross-category crafts:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DATASET SUMMARY MATRIX                                 │
├──────────────────────────┬────────────────────────┬─────────────┬──────────────────────┤
│ Kategori                 │ File Dataset           │ Jumlah Item │ Skenario Produk      │
├──────────────────────────┼────────────────────────┼─────────────┼──────────────────────┤
│ Kerajinan Benang & Tali  │ yarn_craft.json        │ 16 item     │ Gelang, Boneka Rajut │
│ Kerajinan Resin          │ resin_craft.json       │ 10 item     │ Key Chain Resin      │
│ Kerajinan Kayu           │ wood_craft.json        │ 6 item      │ Figura Kayu          │
│ Kemasan & Gift Box       │ packaging_gift.json    │ 7 item      │ Gift Box & Kemasan   │
│ Kerajinan Tekstil & Kain │ textile_craft.json     │ 14 item     │ Totebag, Pouch       │
├──────────────────────────┴────────────────────────┼─────────────┼──────────────────────┤
│ TOTAL CURATED RAW MATERIALS                        │ 53 item     │ 11 Demo Scenarios    │
└───────────────────────────────────────────────────┴─────────────┴──────────────────────┘
```

### Complete Demo Products Matrix

| # | Demo Product Name | Category ID(s) | Scenario Type | Multi-Domain Breakdown |
|---|---|---|---|---|
| 1 | **Gelang Macramé / Bracelet Custom** | `yarn_craft` | Single-Category | Tali katun, kancing kayu, stopper |
| 2 | **Kerajinan Miniatur Rajutan** | `yarn_craft` | Single-Category | Benang milk cotton, dakron, safety eyes |
| 3 | **Key Chain Rajut Custom Karakter** | `yarn_craft` | Single-Category | Benang katun, ring gantungan, dakron |
| 4 | **Key Chain Resin** | `resin_craft` | Single-Category | Epoxy resin A+B, cetakan silicone, ring |
| 5 | **Figura Kayu** | `wood_craft` | Single-Category | Kayu jati belanda, kaca/akrilik, gantungan |
| 6 | **Kemasan Gift Box** | `packaging_gift` | Single-Category | Hardbox duplex, shredded paper, pita satin |
| 7 | **Totebag Canvas (Custom Draw)** | `textile_craft` | Single-Category | Kain kanvas blacu, benang jahit, webbing |
| 8 | **Gantungan Kunci Resin Kayu Premium + Rumbai** | `resin_craft`, `wood_craft`, `yarn_craft`, `packaging_gift` | **Cross-Category** | Resin + Kayu + Tali Rumbai + Hardbox |
| 9 | **Pouch Kanvas Resleting dengan Gantungan Resin** | `textile_craft`, `resin_craft`, `packaging_gift` | **Cross-Category** | Kanvas + Zipper + Charm Resin + Box |
| 10 | **Paket Kado Figura Kayu & Boneka Rajut** | `wood_craft`, `yarn_craft`, `packaging_gift` | **Cross-Category** | Figura Kayu + Rajutan + Box Kemasan |
| 11 | **Totebag Kanvas dengan Tali Makrame & Pegangan Resin** | `textile_craft`, `yarn_craft`, `resin_craft`, `packaging_gift` | **Cross-Category** | Kanvas + Tali Makrame + Handle Resin + Box |

### Raw Material Data Schema

Every material in `/datasets` adheres to a standardized JSON schema:

```json
{
  "id": "YC001",
  "name": "Tali Macramé Katun",
  "unit": "meter",
  "price_range": {
    "min": 500,
    "max": 1200,
    "currency": "IDR"
  },
  "grade": ["standard", "premium"],
  "common_use": ["gelang macramé", "bracelet", "dekorasi tali"],
  "substitutes": ["YC002"],
  "supplier_platforms": ["Tokopedia", "Shopee"],
  "tags": ["tali", "macramé", "katun", "gelang"]
}
```

### Intentional Curation Principles
- **Aesthetic Independence**: Colors, dyes, and paints are intentionally excluded. Color selection is an artistic preference, whereas MakerFlow focuses strictly on physical production engineering.
- **Price Brackets over Point Estimates**: Real-world SME raw material costs fluctuate. Providing minimum and maximum bounds guarantees realistic financial projections.
- **Pre-computed Substitution Graphs**: Each item contains verified substitute IDs, enabling AI to reason over direct material swaps without hallucinating unavailable alternatives.

---

## 🤖 AI Engine & Iterative Development

MakerFlow executes two specialized LLM calls sequentially for each production request:

```
[Raw User Request]
        │
        ▼
┌────────────────────────────────────────────────────────┐
│  AI CALL 1: Product Category Classifier                │
│  Model: gemini-2.0-flash-lite                          │
│  • Maps product title to 1..N category_ids             │
│  • Strict JSON Key Enforcement                         │
│  • Fallback: PRODUCT_CATEGORY_MAP (Deterministic)      │
└───────────────────────┬────────────────────────────────┘
                        │ category_ids & category_labels
                        ▼
┌────────────────────────────────────────────────────────┐
│  DATASET RETRIEVAL: Lightweight Grounded RAG           │
│  • Reads /datasets/{category_ids}.json                 │
│  • Merges multi-domain materials                       │
│  • Filters by keyword relevance & mandatory lock       │
│  • Enforces context window budget (max 45 items)       │
└───────────────────────┬────────────────────────────────┘
                        │ Filtered Raw Materials Context
                        ▼
┌────────────────────────────────────────────────────────┐
│  AI CALL 2: Estimation, Optimization & Reverse Calc    │
│  Model: gemini-2.0-flash                               │
│  • Strict Grounded Context (FORBIDDEN to invent data)  │
│  • Computes unit BOM & total cost brackets (IDR)       │
│  • Assesses Budget Sufficiency                         │
│  • Task 7: Reverse affordable quantity formula         │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  RESPONSE REFINERY & CONTRACT SERIALIZATION            │
│  • Regex Markdown Fence Stripper                       │
│  • Pydantic v2 EstimateResponse Validation             │
└────────────────────────────────────────────────────────┘
```

### Reverse Quantity Calculation Formula

When a user's budget is insufficient (`budget_status == "insufficient"`), MakerFlow executes Task 7 to calculate how many units the artisan can produce with available capital:

$$\text{HPP}_{\text{per\_unit}} = \frac{\text{total\_cost\_min} + \text{total\_cost\_max}}{2 \times \text{target\_qty}}$$

$$\text{estimated\_affordable\_qty} = \left\lfloor \frac{\text{available\_budget}}{\text{HPP}_{\text{per\_unit}}} \right\rfloor$$

---

## 🔌 API Endpoint Reference

### Summary Table

| Method | Endpoint | Description | Request Body | Response Body |
|---|---|---|---|---|
| `GET` | `/` | System Health Check & Version | — | `{"status": "ok", "message": "MakerFlow API is running"}` |
| `POST` | `/estimate` | Full Planning Pipeline (Classify + Grounded RAG + Estimate) | `EstimateRequest` | `EstimateResponse` |
| `POST` | `/plans` | Persist Production Plan to SQLite | `SavePlanRequest` | `{"plan_id": int, "created_at": string}` |
| `GET` | `/plans` | Retrieve All Saved Production Plans | — | `list[PlanSummary]` |
| `GET` | `/plans/{id}` | Retrieve Single Plan Detail by ID | — | `PlanDetail` |

### Detailed Request & Response Contracts

#### `POST /estimate`
```json
// Request: EstimateRequest
{
  "product_name": "Gantungan Kunci Resin Kayu Premium + Rumbai",
  "target_qty": 50,
  "available_budget": 350000,
  "has_mandatory_material": true,
  "mandatory_material_name": "Epoxy Resin Bening",
  "allow_substitution": true
}
```

```json
// Response: EstimateResponse (Truncated for readability)
{
  "detected_category_ids": ["resin_craft", "wood_craft", "yarn_craft", "packaging_gift"],
  "detected_category_labels": ["Kerajinan Resin", "Kerajinan Kayu", "Kerajinan Benang & Tali", "Kemasan & Gift Box"],
  "product_name": "Gantungan Kunci Resin Kayu Premium + Rumbai",
  "target_qty": 50,
  "available_budget": 350000,
  "estimated_total_cost_min": 420000,
  "estimated_total_cost_max": 580000,
  "budget_status": "insufficient",
  "estimated_affordable_qty": 35,
  "materials_needed": [
    {
      "material_id": "RC001",
      "material_name": "Epoxy Resin Bening (A+B)",
      "qty_per_unit": 0.05,
      "total_qty_needed": 2.5,
      "unit": "kg",
      "estimated_cost_min": 150000,
      "estimated_cost_max": 200000,
      "recommended_grade": "premium",
      "notes": "Bahan utama badan gantungan kunci"
    }
  ],
  "substitution_suggestions": [
    {
      "original_material": "Pita Satin Dekorasi",
      "substitute_material": "Tali Goni Halus",
      "reason": "Mengurangi biaya kemasan sebesar 40% tanpa mengurangi estetika vintage",
      "estimated_saving_min": 25000,
      "estimated_saving_max": 40000
    }
  ],
  "procurement_advice": [
    {
      "material_name": "Epoxy Resin Bening (A+B)",
      "recommended_platform": "Tokopedia",
      "tips": "Beli kemasan jerigen 1kg untuk mendapatkan harga grosir terbaik"
    }
  ],
  "planning_notes": "Anggaran awal tidak mencukupi untuk 50 unit. Disarankan memproduksi 35 unit atau menerapkan substitusi kemasan."
}
```

---

## 🎯 User Journeys & UI Layout

MakerFlow provides a friction-free workflow designed for non-technical artisans:

```
[1. Landing Page] ──► [2. Planning Form] ──► [3. AI Computation] ──► [4. Result Dashboard] ──► [5. Saved History]
  Hero & Overview      6 Input Parameters       Sub-10s Dual Call       7 Visual Sections         Plan Management
```

### Result Page Visual Breakdown (Sections A–G)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ Section A: Input Summary (Product, Multi-Categories, Target Qty, Available Budget)     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Section B: Budget Status Card                                                           │
│   • Status Badge: "Sufficient" (Green) | "Insufficient" (Amber/Red)                     │
│   • Cost Estimate Range: Rp Min – Rp Max                                                │
│   • Reverse Calculation (If Insufficient): "Max Affordable Production: X units"        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Section C: Material Highlights (Horizontal Carousel of Primary Components & Grades)    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Section D: Granular Bill of Materials (BOM) Table                                       │
│   • Material Name | Qty / Unit | Total Required | Unit Price Range | Projected Cost    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Section E: Smart Substitution Suggestions (Cost-Saving Material Swaps)                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Section F: Procurement Advice & Sourcing Platforms (Tokopedia / Shopee / Local Tips)    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Section G: Action Toolbar: [💾 Simpan Rencana]  [📜 Riwayat Produksi]  [➕ Buat Baru]     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚖️ AI Ethics, Governance & Reliability

- **Strict Grounding as an Ethical Imperative**: In manufacturing, inaccurate raw material cost predictions cause direct financial losses for micro-enterprises. MakerFlow enforces strict prompt constraints forbidding the AI from hallucinating unverified materials or arbitrary price points.
- **Transparent Decision Rationale**: Every suggested substitution includes human-readable economic and technical justifications.
- **Data Privacy by Design**: MakerFlow requires no user registration, tracks zero personal identifiable information (PII), and stores production plans in a self-contained local SQLite instance.
- **Realistic Economic Disclaimers**: The platform explicitly informs artisans that generated outputs are data-grounded estimations and recommends final price verification with local distributors.

---

## 📈 Comparative Analysis & Business Impact

### MakerFlow vs Conventional SME Solutions

| Aspect | Manual Planning | Static Spreadsheets | Enterprise ERP (SAP/Oracle) | MakerFlow |
|---|---|---|---|---|
| **Estimation Time** | 1–3 hours | 30–60 minutes | Hours (complex setup) | **< 10 seconds** |
| **Material Intelligence** | Intuition-based | Manual formula lookup | Complex BOM configuration | **Automated Grounded AI** |
| **Substitution Advisory** | Trial & error | Not available | Manual alternative lookup | **Automated Graph-Based** |
| **Reverse QTY Diagnostics**| Manual recalculation | Complex manual goal-seek | Custom scripting required | **Native Task 7 Feature** |
| **Adoption Cost** | High (human error) | Low (labor intensive) | Very High ($10k+ / year) | **Zero / Open-Source** |
| **Technical Barrier** | None | Moderate | High (requires ERP training) | **Zero (Intuitive Web UI)** |

### Business Model Evolution

```
[Phase 1: Open MVP (Current)] ──► [Phase 2: Freemium SaaS] ──────► [Phase 3: B2B Ecosystem]
• Curated static datasets         • Free: 10 plans/mo, 11 demo products • B2B SME ERP integration
• Zero registration required      • Pro: Unlimited plans, real-time      • Marketplace procurement APIs
• Product-market-fit validation     web scraping & PDF report export   • White-label for craft co-ops
```

---

## 🗺️ Project Roadmap

- [x] **Phase 1: Core Foundation & Dataset Curation**
  - [x] Standardized JSON schema for 53 raw materials across 5 craft domains.
  - [x] Docker containerization with read-only dataset volume mounts.
- [x] **Phase 2: Dual-Call AI Pipeline & Grounded RAG**
  - [x] Fast category classification (`gemini-2.0-flash-lite`) with deterministic fallback.
  - [x] Grounded BOM estimation (`gemini-2.0-flash`) with Task 7 reverse affordable quantity formula.
  - [x] Markdown fence regex sanitization and Pydantic v2 contract enforcement.
- [x] **Phase 3: Frontend Dashboard & Persistence**
  - [x] Responsive Next.js 16 + React 19 UI with Tailwind CSS v4.
  - [x] Sections A through G result dashboard visualization.
  - [x] SQLAlchemy 2.0 + SQLite persistence for production plans CRUD.
- [ ] **Phase 4: Real-Time Sourcing & Automation (Planned)**
  - [ ] Real-time e-commerce price scraping pipeline (Tokopedia, Shopee, Indotrading).
  - [ ] Export production plans to branded PDF reports and CSV/Excel sheets.
  - [ ] Multi-region localization for other Southeast Asian handicraft sectors.

---

## 🤝 Contributing & Engineering Standards

1. **Fork the repository** & create your branch (`git checkout -b feat/smart-procurement-filter`).
2. **Follow Semantic / Conventional Commits**:
   - `feat:` for new capabilities.
   - `fix:` for bug and schema corrections.
   - `refactor:` for code restructurings without behavior modification.
   - `docs:` for documentation updates.
3. **Ensure Contract Integrity**: Verify that backend Pydantic models in [`backend/models/`] and frontend TypeScript types in [`frontend/src/types/`] remain perfectly synchronized.
4. **Submit a Pull Request** with a detailed summary of changes.

---

## 📄 License & Acknowledgments

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Developed for **AIC COMPFEST 18 Preliminary Round (2026)**  
*Empowering Indonesian Creative SMEs through Accessible Smart Manufacturing Intelligence.*
