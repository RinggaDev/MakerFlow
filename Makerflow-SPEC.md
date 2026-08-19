# MakerFlow — Master Project Context & Technical Specification
**Version:** 1.5.0 | **Competition:** AIC COMPFEST 18 | **Theme:** Smart Manufacturing — AI for the Backbone of the Economy

> This document is the single source of truth for the MakerFlow MVP. It functions as a `.cursorrules` / system prompt for any AI coding agent entering this codebase. Every architectural decision, constraint, and convention documented here has been finalized. Do not deviate without explicit instruction.

---

## 1. Project Overview & MVP Scope

### 1.1 Product Summary

**MakerFlow** is an AI-powered production planning assistant for Indonesian creative-sector SMEs (UMKM) and mid-scale manufacturers. It solves three simultaneous pain points that currently rely on manual guesswork:

1. **Raw material estimation** — how much of each material is needed for a target production quantity
2. **Cost optimization** — whether the available budget is sufficient, and where savings are possible
3. **Substitution advisory** — recommending alternative materials when budget is insufficient, respecting any materials the user has locked as non-substitutable
4. **Reverse quantity calculation** — if the available budget is insufficient for the target quantity, the AI proactively calculates the maximum affordable production quantity based on the estimated unit cost

The core user interaction is a **single planning flow**: describe your product → AI classifies it → AI estimates materials and costs from a curated local dataset → user receives a structured production plan they can save.

### 1.2 Target Users

- Creative UMKM (home industry, craft sellers, independent makers)
- Mid-scale manufacturers in the creative/craft sector
- Operators without accounting or procurement expertise

### 1.3 Competitive Theme Alignment

| AIC Theme Axis | MakerFlow Position |
|---|---|
| Smart Manufacturing | ✅ Primary — production planning before the factory floor |
| Social Impact | ✅ Targets underserved UMKM segment with no access to ERP |
| AI for Backbone | ✅ Strengthens the production link of the SME value chain |

### 1.4 Agreed MVP Scope — MANDATORY CONSTRAINTS

These constraints are dictated by AIC COMPFEST 18 rulebook (Preliminary Round, Product Requirements) and agreed upon in planning. **No feature outside this scope may be built for the preliminary submission.**

| Constraint | Rule |
|---|---|
| **UI scope** | Single core interaction flow only: input form → AI output display → save plan |
| **No complex auth** | No login, registration, OAuth, or JWT. Session-less or single-session only |
| **No background jobs** | All processing is synchronous, request-response only |
| **No analytics dashboard** | No charts, usage metrics, or aggregation views |
| **No automated pipelines** | No scheduled tasks, cron jobs, or automated data logging |
| **No distributed DB** | Single SQLite file only. No Postgres, Redis, or external DB |
| **AI: static inference only** | No fine-tuning loops, auto-tuning, bulk test scripts, or feedback mechanisms during demo |
| **History page** | Allowed as a simple list of saved plans (GET from SQLite). No filtering, sorting, or pagination required |
| **Color/aesthetic preferences excluded** | Dataset and AI output explicitly exclude color, dye, paint, and pigment recommendations — these are personal preference, not production planning |

### 1.5 Acknowledged Limitations (for Proposal)

> *"At MVP stage, MakerFlow uses a manually curated dataset of ~53 raw materials across 5 product categories, sufficient to support 11 representative demo scenarios including advanced cross-category products. The system employs a Strict Grounded RAG approach, forbidding the AI from hallucinating external materials. The development roadmap includes real-time data integration via e-commerce scraping and expansion to additional product categories in subsequent iterations."*

---

## 2. Final Tech Stack

### 2.1 Frontend

| Layer | Choice | Version |
|---|---|---|
| Framework | Next.js (App Router) | 14.x |
| Language | TypeScript | 5.x |
| Styling | Tailwind CSS | 3.x |
| HTTP Client | Native `fetch` wrapped in `src/lib/api.ts` | — |
| Package Manager | npm | — |

### 2.2 Backend

| Layer | Choice | Version |
|---|---|---|
| Framework | FastAPI | 0.111.0 |
| Language | Python | 3.11 |
| Server | Uvicorn | 0.29.0 |
| Data Validation | Pydantic v2 | 2.7.1 |
| ORM | SQLAlchemy | 2.0.30 |
| Environment | python-dotenv | 1.0.1 |

### 2.3 AI Model Integration

| Layer | Choice | Detail |
|---|---|---|
| Provider (Release) | Anthropic | Claude API (Production standard) |
| Provider (Dev/MVP) | Google AI | Gemini API (Development & MVP) |
| Model Strategy | Hybrid Routing | Call 1: Lightweight (e.g., `gemini-2.0-flash-lite`) for fast classification. Call 2: Heavy Reasoning (e.g., `gemini-2.0-flash` or `claude-sonnet-4-6`) for complex estimation. |
| SDK | Multi-SDK | `google-generativeai` (Dev) / `anthropic` (Release) |
| Call pattern | Two sequential synchronous calls per planning request | See Section 4 |
| Call 1 purpose | Product classification → category detection | |
| Call 2 purpose | Material estimation + cost optimization from filtered dataset | |
| Output format | Structured JSON via prompt instruction | |

