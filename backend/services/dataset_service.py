"""
dataset_service.py

Lightweight RAG: Local JSON loading and keyword-based material filtering.
Datasets live at the monorepo root (`datasets/`), mounted read-only into the
container at `/app/datasets`. For local development the path is resolved
relative to this file's location (backend/../datasets/).

Functions:
    load_index()               → Load datasets/index.json
    load_category_file()       → Load a specific category JSON file
    get_filtered_materials()   → Main filter function (mandatory + keyword + hard cap)
"""

import json
import os
from pathlib import Path
from typing import Any

from fastapi import HTTPException

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------
# Resolves to <monorepo_root>/datasets/ regardless of where the server is
# launched from, and regardless of whether it runs locally or in Docker.
#
# In Docker:  backend code lives at /app, datasets mounted at /app/datasets
# Locally:    backend code at .../backend/, datasets at .../datasets/
# ---------------------------------------------------------------------------

_BACKEND_DIR = Path(__file__).resolve().parent.parent  # backend/
_DATASETS_DIR = _BACKEND_DIR.parent / "datasets"       # monorepo_root/datasets/

# Docker override: if /app/datasets exists (inside container), prefer it.
_DOCKER_DATASETS = Path("/app/datasets")
if _DOCKER_DATASETS.is_dir():
    _DATASETS_DIR = _DOCKER_DATASETS


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _load_json(path: Path) -> Any:
    """Load and parse a JSON file. Raises HTTPException on any error."""
    if not path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Dataset file not found: {path.name}. Check that the datasets volume is mounted correctly."
        )
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON in dataset file '{path.name}': {str(exc)}"
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_index() -> dict:
    """
    Load datasets/index.json which contains the category registry and
    file routing table.

    Returns:
        dict: Parsed contents of index.json.
    """
    return _load_json(_DATASETS_DIR / "index.json")


def load_category_file(filename: str) -> dict:
    """
    Load a specific category JSON file from the datasets directory.

    Args:
        filename: Bare filename as stored in index.json (e.g. 'yarn_craft.json').

    Returns:
        dict: Parsed contents of the category file.
    """
    # Prevent directory traversal attacks
    safe_name = Path(filename).name
    return _load_json(_DATASETS_DIR / safe_name)


def get_category_by_id(category_id: str) -> dict:
    """
    Resolve a category entry from index.json by its ID.

    Args:
        category_id: e.g. 'yarn_craft', 'resin_craft'

    Returns:
        dict: The matching category entry from index.json['categories'].

    Raises:
        HTTPException 404: If category_id is not found in the index.
    """
    index = load_index()
    for cat in index.get("categories", []):
        if cat.get("id") == category_id:
            return cat
    raise HTTPException(
        status_code=404,
        detail=(
            f"Category '{category_id}' not found in index.json. "
            f"Valid category IDs: {[c['id'] for c in index.get('categories', [])]}"
        )
    )



# ponytail: values are lists — single-cat products use a 1-element list, cross-cat use N-element lists
PRODUCT_CATEGORY_MAP: dict[str, list[str]] = {
    "Gelang Macramé / Bracelet Custom":                        ["yarn_craft"],
    "Kerajinan Miniatur Rajutan":                              ["yarn_craft"],
    "Key Chain Rajut Custom Karakter":                         ["yarn_craft"],
    "Key Chain Resin":                                         ["resin_craft"],
    "Figura Kayu":                                             ["wood_craft"],
    "Kemasan Gift Box":                                        ["packaging_gift"],
    "Totebag Canvas (Custom Draw)":                            ["textile_craft"],
    "Gantungan Kunci Resin Kayu Premium + Rumbai":             ["resin_craft", "wood_craft", "yarn_craft", "packaging_gift"],
    "Pouch Kanvas Resleting dengan Gantungan Resin":           ["textile_craft", "resin_craft", "packaging_gift"],
    "Paket Kado Figura Kayu & Boneka Rajut":                   ["wood_craft", "yarn_craft", "packaging_gift"],
    "Totebag Kanvas dengan Tali Makrame & Pegangan Resin":     ["textile_craft", "yarn_craft", "resin_craft", "packaging_gift"],
}

KNOWN_CATEGORY_IDS = {cid for cats in PRODUCT_CATEGORY_MAP.values() for cid in cats}


def resolve_category(llm_category_ids: list[str], product_name: str) -> list[str]:
    """
    Validates LLM Call 1 output (list of category IDs) against known IDs.
    Falls back to hardcoded map if any ID is invalid / hallucinated.
    """
    if llm_category_ids and all(cid in KNOWN_CATEGORY_IDS for cid in llm_category_ids):
        return llm_category_ids
    return PRODUCT_CATEGORY_MAP.get(product_name, ["yarn_craft"])


def get_filtered_materials(
    category_ids: list[str],
    product_name: str,
    mandatory_material_name: str | None = None,
) -> list[dict]:
    """
    Multi-category Lightweight RAG filter — implements SPEC v1.4.0 Section 4.5.

    Loads and merges materials from ALL relevant category JSON files,
    then filters down to materials relevant to the product.
    Returns max 45 items (increased from 30 for multi-category context window).

    Args:
        category_ids:            List of validated category IDs.
        product_name:            Product name for keyword tag matching.
        mandatory_material_name: Material name user locked; force-included via fuzzy match.

    Returns:
        list[dict]: Filtered + merged material list, max 45 items.
    """
    index = load_index()
    categories_by_id = {c["id"]: c for c in index.get("categories", [])}

    # 1. Gather and merge materials from ALL relevant category files
    merged: list[dict] = []
    for cat_id in category_ids:
        cat_entry = categories_by_id.get(cat_id)
        if not cat_entry:
            raise HTTPException(
                status_code=404,
                detail=f"Category '{cat_id}' not found in index.json."
            )
        cat_data = load_category_file(cat_entry["file"])
        merged.extend(cat_data.get("materials", []))

    if not merged:
        raise HTTPException(status_code=500, detail="No materials found for the requested categories.")

    # 2. Filter logic
    keywords = [kw.strip().lower() for kw in product_name.lower().replace("/", " ").split() if kw.strip()]

    filtered: list[dict] = []
    for m in merged:
        mat_name: str = m.get("name", "").lower()
        mat_tags: list[str] = [t.lower() for t in m.get("tags", [])]

        # Force-include mandatory material by fuzzy name match
        if mandatory_material_name and mandatory_material_name.strip().lower() in mat_name:
            filtered.append(m)
            continue

        if keywords and any(kw in tag for kw in keywords for tag in mat_tags):
            filtered.append(m)

    # Safety fallback: if filter returns nothing, use all merged materials
    if not filtered:
        filtered = merged

    return filtered[:45]  # ponytail: hard cap increased to 45 for multi-category hygiene

