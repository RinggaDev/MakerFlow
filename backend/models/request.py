from typing import Optional
from pydantic import BaseModel, Field, model_validator

class EstimateRequest(BaseModel):
    product_name: str = Field(..., description="Name of the product from fixed dropdown")
    target_qty: int = Field(..., gt=0, description="Target production quantity required")
    available_budget: int = Field(..., gt=0, description="Total available budget/modal owned by the user (IDR)")
    has_mandatory_material: bool = Field(..., description="Flag indicating if mandatory material is required")
    mandatory_material_name: Optional[str] = Field(None, description="Name of mandatory material if has_mandatory_material is True")
    allow_substitution: Optional[bool] = Field(None, description="Whether substitution is allowed for non-mandatory materials")

    @model_validator(mode="after")
    def validate_mandatory_fields(self):
        if self.has_mandatory_material:
            if not self.mandatory_material_name:
                raise ValueError("mandatory_material_name required when has_mandatory_material is true")
            if self.allow_substitution is None:
                raise ValueError("allow_substitution required when has_mandatory_material is true")
        return self

class SavePlanRequest(BaseModel):
    product_name: str = Field(..., description="Name of the product")
    target_qty: int = Field(..., gt=0, description="Target production quantity")
    budget_max: int = Field(..., gt=0, description="Budget ceiling in IDR")
    category: str = Field(..., description="Detected category label or ID")
    result_json: dict = Field(..., description="Full EstimateResponse JSON dictionary")