### 2.4 Database

| Layer | Choice | Detail |
|---|---|---|
| Engine | SQLite | Single file: `backend/db/makerflow.db` |
| ORM | SQLAlchemy | Declarative models in `backend/db/models.py` |
| Persistence | Docker volume mount | `./backend/db:/app/db` |
| Scope | `production_plans` table only | id, product_name, qty, budget, category, result_json, created_at |

### 2.5 Infrastructure & Deployment

| Layer | Choice | Detail |
|---|---|---|
| Containerization | Docker + Docker Compose | `docker-compose.yml` at monorepo root |
| Network | Internal bridge network | `makerflow_network` |
| Frontend port | 3000 | |
| Backend port | 8000 | |
| Dataset mount | Read-only volume | `./datasets:/app/datasets:ro` |
| Environment secrets | `.env` at monorepo root | `ANTHROPIC_API_KEY` (Release) + `GOOGLE_API_KEY` (Dev/MVP) |

---

## 3. Architecture & Directory Structure

### 3.1 Monorepo Strategy

The repository is a monorepo with **three isolated layers**, each with a distinct responsibility:

```
makerflow/
├── frontend/     ← UI only. Zero business logic. Zero AI calls.
├── backend/      ← API, AI orchestration, DB access. No UI concerns.
└── datasets/     ← External data layer. Mounted read-only into backend container.
```

**Key architectural principle:** `datasets/` lives at the repository root, not inside `backend/`. This signals to reviewers that the data layer is decoupled from application logic and can be updated, replaced, or scaled independently without touching source code. In the proposal, this is described as: *"datasets are managed as an independent layer, enabling scaling and data updates without modifying backend code."*

### 3.2 Full Directory Tree

```
makerflow/
│
├── docker-compose.yml
├── .env.example
├── .env                          ← gitignored, contains ANTHROPIC_API_KEY
├── README.md
│
├── datasets/                     ← READ-ONLY data layer (mounted into backend container)
│   ├── index.json                ← Category registry + file routing
│   ├── yarn_craft.json           ← Gelang Macramé, Miniatur Rajutan, Key Chain Rajut
│   ├── resin_craft.json          ← Key Chain Resin
│   ├── wood_craft.json           ← Figura Kayu
│   ├── packaging_gift.json       ← Kemasan Gift Box
│   └── textile_craft.json        ← Totebag Canvas (Custom Draw)
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── .env.local.example
│   │
│   └── src/
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx           ← Landing / Home
│       │   ├── plan/
│       │   │   ├── page.tsx       ← Main planning input form
│       │   │   └── result/
│       │   │       └── page.tsx   ← AI output display + save action
│       │   └── history/
│       │       └── page.tsx       ← Saved production plans list
│       │
│       ├── components/
│       │   ├── ui/                ← Primitive components: Button, Input, Card, Badge
│       │   ├── PlanForm.tsx       ← User input: 6 fields — product_name (fixed list), qty, budget_max, has_mandatory (bool), mandatory_material_name, allow_substitution (bool)
│       │   ├── InputSummary.tsx   ← Section A: echoes category, product, qty, budget
│       │   ├── BudgetStatusCard.tsx ← Section B: status badge + cost min/max comparison
│       │   ├── MaterialCardList.tsx ← Section C: horizontal scroll cards (name, grade, price)
│       │   ├── MaterialTable.tsx  ← Section D: detailed table (per unit, total, cost range)
│       │   ├── SubstitutionList.tsx ← Section E: substitution suggestions
│       │   ├── ProcurementAdvice.tsx ← Section F: platform names per material
│       │   └── HistoryList.tsx    ← List of saved production_plans
│       │
│       ├── lib/
│       │   └── api.ts             ← All fetch calls to backend. No direct AI calls from FE.
│       │
│       └── types/
│           └── index.ts           ← Shared TypeScript interfaces mirroring Pydantic schemas
│
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    ├── .env.example
    │
    ├── main.py                    ← FastAPI app instantiation + router registration
    │
    ├── api/
    │   ├── __init__.py
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   ├── classify.py        ← POST /classify
    │   │   ├── estimate.py        ← POST /estimate
    │   │   └── plans.py           ← POST /plans, GET /plans, GET /plans/{id}
    │   └── middleware/
    │       └── cors.py            ← CORS config allowing frontend origin
    │
    ├── services/
    │   ├── __init__.py
    │   ├── claude_service.py      ← All Anthropic API calls. No route logic here.
    │   ├── dataset_service.py     ← JSON loading, category filtering, keyword matching
    │   └── plan_service.py        ← SQLAlchemy CRUD for production_plans
    │
    ├── models/
    │   ├── __init__.py
    │   ├── request.py             ← Pydantic input schemas (ClassifyRequest, EstimateRequest)
    │   └── response.py            ← Pydantic output schemas (ClassifyResponse, EstimateResponse)
    │
    ├── db/
    │   ├── database.py            ← SQLAlchemy engine + session factory
    │   ├── models.py              ← ProductionPlan ORM table definition
    │   └── makerflow.db           ← Auto-generated on first run (gitignored)
    │
    └── prompts/
        ├── classify_prompt.py     ← f-string template for classification call
        └── estimate_prompt.py     ← f-string template for estimation call
```

