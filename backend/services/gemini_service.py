"""
gemini_service.py

AI service layer for MakerFlow — implements the two-call pipeline per SPEC v1.3.0.

Model Routing (Section 2.3 Hybrid Strategy):
  Call 1 — Classification : gemini-2.0-flash-lite  (lightweight, fast, token-efficient)
  Call 2 — Estimation     : gemini-2.0-flash        (heavy reasoning for cost optimization)

Both calls use google-genai SDK with response_mime_type="application/json" to enforce
structured output. Regex-based markdown fence stripping is applied as a safety net per
SPEC Section 5.5 (Gemini sometimes wraps output in ```json fences despite instructions).
"""

import os
import json
import re
from typing import Optional

from google import genai
from google.genai import types
from fastapi import HTTPException

# ---------------------------------------------------------------------------
# Model constants — SPEC v1.3.0 Section 2.3 Hybrid Model Routing
# ---------------------------------------------------------------------------
MODEL_CLASSIFY = "gemini-3.1-flash-lite"  # Call 1: lightweight classifier (fast, cheap)
MODEL_ESTIMATE = "gemini-3.5-flash"       # Call 2: heavy estimation + cost reasoning


# ---------------------------------------------------------------------------
# Private helper
# ---------------------------------------------------------------------------

def _call_gemini_json(prompt: str, model: str) -> dict:
    """
    Call Gemini API with the specified model, return parsed JSON dict.

    Args:
        prompt: The full prompt string to send.
        model:  Model ID to use (MODEL_CLASSIFY or MODEL_ESTIMATE).

    Returns:
        Parsed dict from Gemini JSON response.

    Raises:
        HTTPException 500: If GEMINI_API_KEY is not set.
        HTTPException 502: If Gemini API call or JSON parsing fails.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )
        text = response.text.strip()
        # Regex strip: handles ```json, ```, any whitespace/newline variants
        # Per SPEC Section 5.5 — mandatory safety net for Gemini fence wrapping
        text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s*```$', '', text)
        return json.loads(text.strip())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini error [{model}]: {e}")


# ---------------------------------------------------------------------------
# Call 1 — Classification (uses MODEL_CLASSIFY: gemini-2.0-flash-lite)
# ---------------------------------------------------------------------------

def classify_product(product_name: str) -> dict:
    """
    Call 1 — LLM product classification using lightweight model.

    For cross-category products (SPEC v1.4.0), the LLM now returns LISTS of
    category_ids and category_labels instead of single strings.
    resolve_category() in dataset_service.py validates and applies fallback.

    Args:
        product_name: Product name from the fixed dropdown.

    Returns:
        dict with keys: category_ids (list[str]), category_labels (list[str])
    """
    prompt = f"""You are a product category classifier for a craft production planning system.
A product may belong to MULTIPLE categories simultaneously.

AVAILABLE CATEGORIES:
- yarn_craft     : Kerajinan Benang & Tali
- resin_craft    : Kerajinan Resin
- wood_craft     : Kerajinan Kayu
- packaging_gift : Kemasan & Gift Box
- textile_craft  : Kerajinan Tekstil & Kain

PRODUCT: "{product_name}"

Reply ONLY in this exact JSON, no markdown fences:
{{
  "category_ids": ["string"],
  "category_labels": ["string"]
}}"""
    return _call_gemini_json(prompt, MODEL_CLASSIFY)


# ---------------------------------------------------------------------------
# Call 2 — Estimation
# ---------------------------------------------------------------------------

def estimate_materials(
    product_name: str,
    target_qty: int,
    available_budget: int,
    mandatory_material_name: Optional[str],
    allow_substitution: Optional[bool],
    filtered_materials: list[dict],
) -> dict:
    """
    Call 2 — LLM material estimation using heavy reasoning model.

    Receives filtered dataset materials and produces full cost estimation.
    Implements SPEC v1.3.0 Section 4.5 Strict Grounded RAG constraints —
    the model is forbidden from hallucinating materials, prices, or platforms
    outside the injected dataset.

    Args:
        product_name:             Product name from fixed dropdown.
        target_qty:               Target production quantity in units.
        available_budget:         Total available budget/modal owned by the user (IDR).
        mandatory_material_name:  Free-text name of locked material (or None).
        allow_substitution:       Whether non-mandatory materials may be substituted.
        filtered_materials:       Pre-filtered materials list from dataset_service.py.

    Returns:
        dict matching EstimateResponse fields (budget_status, totals, materials, etc.)
    """
    materials_str = json.dumps(filtered_materials, indent=2, ensure_ascii=False)
    mandatory_str = mandatory_material_name or "Tidak ada"
    allow_sub_str = str(allow_substitution) if allow_substitution is not None else "Tidak ada"

    prompt = f"""You are a production planning assistant for Indonesian SMEs.
All output must be in Bahasa Indonesia.

AVAILABLE RAW MATERIALS DATA:
{materials_str}

USER INPUT:
- Produk           : {product_name}
- Target Qty       : {target_qty} unit
- Available Budget : Rp {available_budget}
- Bahan Wajib      : {mandatory_str}
- Boleh Substitusi : {allow_sub_str}

TASKS:
1. Estimate qty_per_unit and qty_total for each required material
2. Calculate cost_min and cost_max per material from price_range in the data
3. Sum total_cost_min and total_cost_max across all materials
4. Set budget_status = "sufficient" if total_cost_max <= available_budget, otherwise "insufficient"
5. If allow_substitution=true AND budget insufficient: suggest cheaper alternatives from AVAILABLE DATA only
6. Write procurement_advice listing supplier_platforms per material
7. If budget_status is "insufficient", perform REVERSE CALCULATION: Calculate the estimated HPP (Harga Pokok Produksi) per 1 unit. Divide the {available_budget} by the estimated HPP per unit. FLOOR the result to the nearest whole integer. Populate the "estimated_affordable_qty" field with this number.

CONSTRAINTS (STRICT GROUNDED RAG - CRITICAL):
1. HANYA gunakan material yang tersedia di AVAILABLE RAW MATERIALS DATA.
2. DILARANG KERAS menambah, mengarang, atau menebak material, harga, atau platform di luar data yang disediakan.
3. Jika material yang dibutuhkan user tidak ada di data, abaikan material tersebut dan tulis penjelasan di field "notes" (contoh: "Kain parasut tidak tersedia di database kami, estimasi biaya hanya mencakup bahan yang tersedia.").
4. mandatory_material_name wajib ada di output, jangan disubstitusi.
5. grade: pick the single most appropriate grade string per item (string, not array).
6. For reverse calculation (Task 7), use the average of cost_min and cost_max to estimate HPP per unit. Always floor the final quantity to an integer. If budget_status is "sufficient", set estimated_affordable_qty to null.

Reply ONLY in this exact JSON, no markdown fences:
{{
  "budget_status": "sufficient",
  "total_cost_min": 0,
  "total_cost_max": 0,
  "materials_needed": [
    {{
      "id": "string",
      "name": "string",
      "grade": "string",
      "unit": "string",
      "qty_per_unit": 0.0,
      "qty_total": 0.0,
      "cost_min": 0,
      "cost_max": 0,
      "supplier_platforms": ["string"]
    }}
  ],
  "substitution_suggestions": [
    {{
      "original_id": "string",
      "original_name": "string",
      "substitute_id": "string",
      "substitute_name": "string",
      "reason": "string"
    }}
  ],
  "procurement_advice": "string",
  "notes": "string",
  "estimated_affordable_qty": null
}}"""
    return _call_gemini_json(prompt, MODEL_ESTIMATE)
