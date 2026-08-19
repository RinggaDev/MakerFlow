from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class MaterialItem(BaseModel):
    id: str = Field(..., description="Material ID (e.g., YC001)")
    name: str = Field(..., description="Material Name")
    grade: str = Field(..., description="Single grade string (e.g. standard, premium)")
    unit: str = Field(..., description="Unit of measurement (e.g., meter, pcs, roll)")
    qty_per_unit: float = Field(..., description="Quantity needed per unit")
    qty_total: float = Field(..., description="Total quantity needed for production")
    cost_min: int = Field(..., description="Minimum cost in IDR")
    cost_max: int = Field(..., description="Maximum cost in IDR")
    supplier_platforms: List[str] = Field(default_factory=list, description="Supplier platform names")

class SubstitutionSuggestion(BaseModel):
    original_id: str = Field(..., description="ID of original material")
    original_name: str = Field(..., description="Name of original material")
    substitute_id: str = Field(..., description="ID of substitute material")
    substitute_name: str = Field(..., description="Name of substitute material")
    reason: str = Field(..., description="Reason for substitution")

class EstimateResponse(BaseModel):
    detected_category_ids: List[str] = Field(..., description="Category IDs detected by Call 1")
    detected_category_labels: List[str] = Field(..., description="Category labels detected by Call 1")
    product_name: str = Field(..., description="Product name echoed from request")
    target_qty: int = Field(..., description="Target production quantity echoed from request")
    available_budget: int = Field(..., description="Available budget echoed from request")
    budget_status: Literal["sufficient", "insufficient"] = Field(..., description="Flat budget status string")
    total_cost_min: int = Field(..., description="Total minimum estimated cost in IDR")
    total_cost_max: int = Field(..., description="Total maximum estimated cost in IDR")
    materials_needed: List[MaterialItem] = Field(default_factory=list, description="List of materials needed")
    substitution_suggestions: List[SubstitutionSuggestion] = Field(default_factory=list, description="List of substitution suggestions")
    procurement_advice: str = Field("", description="Procurement advice text")
    notes: str = Field("", description="Additional notes")
    estimated_affordable_qty: Optional[int] = Field(None, description="Populated only if budget_status is insufficient — reverse calc result")

class SavePlanResponse(BaseModel):
    plan_id: int
    created_at: str

class PlanSummary(BaseModel):
    id: int
    product_name: str
    target_qty: int
    budget_max: int
    category: str
    created_at: str

class PlanDetail(PlanSummary):
    result_json: dict

