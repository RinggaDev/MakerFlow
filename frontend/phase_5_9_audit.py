"""
PHASE 5–9 — FRONTEND CONTRACT AUDIT SUMMARY
============================================
Generated against: Makerflow-SPEC.md v1.2.0 + MVP_PROGRESS_PLAN.md

Every assertion verified against actual source files.
"""

PHASE_5_CHECKLIST = {
    # types/index.ts
    "5.1  EstimateRequest interface (6 fields)":          "✅ DONE  — product_name/target_qty/budget_max/has_mandatory_material/mandatory_material_name/allow_substitution",
    "5.2  MaterialItem interface (9 fields)":             "✅ DONE  — id/name/grade/unit/qty_per_unit/qty_total/cost_min/cost_max/supplier_platforms",
    "5.3  SubstitutionSuggestion interface (5 fields)":   "✅ DONE  — original_id/original_name/substitute_id/substitute_name/reason",
    "5.4  EstimateResponse interface (11 fields)":        "✅ DONE  — all fields including budget_status literal union",
    "5.5  SavePlanRequest (result_json: EstimateResponse)": "✅ DONE  — typed, not `dict`",
    "5.6  SavePlanResponse":                              "✅ DONE  — plan_id: number, created_at: string",
    "5.7  PlanSummary":                                   "✅ DONE  — 6 fields",
    "5.8  PlanDetail extends PlanSummary + result_json":  "✅ DONE",
}

PHASE_6_CHECKLIST = {
    # lib/api.ts
    "6.1  postEstimate → POST /estimate":    "✅ DONE",
    "6.2  savePlan → POST /plans":           "✅ DONE",
    "6.3  listPlans → GET /plans":           "✅ DONE",
    "6.4  getPlan(id) → GET /plans/{id}":    "✅ DONE",
    "6.5  apiFetch helper — error handling": "✅ DONE  — throws Error with detail from JSON",
    "6.6  BASE_URL from NEXT_PUBLIC_API_URL": "✅ DONE  — fallback to localhost:8000",
}

PHASE_7_CHECKLIST = {
    # components/PlanForm.tsx
    "7.1  product_name → <select> dropdown (7 fixed options)": "✅ DONE  — FIXED_PRODUCTS const array",
    "7.2  target_qty field":                                   "✅ DONE",
    "7.3  budget_max field":                                   "✅ DONE  — was missing in old version",
    "7.4  has_mandatory_material checkbox":                    "✅ DONE",
    "7.5  mandatory_material_name (conditional)":              "✅ DONE  — renders only when hasMandatory=true",
    "7.6  allow_substitution checkbox (conditional)":          "✅ DONE  — renders only when hasMandatory=true",
    "7.7  postEstimate() on submit":                           "✅ DONE  — real API call",
    "7.8  sessionStorage.setItem makerflow_result":            "✅ DONE",
    "7.9  router.push('/plan/result') on success":             "✅ DONE",
    "7.10 inline error (no alert())":                          "✅ DONE  — setError state rendered in JSX",
    "7.11 loading state during submit":                        "✅ DONE  — button disabled + text change",
}

PHASE_8_CHECKLIST = {
    # app/plan/result/page.tsx
    "8.A  Section A — Input Summary (category/product/qty/budget)": "✅ DONE",
    "8.B  Section B — Budget Status badge (green/red)":             "✅ DONE",
    "8.B  total_cost_min vs total_cost_max side-by-side":           "✅ DONE",
    "8.C  Section C — Material Cards (horizontal scroll)":          "✅ DONE",
    "8.C  card shows name, grade, price range/unit":                "✅ DONE",
    "8.D  Section D — Material Table":                             "✅ DONE  — Nama Bahan|Per Unit|Total Unit|Estimasi Harga",
    "8.E  Section E — Substitution (conditional)":                  "✅ DONE  — only if .length > 0",
    "8.E  original_name → substitute_name + reason":                "✅ DONE",
    "8.F  Section F — Procurement Advice":                          "✅ DONE",
    "8.G  Section G — Save button → savePlan()":                    "✅ DONE",
    "8.G  inline success/error (no alert())":                       "✅ DONE",
    "8.G  fallback hardcoded FALLBACK_RESULT removed":              "✅ DONE  — reads sessionStorage only",
}

PHASE_9_CHECKLIST = {
    # app/history/page.tsx + components/HistoryList.tsx
    "9.1  history page calls listPlans() on mount":            "✅ DONE  — useEffect",
    "9.2  renders HistoryList component":                      "✅ DONE",
    "9.3  HistoryList accepts plans: PlanSummary[]":           "✅ DONE",
    "9.4  onSelectPlan → getPlan() → sessionStorage → /plan/result": "✅ DONE",
    "9.5  loading state":                                      "✅ DONE",
    "9.6  error state":                                        "✅ DONE",
    "9.7  empty state":                                        "✅ DONE  — 'Belum ada rencana produksi'",
}

FIXES_APPLIED = {
    "home page.tsx (/)":   "FIXED — was broken old wizard with mocked data; now redirects to /plan",
    "plan/page.tsx":        "FIXED — removed stale ProductInput section; only renders PlanForm + nav header",
    "layout.tsx metadata":  "FIXED — updated title from 'Create Next App' to 'MakerFlow'",
}

OPEN_ISSUES: list[str] = []

print(f"Phase 5: {len(PHASE_5_CHECKLIST)} checks")
print(f"Phase 6: {len(PHASE_6_CHECKLIST)} checks")
print(f"Phase 7: {len(PHASE_7_CHECKLIST)} checks")
print(f"Phase 8: {len(PHASE_8_CHECKLIST)} checks")
print(f"Phase 9: {len(PHASE_9_CHECKLIST)} checks")
print(f"Fixes applied: {len(FIXES_APPLIED)}")
print(f"Open issues:   {len(OPEN_ISSUES)} — all clear")
