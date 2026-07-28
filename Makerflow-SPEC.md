# MakerFlow — Master Project Context & Technical Specification
**Version:** 1.2.0 | **Competition:** AIC COMPFEST 18 | **Theme:** Smart Manufacturing — AI for the Backbone of the Economy

> This document is the single source of truth for the MakerFlow MVP. It functions as a `.cursorrules` / system prompt for any AI coding agent entering this codebase. Every architectural decision, constraint, and convention documented here has been finalized. Do not deviate without explicit instruction.

---

## 1. Project Overview & MVP Scope

### 1.1 Product Summary

**MakerFlow** is an AI-powered production planning assistant for Indonesian creative-sector SMEs (UMKM) and mid-scale manufacturers. It solves three simultaneous pain points that currently rely on manual guesswork:

1. **Raw material estimation** — how much of each material is needed for a target production quantity
2. **Cost optimization** — whether the available budget is sufficient, and where savings are possible
3. **Substitution advisory** — recommending alternative materials when budget is insufficient, respecting any materials the user has locked as non-substitutable

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

> *"At MVP stage, MakerFlow uses a manually curated dataset of ~46 raw materials across 5 product categories, sufficient to support 7 representative demo scenarios. The development roadmap includes real-time data integration via e-commerce scraping (Tokopedia, Indotrading) and expansion to additional product categories in subsequent iterations."*

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
| Provider | Anthropic | Claude API |
| Model | `claude-sonnet-4-6` | Fixed. Do not substitute |
| SDK | `anthropic` Python SDK | 0.25.0 |
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
| Environment secrets | `.env` at monorepo root | `ANTHROPIC_API_KEY` only |

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
| 3 | `budget_max` | `integer` (IDR) | Yes | Maximum budget ceiling in Rupiah |
| 4 | `has_mandatory_material` | `boolean` | Yes | Toggles visibility of fields 5 and 6. If `false`, fields 5–6 are null. |
| 5 | `mandatory_material_name` | `string \| null` | Conditional | Free-text name of the locked material. Only sent if field 4 is `true`. |
| 6 | `allow_substitution` | `boolean \| null` | Conditional | Whether non-mandatory materials may be substituted. Only sent if field 4 is `true`. |

**Fixed product name list** (drives category routing, no free text allowed):

```
"Gelang Macramé / Bracelet Custom"   → yarn_craft
"Kerajinan Miniatur Rajutan"          → yarn_craft
"Key Chain Rajut Custom Karakter"     → yarn_craft
"Key Chain Resin"                     → resin_craft
"Figura Kayu"                         → wood_craft
"Kemasan Gift Box"                    → packaging_gift
"Totebag Canvas (Custom Draw)"        → textile_craft
```

**Pydantic Request Schema (`backend/models/request.py`):**

```python
class EstimateRequest(BaseModel):
    product_name: str                        # must match fixed product list
    target_qty: int = Field(gt=0)
    budget_max: int = Field(gt=0)
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
  budget_max: number;
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
Anggaran    : Rp {budget_max}
```

**Section B — Budget Status Card:**

```
Status      : "sufficient" | "insufficient"
Est. Min    : Rp {total_cost_min}
Est. Max    : Rp {total_cost_max}
```
Both min and max are displayed together in the same card for direct comparison.

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
    budget_max: int
    budget_status: Literal["sufficient", "insufficient"]
    total_cost_min: int
    total_cost_max: int
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
    │ planning system.                                                 │
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
    │   "category_id": "string",                                       │
    │   "category_label": "string"                                     │
    │ }                                                                │
    └─────────────────────────────────────────────────────────────────┘

    Returns: { category_id: str, category_label: str }