---

## 4. Core Data Flow & Lightweight RAG

### 4.1 Overview

Each user planning request triggers **two sequential Claude API calls**. There is no vector database. This pipeline is referred to internally as "Lightweight RAG."

**Call 1 — LLM Classification (primary):** Claude classifies `product_name` → outputs `category_id` + `category_label`. The backend then loads the corresponding `.json` dataset file based on this output.

**Deterministic Fallback:** If Call 1 output does not match a known `category_id`, the backend falls back to `PRODUCT_CATEGORY_MAP` (hardcoded). This guarantees zero failure at MVP scale while keeping the architecture ready for free-text input at scale.

**Call 2 — LLM Estimation (primary inference):** Claude receives the filtered materials from the loaded `.json` dataset and produces the full estimation output.

This design is intentional and must be stated in the proposal as: *"MakerFlow uses LLM as the primary classifier with a deterministic fallback, guaranteeing reliability at MVP scale while architecting for free-text product input in future iterations."*

### 4.2 Finalized Input Schema (PlanForm → Backend)

The form has exactly **6 fields**. These are the only fields that exist. Do not add or remove fields without explicit instruction.

| # | Field Name | Type | Required | Notes |
|---|---|---|---|---|
| 1 | `product_name` | `string` (fixed enum) | Yes | User selects from fixed product list. Used for dataset category routing and displayed verbatim on output page. |
| 2 | `target_qty` | `integer` | Yes | Target production quantity in units |
| 3 | `available_budget` | `integer` (IDR) | Yes | Total modal yang dimiliki user (Total Available Budget). Used for both forward validation and reverse quantity calculation. |
| 4 | `has_mandatory_material` | `boolean` | Yes | Toggles visibility of fields 5 and 6. If `false`, fields 5–6 are null. |
| 5 | `mandatory_material_name` | `string \| null` | Conditional | Free-text name of the locked material. Only sent if field 4 is `true`. |
| 6 | `allow_substitution` | `boolean \| null` | Conditional | Whether non-mandatory materials may be substituted. Only sent if field 4 is `true`. |

**Fixed product name list** (drives category routing, no free text allowed). Single-category products map to a single-element array; cross-category products map to multiple category IDs loaded and merged simultaneously:

```
── Single-Category ──────────────────────────────────────────────────────────
"Gelang Macramé / Bracelet Custom"                      → ["yarn_craft"]
"Kerajinan Miniatur Rajutan"                            → ["yarn_craft"]
"Key Chain Rajut Custom Karakter"                       → ["yarn_craft"]
"Key Chain Resin"                                       → ["resin_craft"]
"Figura Kayu"                                           → ["wood_craft"]
"Kemasan Gift Box"                                      → ["packaging_gift"]
"Totebag Canvas (Custom Draw)"                          → ["textile_craft"]

── Cross-Category (Multi-Domain) ────────────────────────────────────────────
"Gantungan Kunci Resin Kayu Premium + Rumbai"           → ["resin_craft", "wood_craft", "yarn_craft", "packaging_gift"]
"Pouch Kanvas Resleting dengan Gantungan Resin"         → ["textile_craft", "resin_craft", "packaging_gift"]
"Paket Kado Figura Kayu & Boneka Rajut"                 → ["wood_craft", "yarn_craft", "packaging_gift"]
"Totebag Kanvas dengan Tali Makrame & Pegangan Resin"   → ["textile_craft", "yarn_craft", "resin_craft", "packaging_gift"]
```

**Pydantic Request Schema (`backend/models/request.py`):**

```python
class EstimateRequest(BaseModel):
    product_name: str                        # must match fixed product list
    target_qty: int = Field(gt=0)
    available_budget: int = Field(gt=0)
    has_mandatory_material: bool
    mandatory_material_name: str | None = None
    allow_substitution: bool | None = None

    @model_validator(mode="after")
    def validate_mandatory_fields(self):
        if self.has_mandatory_material:
            if not self.mandatory_material_name:
                raise ValueError("mandatory_material_name required when has_mandatory_material is true")
            if self.allow_substitution is None:
                raise ValueError("allow_substitution required when has_mandatory_material is true")
        return self
```

**TypeScript Interface (`frontend/src/types/index.ts`):**

```typescript
export interface EstimateRequest {
  product_name: string;
  target_qty: number;
  available_budget: number;
  has_mandatory_material: boolean;
  mandatory_material_name: string | null;
  allow_substitution: boolean | null;
}
```

### 4.3 Finalized Output Schema (Backend → ResultPage)

The output page renders all of the following sections. Every field listed here must be present in the `EstimateResponse` Pydantic model and the corresponding TypeScript interface.

**Section A — User Input Summary (echoed back, displayed at top of result page):**

```
Kategori    : {detected_category_label}   ← output dari deteksi AI (Call 1)
Produk      : {product_name}              ← fixed, echoed from input
Jumlah      : {target_qty} unit
Anggaran    : Rp {available_budget}
```

