# CURRENT STATE OF MAKERFLOW MVP

## 1. Architecture & Stack Summary
- **Frontend:** Next.js (version 16.2.11 with React 19.x), built with TypeScript and Tailwind CSS v4.
- **Backend:** FastAPI, Python, utilizing `pydantic` for data validation, and `google.generativeai` for the Gemini integration. (SQLite ORM dependencies like SQLAlchemy are intended but not yet fully wired).
- **AI Integration:** Google Gemini API (`gemini-3.5-flash`) orchestrated within `gemini_service.py` (explicitly overriding the Claude requirement from the spec).

## 2. Backend Status (FastAPI)
- **Active Endpoints:** 
  - `POST /estimate` is the only active functional route (located in `api/routes/estimate.py`).
  - `api/routes/plans.py` exists but is completely empty.
- **Pydantic Schema Variable Names (`backend/models/request.py`):**
  - **`EstimateRequest`**: `product_description`, `target_qty`, `max_budget`, `mandatory_materials` (List), `category_id`, `keywords`. (This is a significant deviation from the spec).
  - **`SavePlanRequest`**: `product_name`, `target_qty`, `max_budget`, `category`, `result_json`.
  - **`ClassifyRequest`**: `product_description`.
- **Pydantic Schema Variable Names (`backend/models/response.py`):**
  - **`EstimateResponse`**: `materials_needed` (List of `MaterialEstimate`), `total_cost_min`, `total_cost_max`, `budget_status`, `substitution_suggestions`, `notes`.
  - **`ClassifyResponse`**: `primary_category`, `keywords`.
- **Gemini Service (`gemini_service.py`):** 
  - Working and orchestrates the two-step AI flow (`classify_product` and `estimate_materials`) using the Gemini API. It enforces JSON formatting and cleans up markdown blocks from the responses.
- **Database/SQLite Implementation:**
  - **Status:** Unimplemented. The files `backend/db/database.py` and `backend/db/models.py` are completely empty. No database connection or tables exist yet.

## 3. Frontend Status (Next.js)
- **UI Components (`src/components/`):** 
  - Present: `ClassifyResult.tsx`, `EstimateForm.tsx`, `EstimateResult.tsx`, `HistoryList.tsx`, `MaterialTable.tsx`, `PlanForm.tsx`, `ProductInput.tsx`, `ResultCard.tsx`.
- **TypeScript Interfaces (`src/types/index.ts`):**
  - Defines `PlanFormState` (`productName`, `targetQty`, `maxBudget`, `hasMandatory`, `mandatoryDetails`) and `MandatoryMaterial`. 
  - These interfaces *do not match* the backend Pydantic models nor the 6 fields required by the spec.
- **State Management:**
  - `src/app/plan/page.tsx` uses local React state (`useState`) to manage `isLoading`. It only simulates a network request via `setTimeout` instead of making a real API call.
  - `PlanForm.tsx` manages its local state for the form inputs. Upon submission, it constructs a payload (with an array of formatted strings for mandatory materials) and simply routes the user to `/plan/result` via `router.push()` without sending an actual HTTP request to the backend.

## 4. Deviations & Action Items

### Deviations from `makerflow-spec.md`
1. **Gemini Override Compliant:** The system successfully uses `gemini_service.py` and Gemini instead of Anthropic Claude.
2. **Schema Mismatch (Fragmented Fields):** The specification requires `EstimateRequest` to have exactly 6 fields (`product_name` [fixed enum], `target_qty`, `budget_max`, `has_mandatory_material`, `mandatory_material_name`, `allow_substitution`). Both the backend and frontend are currently using different, misaligned variables (e.g., `product_description`, `maxBudget`/`max_budget`, `mandatory_materials` array, `category_id`).
3. **Frontend API Integration:** The frontend is not sending any requests to `/estimate`. It logs the payload and immediately redirects the user.
4. **Input Constraints:** `PlanForm.tsx` uses a free-text input for `productName` instead of the fixed list (enum) required for the deterministic category fallback.
5. **Database Omission:** SQLite persistence for saving plans is entirely missing.

### Action Items for 100% MVP Compliance
1. **Unify Schemas:** 
   - Refactor `backend/models/request.py` and `backend/models/response.py` to match the exact v1.2.0 spec.
   - Refactor `frontend/src/types/index.ts` to mirror the updated backend Pydantic models exactly.
2. **Refactor `PlanForm.tsx`:** 
   - Convert the product name input to a dropdown containing the 7 fixed products.
   - Wire the form to make a real `fetch` request to `POST /estimate` (via an `api.ts` utility).
3. **Align Backend Prompts/Services:**
   - Update `gemini_service.py` prompts to output the exact JSON fields required by the new `EstimateResponse` (e.g., `procurement_advice`, proper `budget_status`).
4. **Implement SQLite Persistence:**
   - Write the SQLAlchemy models in `backend/db/models.py`.
   - Setup engine and session maker in `backend/db/database.py`.
   - Implement `POST /plans` and `GET /plans` in `backend/api/routes/plans.py`.
5. **Build the Results UI:**
   - Ensure `ResultPage` properly maps the newly formatted `EstimateResponse` to Sections A-G as specified.
