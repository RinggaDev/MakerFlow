export interface EstimateRequest {
  product_name: string;
  target_qty: number;
  available_budget: number;
  has_mandatory_material: boolean;
  mandatory_material_name: string | null;
  allow_substitution: boolean | null;
}

export interface MaterialItem {
  id: string;
  name: string;
  grade: string;
  unit: string;
  qty_per_unit: number;
  qty_total: number;
  cost_min: number;
  cost_max: number;
  supplier_platforms: string[];
}

export interface SubstitutionSuggestion {
  original_id: string;
  original_name: string;
  substitute_id: string;
  substitute_name: string;
  reason: string;
}

export interface EstimateResponse {
  detected_category_ids: string[];
  detected_category_labels: string[];
  product_name: string;
  target_qty: number;
  available_budget: number;
  budget_status: "sufficient" | "insufficient";
  total_cost_min: number;
  total_cost_max: number;
  materials_needed: MaterialItem[];
  substitution_suggestions: SubstitutionSuggestion[];
  procurement_advice: string;
  notes: string;
  estimated_affordable_qty: number | null;
}

export interface SavePlanRequest {
  product_name: string;
  target_qty: number;
  budget_max: number;
  category: string;
  result_json: EstimateResponse;
}

export interface SavePlanResponse {
  plan_id: number;
  created_at: string;
}

export interface PlanSummary {
  id: number;
  product_name: string;
  target_qty: number;
  budget_max: number;
  category: string;
  created_at: string;
}

export interface PlanDetail extends PlanSummary {
  result_json: EstimateResponse;
}