**Section B — Budget Status Card:**

```
Status               : "sufficient" | "insufficient"
Est. Min             : Rp {total_cost_min}
Est. Max             : Rp {total_cost_max}
Estimasi QTY Mampu   : {estimated_affordable_qty} unit (Hanya muncul jika status "insufficient")
```
Both min and max are displayed together in the same card for direct comparison. `estimated_affordable_qty` is rendered only when `budget_status` is `"insufficient"`; the field is hidden entirely when status is `"sufficient"`.

**Section C — Material Breakdown (horizontal card list, one card per material):**

Each card contains:
- `name` — material name
- `grade` — recommended grade (string, e.g. "standard", "premium", "8oz")
- `price_display` — formatted price range, e.g. "Rp 500 – Rp 1.200 / meter"

**Section D — Detailed Material Table (one row per material):**

| Column | Field | Description |
|---|---|---|
| Nama Bahan | `name` | Material name |
| Per Unit | `qty_per_unit` + `unit` | e.g. "1.5 meter" |
| Total Unit | `qty_total` + `unit` | e.g. "150 meter" for qty=100 |
| Estimasi Harga | `cost_min` – `cost_max` | Per-material cost range in IDR |

**Section E — Rekomendasi & Substitusi:**

- Shown only when `allow_substitution: true` AND budget status is `insufficient`, OR as general recommendations
- Each substitution entry: original material name → suggested alternative name + reason

**Section F — Saran Pembelian (Procurement Advice):**

- Sourced from `supplier_platforms` field in dataset
- Rendered as platform name list per material (e.g. "Tokopedia, toko craft lokal")
- No direct URLs — platform names only

**Pydantic Response Schema (`backend/models/response.py`):**

```python
class MaterialItem(BaseModel):
    id: str
    name: str
    grade: str
    unit: str
    qty_per_unit: float
    qty_total: float
    cost_min: int
    cost_max: int
    supplier_platforms: list[str]

class SubstitutionSuggestion(BaseModel):
    original_id: str
    original_name: str
    substitute_id: str
    substitute_name: str
    reason: str

class EstimateResponse(BaseModel):
    detected_category_label: str
    product_name: str
    target_qty: int
    available_budget: int
    budget_status: Literal["sufficient", "insufficient"]
    total_cost_min: int
    total_cost_max: int
    estimated_affordable_qty: int | None = None  # Populated only if budget_status is "insufficient"
    materials_needed: list[MaterialItem]
    substitution_suggestions: list[SubstitutionSuggestion]
    procurement_advice: str
    notes: str
```

### 4.4 Step-by-Step Request Flow

