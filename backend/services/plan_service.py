import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import ProductionPlan
from models.request import SavePlanRequest
from models.response import SavePlanResponse, PlanSummary, PlanDetail

def save_plan(db: Session, req: SavePlanRequest) -> SavePlanResponse:
    plan = ProductionPlan(
        product_name=req.product_name,
        target_qty=req.target_qty,
        budget_max=req.budget_max,
        category=req.category,
        result_json=json.dumps(req.result_json, ensure_ascii=False),
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return SavePlanResponse(
        plan_id=plan.id,
        created_at=plan.created_at.isoformat()
    )

def list_plans(db: Session) -> list[PlanSummary]:
    plans = db.query(ProductionPlan).order_by(ProductionPlan.created_at.desc()).all()
    return [
        PlanSummary(
            id=p.id,
            product_name=p.product_name,
            target_qty=p.target_qty,
            budget_max=p.budget_max,
            category=p.category,
            created_at=p.created_at.isoformat(),
        )
        for p in plans
    ]

def get_plan(db: Session, plan_id: int) -> PlanDetail:
    plan = db.query(ProductionPlan).filter(ProductionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return PlanDetail(
        id=plan.id,
        product_name=plan.product_name,
        target_qty=plan.target_qty,
        budget_max=plan.budget_max,
        category=plan.category,
        created_at=plan.created_at.isoformat(),
        result_json=json.loads(plan.result_json),
    )
