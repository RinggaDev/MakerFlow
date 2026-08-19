from fastapi import APIRouter, HTTPException
from models.request import EstimateRequest
from models.response import EstimateResponse
from services.dataset_service import get_filtered_materials, resolve_category
from services.gemini_service import estimate_materials, classify_product

router = APIRouter()

@router.post("/estimate", response_model=EstimateResponse)
async def estimate_route(request: EstimateRequest):
    """
    Full two-call pipeline per SPEC v1.4.0:
    Call 1 → multi-category classification → dataset merge → Call 2 estimation.
    """
    try:
        # Step 1: LLM Classification (Call 1) — returns lists
        classify_result = classify_product(request.product_name)
        llm_category_ids = classify_result.get("category_ids", [])
        llm_category_labels = classify_result.get("category_labels", [])

        # Step 2: Validate + Fallback (list-aware)
        validated_ids = resolve_category(llm_category_ids, request.product_name)

        # Step 3: Load & merge datasets for all validated categories
        filtered_materials = get_filtered_materials(
            category_ids=validated_ids,
            product_name=request.product_name,
            mandatory_material_name=request.mandatory_material_name,
        )

        # Step 4: LLM Estimation (Call 2)
        estimate_result = estimate_materials(
            product_name=request.product_name,
            target_qty=request.target_qty,
            available_budget=request.available_budget,
            mandatory_material_name=request.mandatory_material_name,
            allow_substitution=request.allow_substitution,
            filtered_materials=filtered_materials,
        )

        # Step 5: Assemble — fallback labels to IDs if LLM returned mismatched counts
        category_labels = llm_category_labels if len(llm_category_labels) == len(validated_ids) else validated_ids

        return EstimateResponse(
            detected_category_ids=validated_ids,
            detected_category_labels=category_labels,
            product_name=request.product_name,
            target_qty=request.target_qty,
            available_budget=request.available_budget,
            **estimate_result,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Estimation error: {str(e)}")