```
[1] User fills PlanForm.tsx (6 fields as defined in 4.2)
    Submits → api.ts calls POST /estimate

─────────────────────────────────────────────
CALL 1 — LLM Classification
─────────────────────────────────────────────
[2] Backend: POST /estimate — Step A: LLM Classifies Product
    Handler: api/routes/estimate.py
    claude_service.py → Call 1 to Claude API

    Prompt (classify_prompt.py):
    ┌─────────────────────────────────────────────────────────────────┐
    │ You are a product category classifier for a craft production     │
    │ planning system. A product may belong to MULTIPLE categories     │
    │ simultaneously if it combines materials from different domains.  │
    │                                                                  │
    │ AVAILABLE CATEGORIES:                                            │
    │ - yarn_craft     : Kerajinan Benang & Tali                       │
    │ - resin_craft    : Kerajinan Resin                               │
    │ - wood_craft     : Kerajinan Kayu                                │
    │ - packaging_gift : Kemasan & Gift Box                            │
    │ - textile_craft  : Kerajinan Tekstil & Kain                      │
    │                                                                  │
    │ PRODUCT: "{product_name}"                                        │
    │                                                                  │
    │ Reply ONLY in this exact JSON, no markdown fences:              │
    │ {                                                                │
    │   "category_ids": ["string"],                                    │
    │   "category_labels": ["string"]                                  │
    │ }                                                                │
    │                                                                  │
    │ RULES:                                                           │
    │ - category_ids MUST be an array, even for single-category items  │
    │ - Only use IDs from the AVAILABLE CATEGORIES list above          │
    │ - Order arrays so primary/dominant category is first             │
    └─────────────────────────────────────────────────────────────────┘

    Returns: { category_ids: list[str], category_labels: list[str] }

    > *Note: Gemini models often hallucinate keys like `primary_category` or return a string instead of an array. The prompt MUST strictly enforce `category_ids` and `category_labels` as arrays. See Section 5.5 for mandatory parsing pattern.*

[3] Backend: Step B — Validate + Fallback
    dataset_service.py validates category_ids list from Call 1:
    - If ALL category_ids in the returned list match known KNOWN_CATEGORY_IDS → use the list
    - If ANY category_id is unknown / hallucinated, or if result is not a list → fallback to
      PRODUCT_CATEGORY_MAP[product_name] (which always returns a list[str])

    PRODUCT_CATEGORY_MAP (fallback only — see Section 4.5 for full map):
    {
      "Gelang Macramé / Bracelet Custom"                   : ["yarn_craft"],
      "Key Chain Resin"                                    : ["resin_craft"],
      "Gantungan Kunci Resin Kayu Premium + Rumbai"        : ["resin_craft", "wood_craft", "yarn_craft", "packaging_gift"],
      "Pouch Kanvas Resleting dengan Gantungan Resin"      : ["textile_craft", "resin_craft", "packaging_gift"],
      ... (see Section 4.5 for complete map)
    }

─────────────────────────────────────────────
DATASET RETRIEVAL — Backend loads .json files
─────────────────────────────────────────────
[4] Backend: Step C — Load & Filter Dataset (Multi-Category)
    dataset_service.py:
    → Receives validated list[str] of category_ids (1 or more)
    → For EACH category_id: reads index.json → resolves file path → loads .json
    → Merges all materials arrays from all loaded files into one master list
    → Applies keyword/tag filtering against product_name tokens across master list
    → If has_mandatory_material=true: force-includes material matching
      mandatory_material_name by fuzzy name match across merged master list
    → Fallback: if filter returns 0 results, pass full merged master list
    → Hard cap: max 45 items forwarded to Claude Call 2 (increased from 30
      to safely accommodate multi-category merges while maintaining context
      window hygiene)

─────────────────────────────────────────────
CALL 2 — LLM Estimation
─────────────────────────────────────────────
[5] Backend: Step D — LLM Estimates from Loaded Dataset
    claude_service.py → Call 2 to Claude API

    Prompt (estimate_prompt.py):
    ┌────────────────────────────────────────────────────────────────────┐
    │ You are a production planning assistant for Indonesian SMEs.       │
    │ All output must be in Bahasa Indonesia.                            │
    │                                                                    │
    │ AVAILABLE RAW MATERIALS DATA:                                      │
    │ {filtered_materials_json}           ← injected from Step C        │
    │                                                                    │
    │ USER INPUT:                                                        │
    │ - Produk            : {product_name}                               │
    │ - Target Qty        : {target_qty} unit                            │
    │ - Available Budget  : Rp {available_budget}                        │
    │ - Bahan Wajib       : {mandatory_material_name or "Tidak ada"}     │
    │ - Boleh Substitusi  : {allow_substitution}                         │
    │                                                                    │
    │ TASKS:                                                             │
    │ 1. Estimate qty_per_unit and qty_total for each required material  │
    │ 2. Calculate cost_min and cost_max per material from price_range   │
    │ 3. Sum total_cost_min and total_cost_max across all materials      │
    │ 4. Set budget_status = "sufficient" if total_cost_max <=           │
    │    available_budget, otherwise "insufficient"                      │
    │ 5. If allow_substitution=true AND budget insufficient:             │
    │    suggest cheaper alternatives from AVAILABLE DATA only           │
    │ 6. Write procurement_advice from supplier_platforms in the data    │
    │ 7. If budget_status is "insufficient", perform REVERSE             │
    │    CALCULATION: Calculate the estimated HPP (Harga Pokok          │
    │    Produksi) per 1 unit. Divide the {available_budget} by the     │
    │    HPP per unit. FLOOR the result to the nearest whole integer.   │
    │    Populate the "estimated_affordable_qty" field with this number. │
    │                                                                    │
    │ CONSTRAINTS (STRICT GROUNDED RAG - CRITICAL):                      │
    │ 1. HANYA gunakan material yang tersedia di AVAILABLE RAW MATERIALS │
    │    DATA.                                                            │
    │ 2. DILARANG KERAS menambah, mengarang, atau menebak material,      │
    │    harga, atau platform di luar data yang disediakan.              │
    │ 3. Jika material yang dibutuhkan user tidak ada di data, abaikan   │
    │    material tersebut dan tulis penjelasan di field "notes"         │
    │    (contoh: "Kain parasut tidak tersedia di database kami,         │
    │    estimasi biaya hanya mencakup bahan yang tersedia.").           │
    │ 4. mandatory_material_name wajib ada di output, jangan            │
    │    disubstitusi.                                                    │
    │ 5. grade: pick the single most appropriate grade string per item.  │
    │ 6. For reverse calculation (Task 7), use the average of cost_min  │
    │    and cost_max to estimate HPP per unit. Always floor the final  │
    │    quantity to an integer.                                         │
    │                                                                    │
    │ Reply ONLY in this exact JSON, no markdown fences:                 │
    │ {                                                                  │
    │   "budget_status": "sufficient|insufficient",                      │
    │   "total_cost_min": int,                                           │
    │   "total_cost_max": int,                                           │
    │   "estimated_affordable_qty": int or null,                         │
    │   "materials_needed": [                                            │
    │     {                                                              │
    │       "id": "string",                                              │
    │       "name": "string",                                            │
    │       "grade": "string",                                           │
    │       "unit": "string",                                            │
    │       "qty_per_unit": float,                                       │
    │       "qty_total": float,                                          │
    │       "cost_min": int,                                             │
    │       "cost_max": int,                                             │
    │       "supplier_platforms": ["string"]                             │
    │     }                                                              │
    │   ],                                                               │
    │   "substitution_suggestions": [                                    │
    │     {                                                              │
    │       "original_id": "string",                                     │
    │       "original_name": "string",                                   │
    │       "substitute_id": "string",                                   │
    │       "substitute_name": "string",                                 │
    │       "reason": "string"                                           │
    │     }                                                              │
    │   ],                                                               │
    │   "procurement_advice": "string",                                  │
    │   "notes": "string"                                                │
    │ }                                                                  │
    └────────────────────────────────────────────────────────────────────┘

─────────────────────────────────────────────
RESPONSE ASSEMBLY & RENDER
─────────────────────────────────────────────
[6] Backend assembles final EstimateResponse:
    Merges: category_label (Call 1) + estimation fields (Call 2)
    + echoes: product_name, target_qty, available_budget from original request
    Validates entire object through Pydantic EstimateResponse model
    Returns to frontend

[7] Frontend result/page.tsx renders in this exact section order:
    A. Input Summary     → Kategori (label from Call 1), Produk, Jumlah, Anggaran
    B. Budget Status     → "sufficient"/"insufficient" badge + Est. Min vs Est. Max
    C. Material Cards    → horizontal scroll, one card per material
                           (name, grade, price range "Rp X – Rp Y / unit")
    D. Material Table    → per unit qty, total qty, material name, cost range per item
    E. Substitusi        → shown only when substitution_suggestions is non-empty
    F. Procurement       → platform names per material from supplier_platforms
    G. "Simpan Rencana"  → POST /plans

[8] Backend: POST /plans (user-triggered save)
    Persists full EstimateResponse JSON + EstimateRequest to SQLite
    Returns: { plan_id: int, created_at: string }
```