[3] Backend: Step B — Validate + Fallback
    dataset_service.py validates category_id from Call 1:
    - If category_id matches a known key in PRODUCT_CATEGORY_MAP → use it
    - If category_id is unknown / hallucinated → fallback to PRODUCT_CATEGORY_MAP[product_name]

    PRODUCT_CATEGORY_MAP (fallback only):
    {
      "Gelang Macramé / Bracelet Custom"  : "yarn_craft",
      "Kerajinan Miniatur Rajutan"         : "yarn_craft",
      "Key Chain Rajut Custom Karakter"    : "yarn_craft",
      "Key Chain Resin"                    : "resin_craft",
      "Figura Kayu"                        : "wood_craft",
      "Kemasan Gift Box"                   : "packaging_gift",
      "Totebag Canvas (Custom Draw)"       : "textile_craft",
    }

─────────────────────────────────────────────
DATASET RETRIEVAL — Backend loads .json
─────────────────────────────────────────────
[4] Backend: Step C — Load & Filter Dataset
    dataset_service.py:
    → Reads index.json → resolves file path for validated category_id
    → Loads {category_id}.json (e.g. yarn_craft.json)
    → Filters materials by keyword/tag match against product_name tokens
    → If has_mandatory_material=true: force-includes material matching
      mandatory_material_name by fuzzy name match (user typed free text,
      no ID available)
    → Fallback: if filter returns 0 results, pass all materials in category
    → Hard cap: max 30 items forwarded to Claude Call 2

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
    │ - Produk           : {product_name}                                │
    │ - Target Qty       : {target_qty} unit                             │
    │ - Budget Max       : Rp {budget_max}                               │
    │ - Bahan Wajib      : {mandatory_material_name or "Tidak ada"}      │
    │ - Boleh Substitusi : {allow_substitution}                          │
    │                                                                    │
    │ TASKS:                                                             │
    │ 1. Estimate qty_per_unit and qty_total for each required material  │
    │ 2. Calculate cost_min and cost_max per material from price_range   │
    │ 3. Sum total_cost_min and total_cost_max across all materials      │
    │ 4. Set budget_status = "sufficient" if total_cost_max <= budget,   │
    │    otherwise "insufficient"                                        │
    │ 5. If allow_substitution=true AND budget insufficient:             │
    │    suggest cheaper alternatives from AVAILABLE DATA only           │
    │ 6. Write procurement_advice from supplier_platforms in the data    │
    │                                                                    │
    │ CONSTRAINTS:                                                       │
    │ - Only use materials present in AVAILABLE RAW MATERIALS DATA       │
    │ - Never invent materials, prices, or platforms outside the data    │
    │ - mandatory_material_name must appear in output, never substituted │
    │ - grade: pick the single most appropriate grade string per item    │
    │                                                                    │
    │ Reply ONLY in this exact JSON, no markdown fences:                 │
    │ {                                                                  │
    │   "budget_status": "sufficient|insufficient",                      │
    │   "total_cost_min": int,                                           │
    │   "total_cost_max": int,                                           │
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
    + echoes: product_name, target_qty, budget_max from original request
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

# Fallback map — only used when Call 1 output fails validation
PRODUCT_CATEGORY_MAP: dict[str, str] = {
    "Gelang Macramé / Bracelet Custom": "yarn_craft",
    "Kerajinan Miniatur Rajutan":        "yarn_craft",
    "Key Chain Rajut Custom Karakter":   "yarn_craft",
    "Key Chain Resin":                   "resin_craft",
    "Figura Kayu":                       "wood_craft",
    "Kemasan Gift Box":                  "packaging_gift",
    "Totebag Canvas (Custom Draw)":      "textile_craft",
}

KNOWN_CATEGORY_IDS = set(PRODUCT_CATEGORY_MAP.values())


def resolve_category(llm_category_id: str, product_name: str) -> str:
    """
    Validates LLM Call 1 output against known category IDs.
    Falls back to hardcoded map if LLM output is invalid.
    """
    if llm_category_id in KNOWN_CATEGORY_IDS:
        return llm_category_id  # LLM primary path
    return PRODUCT_CATEGORY_MAP[product_name]  # deterministic fallback


def load_and_filter_materials(
    category_id: str,
    product_name: str,
    mandatory_material_name: str | None,
) -> list[dict]:
    """
    Loads the correct .json dataset for category_id,
    then filters down to materials relevant to the product.
    Returns max 30 items for injection into Call 2 prompt.
    """
    index = load_json("datasets/index.json")
    category_entry = next(
        c for c in index["categories"] if c["id"] == category_id
    )
    all_materials = load_json(f"datasets/{category_entry['file']}")["materials"]

    keywords = product_name.lower().replace("/", " ").split()

    filtered = []
    for m in all_materials:
        # Force-include mandatory material by fuzzy name match
        if mandatory_material_name:
            if mandatory_material_name.lower() in m["name"].lower():
                filtered.append(m)
                continue
        # Include if any keyword matches a material tag
        if any(kw in [t.lower() for t in m["tags"]] for kw in keywords):
            filtered.append(m)

    # Safety fallback: if aggressive filter returns nothing, use all
    if not filtered:
        filtered = all_materials

    return filtered[:30]  # hard cap for context window hygiene
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

These 7 scenarios constitute the full demo dataset for the preliminary submission:

| Product | Dataset File | Excluded from Dataset |
|---|---|---|
| Gelang Macramé / Bracelet Custom | `yarn_craft.json` | Warna benang |
| Kerajinan Miniatur Rajutan | `yarn_craft.json` | Warna benang |
| Key Chain Rajut Custom Karakter | `yarn_craft.json` | Warna benang |
| Key Chain Resin | `resin_craft.json` | Pewarna / pigmen resin |
| Figura Kayu | `wood_craft.json` | Cat / warna kayu |
| Kemasan Gift Box | `packaging_gift.json` | — |
| Totebag Canvas (Custom Draw) | `textile_craft.json` | Cat air / pewarna kain |

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

Only one secret exists: `ANTHROPIC_API_KEY`. It is defined in `.env` at the monorepo root and injected into the backend container via `docker-compose.yml`. **The frontend has no access to this key and makes no direct calls to the Anthropic API.**

```
# .env (root, gitignored)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

### 5.5 Error Handling Standards

All Claude API calls must be wrapped in try/except. JSON parsing from Claude responses must strip markdown fences before parsing.

```python
# Pattern for all claude_service.py calls
try:
    response = client.messages.create(...)
    raw = response.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)