### 4.5 Dataset Filter Logic (dataset_service.py)

Category routing uses **LLM as primary, deterministic map as fallback**. The `.json` dataset file is only loaded *after* a valid `category_id` is resolved. Claude never touches the raw dataset file directly — the backend loads it and injects filtered contents into the Call 2 prompt.

```python
# Implement exactly in services/dataset_service.py

# Fallback map — values are now lists to support cross-category products
PRODUCT_CATEGORY_MAP: dict[str, list[str]] = {
    "Gelang Macramé / Bracelet Custom": ["yarn_craft"],
    "Kerajinan Miniatur Rajutan": ["yarn_craft"],
    "Key Chain Rajut Custom Karakter": ["yarn_craft"],
    "Key Chain Resin": ["resin_craft"],
    "Figura Kayu": ["wood_craft"],
    "Kemasan Gift Box": ["packaging_gift"],
    "Totebag Canvas (Custom Draw)": ["textile_craft"],
    "Gantungan Kunci Resin Kayu Premium + Rumbai": ["resin_craft", "wood_craft", "yarn_craft", "packaging_gift"],
    "Pouch Kanvas Resleting dengan Gantungan Resin": ["textile_craft", "resin_craft", "packaging_gift"],
    "Paket Kado Figura Kayu & Boneka Rajut": ["wood_craft", "yarn_craft", "packaging_gift"],
    "Totebag Kanvas dengan Tali Makrame & Pegangan Resin": ["textile_craft", "yarn_craft", "resin_craft", "packaging_gift"],
}

KNOWN_CATEGORY_IDS = {cid for ids in PRODUCT_CATEGORY_MAP.values() for cid in ids}


def resolve_category(llm_category_ids: list[str], product_name: str) -> list[str]:
    """Validates LLM Call 1 output against known category IDs. Falls back to hardcoded map if invalid."""
    if isinstance(llm_category_ids, list) and all(cid in KNOWN_CATEGORY_IDS for cid in llm_category_ids):
        return llm_category_ids  # LLM primary path
    return PRODUCT_CATEGORY_MAP.get(product_name, ["yarn_craft"])  # deterministic fallback


def load_and_filter_materials(
    category_ids: list[str],
    product_name: str,
    mandatory_material_name: str | None,
) -> list[dict]:
    """Loads multiple .json datasets, merges them, and filters down to relevant materials."""
    index = load_json("datasets/index.json")

    # 1. Gather and merge materials from ALL relevant categories
    merged_materials = []
    for cat_id in category_ids:
        category_entry = next(c for c in index["categories"] if c["id"] == cat_id)
        cat_data = load_json(f"datasets/{category_entry['file']}")
        merged_materials.extend(cat_data["materials"])

    # 2. Filter logic
    keywords = product_name.lower().replace("/", " ").split()
    filtered = []

    for m in merged_materials:
        if mandatory_material_name and mandatory_material_name.lower() in m["name"].lower():
            filtered.append(m)
            continue
        if any(kw in [t.lower() for t in m["tags"]] for kw in keywords):
            filtered.append(m)

    # Safety fallback: if aggressive filter returns nothing, use all merged
    if not filtered:
        filtered = merged_materials

    # 3. Hard cap for context window hygiene (increased to 45 for multi-category)
    return filtered[:45]
```

### 4.6 Dataset Structure Contract

Each dataset JSON file must conform to this schema. Deviations will break `dataset_service.py`.

```json
{
  "category_id": "string",
  "category_label": "string",
  "description": "string",
  "unit_note": "string",
  "materials": [
    {
      "id": "string (e.g. YC001)",
      "name": "string",
      "unit": "string (meter|gram|pcs|lembar|pasang|gulung|roll|batang|ml)",
      "price_range": {
        "min": "number (IDR)",
        "max": "number (IDR)",
        "currency": "IDR"
      },
      "grade": ["string"],
      "common_use": ["string"],
      "substitutes": ["string (other material IDs)"],
      "supplier_platforms": ["string"],
      "tags": ["string"]
    }
  ]
}
```

### 4.7 Active Demo Scenarios

These 11 scenarios constitute the full demo dataset for the preliminary submission. The 4 cross-category products demonstrate advanced multi-domain AI reasoning and are a key differentiator in the competition narrative.

| Product | Dataset File(s) | Excluded from Dataset |
|---|---|---|
| Gelang Macramé / Bracelet Custom | `yarn_craft.json` | Warna benang |
| Kerajinan Miniatur Rajutan | `yarn_craft.json` | Warna benang |
| Key Chain Rajut Custom Karakter | `yarn_craft.json` | Warna benang |
| Key Chain Resin | `resin_craft.json` | Pewarna / pigmen resin |
| Figura Kayu | `wood_craft.json` | Cat / warna kayu |
| Kemasan Gift Box | `packaging_gift.json` | — |
| Totebag Canvas (Custom Draw) | `textile_craft.json` | Cat air / pewarna kain |
| **Gantungan Kunci Resin Kayu Premium + Rumbai** | `resin_craft.json`, `wood_craft.json`, `yarn_craft.json`, `packaging_gift.json` | Pewarna resin, cat kayu, warna benang |
| **Pouch Kanvas Resleting dengan Gantungan Resin** | `textile_craft.json`, `resin_craft.json`, `packaging_gift.json` | Pewarna kain, pewarna resin |
| **Paket Kado Figura Kayu & Boneka Rajut** | `wood_craft.json`, `yarn_craft.json`, `packaging_gift.json` | Cat kayu, warna benang |
| **Totebag Kanvas dengan Tali Makrame & Pegangan Resin** | `textile_craft.json`, `yarn_craft.json`, `resin_craft.json`, `packaging_gift.json` | Pewarna kain, warna benang, pewarna resin |

**Color/aesthetic materials are explicitly excluded from all datasets.** The platform provides structural raw material planning only. This is a deliberate product decision, not a data gap, and must be stated as such in the proposal.

---

## 5. Development Methodology

### 5.1 API-First, UI-Driven Development

**Contract definition comes before implementation.** The sequence for any new feature:

1. Define Pydantic schemas in `backend/models/request.py` and `backend/models/response.py`
2. Mirror schemas as TypeScript interfaces in `frontend/src/types/index.ts`
3. Implement backend route and service
4. Implement frontend component consuming the typed response

**Pydantic is the single source of truth for data contracts.** Every request and response is validated by Pydantic before business logic runs. Frontend TypeScript interfaces must match Pydantic schemas exactly.

### 5.2 Service Layer Isolation

**Routes must not contain business logic.** Routes handle HTTP concerns only (parsing, validation, response codes). All logic lives in services.

| File | Responsibility | Must NOT contain |
|---|---|---|
| `api/routes/*.py` | Parse request, call service, return response | Business logic, DB access, AI calls |
| `services/claude_service.py` | All Anthropic API calls | Route logic, DB access |
| `services/dataset_service.py` | JSON loading and filtering | AI calls, route logic |
| `services/plan_service.py` | SQLAlchemy CRUD | AI calls, dataset access |

### 5.3 Commit Convention

**All commits must follow Conventional Commits.** This is a hard requirement from AIC rulebook and will be evaluated by judges reviewing commit history.

```
feat: add LLM classification call with deterministic fallback in dataset_service
feat: implement POST /estimate with two-call Claude pipeline
fix: correct price_range key mismatch in dataset_service filter logic
refactor: extract classify_prompt and estimate_prompt to dedicated prompts/ module
```

Non-conventional commits will be considered non-compliant with AIC development standards.

### 5.4 Environment Variables

Two secrets exist, one per provider tier. Both are defined in `.env` at the monorepo root and injected into the backend container via `docker-compose.yml`. **The frontend has no access to either key and makes no direct calls to any LLM API.**

```
# .env (root, gitignored)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx  # For Release/Production
GOOGLE_API_KEY=AIzaSy-xxxxxxxxxxxxxxxx     # For Dev/MVP (Hybrid Strategy)
```

### 5.5 Error Handling & JSON Parsing Standards (CRITICAL FOR GEMINI)

All LLM API calls must be wrapped in try/except. JSON parsing from LLM responses **must use Regex** to strip markdown fences, as simple string replacement often fails with Gemini's output format.

**Known Gemini Dev Bugs & Solutions:**