except (anthropic.APIError, json.JSONDecodeError) as e:
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
| `POST` | `/estimate` | Full planning pipeline: LLM classify → load dataset JSON → LLM estimate | `EstimateRequest` | `EstimateResponse` |
| `POST` | `/plans` | Save a completed production plan | `SavePlanRequest` | `{ plan_id: int, created_at: string }` |
| `GET` | `/plans` | List all saved plans (history page) | — | `list[PlanSummary]` |
| `GET` | `/plans/{id}` | Get full detail of a single saved plan | — | `PlanDetail` |

**Note:** There is no separate `/classify` endpoint. Both Claude calls are orchestrated inside `POST /estimate`. Call 1 classifies the product and its output drives which `.json` dataset file is loaded. Call 2 receives the filtered dataset contents and produces the estimation. The frontend makes a single call to `/estimate` and receives the complete `EstimateResponse`.

---

## Appendix B: Dataset File Registry

| File | Category ID | Products Covered | Item Count |
|---|---|---|---|
| `yarn_craft.json` | `yarn_craft` | Macramé, Rajutan, Key Chain Rajut | 10 |
| `resin_craft.json` | `resin_craft` | Key Chain Resin | 6 |
| `wood_craft.json` | `wood_craft` | Figura Kayu | 7 |
| `packaging_gift.json` | `packaging_gift` | Kemasan Gift Box | 8 |
| `textile_craft.json` | `textile_craft` | Totebag Canvas | 7 |
| **Total** | | | **~46 items** |

---

*Document version 1.2.0 — updated July 2026. Category routing corrected: LLM Call 1 is now primary classifier; deterministic PRODUCT_CATEGORY_MAP is fallback only. Dataset .json is loaded by backend after Call 1 resolves category_id, then injected into Call 2 prompt. Architecture ready to scale to free-text product input without structural changes. Scope locked for AIC COMPFEST 18 Preliminary Round submission (deadline: August 25, 2026, 23:55 WIB).*