1. **Schema Hallucination:** Gemini may return `primary_category` + `keywords` instead of the spec's `category_id` + `category_label`.
   - *Solution:* Update Call 1 prompt to strictly enforce the exact JSON keys. Implement a fallback mapping in `dataset_service.py` if keys mismatch.

2. **Markdown Fences:** Gemini models frequently wrap JSON in markdown (e.g., ` ```json ... ``` `).
   - *Solution:* Use Regex to strip these fences before `json.loads`.

**Mandatory Parsing Pattern (`llm_service.py` / `claude_service.py`):**

```python
import re
import json

def parse_llm_json_response(raw_text: str) -> dict:
    # Use Regex to strip markdown fences (handles ```json ... ``` or ``` ... ```)
    clean_text = re.sub(r'^```[a-zA-Z]*\n?', '', raw_text.strip())
    clean_text = re.sub(r'\n?```$', '', clean_text.strip())
    return json.loads(clean_text)
```

**Exception Handling (all LLM calls):**

```python
try:
    response = client.messages.create(...)  # or model.generate_content(...)
    raw = response.content[0].text          # or response.text for Gemini
    return parse_llm_json_response(raw)
except (Exception, json.JSONDecodeError) as e:
    raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")
```

### 5.6 Docker Compose Run Contract

The application must be fully operational with these exact three commands:

```bash
cp .env.example .env          # then add ANTHROPIC_API_KEY value
docker compose up --build
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API docs: http://localhost:8000/docs
```

Any deviation from this run contract fails the AIC reproducibility requirement.

### 5.7 README.md Requirements (AIC Mandatory)

README must contain at minimum:

- Project description (1 paragraph)
- Prerequisites (Docker, Docker Compose)
- Setup steps (exact commands above)
- Architecture overview (can reference Section 3 of this document)
- Dataset description and scope statement
- API endpoint table (method, path, description)

---

## Appendix A: API Endpoint Reference

| Method | Path | Description | Request Body | Response |
|---|---|---|---|---|
| `POST` | `/estimate` | Full planning pipeline: LLM classify → load dataset JSON → LLM estimate | `EstimateRequest` | `EstimateResponse` (includes `estimated_affordable_qty` if budget is insufficient) |
| `POST` | `/plans` | Save a completed production plan | `SavePlanRequest` | `{ plan_id: int, created_at: string }` |
| `GET` | `/plans` | List all saved plans (history page) | — | `list[PlanSummary]` |
| `GET` | `/plans/{id}` | Get full detail of a single saved plan | — | `PlanDetail` |

**Note:** There is no separate `/classify` endpoint. Both Claude calls are orchestrated inside `POST /estimate`. Call 1 classifies the product and its output drives which `.json` dataset file is loaded. Call 2 receives the filtered dataset contents and produces the estimation. The frontend makes a single call to `/estimate` and receives the complete `EstimateResponse`.

---

## Appendix B: Dataset File Registry

Files marked with ✦ are shared across multiple cross-category products and are loaded in combination during multi-category dataset retrieval.

| File | Category ID | Products Covered | Item Count |
|---|---|---|---|
| `yarn_craft.json` ✦ | `yarn_craft` | Macramé, Rajutan, Key Chain Rajut; + Gantungan Kunci Resin Kayu, Paket Kado Figura & Rajut, Totebag Makrame & Resin | 10 |
| `resin_craft.json` ✦ | `resin_craft` | Key Chain Resin; + Gantungan Kunci Resin Kayu, Pouch Kanvas & Resin, Totebag Makrame & Resin | 6 |
| `wood_craft.json` ✦ | `wood_craft` | Figura Kayu; + Gantungan Kunci Resin Kayu, Paket Kado Figura & Rajut | 7 |
| `packaging_gift.json` ✦ | `packaging_gift` | Kemasan Gift Box; + Gantungan Kunci Resin Kayu, Pouch Kanvas & Resin, Paket Kado Figura & Rajut, Totebag Makrame & Resin | 8 |
| `textile_craft.json` ✦ | `textile_craft` | Totebag Canvas; + Pouch Kanvas & Resin, Totebag Makrame & Resin | 7 |
| **New cross-category items** | | Items added to support multi-domain products | **+15** |
| **Total** | | | **~53 items** |

---

*Document version 1.5.0 — updated August 2026. Reverse Calculation (Estimasi QTY) feature added. Section 1.1: 4th pain point added. Section 4.2: `budget_max` renamed to `available_budget` across table, Pydantic schema, and TypeScript interface to reflect "total modal" semantics. Section 4.3: `estimated_affordable_qty: int | None` added to `EstimateResponse` Pydantic model; Section B Budget Status Card updated with conditional display rule. Section 4.4 Call 2 prompt: USER INPUT updated to `available_budget`; Task 7 (Reverse Calculation via HPP per unit floor division) added; Constraint 6 (use avg of cost_min/cost_max, always floor) added; `estimated_affordable_qty` added to JSON schema. Appendix A: POST /estimate response column annotated. No changes to tech stack, folder structure, Call 1 logic, dataset filter, or Strict Grounded RAG constraints. Scope locked for AIC COMPFEST 18 Preliminary Round submission (deadline: August 25, 2026, 23:55 WIB).*