from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.request import SavePlanRequest
from models.response import SavePlanResponse, PlanSummary, PlanDetail
from services.plan_service import save_plan as service_save_plan, list_plans as service_list_plans, get_plan as service_get_plan

router = APIRouter()

@router.post("/plans", response_model=SavePlanResponse)
async def create_plan(request: SavePlanRequest, db: Session = Depends(get_db)):
    return service_save_plan(db, request)

@router.get("/plans", response_model=list[PlanSummary])
async def get_plans_list(db: Session = Depends(get_db)):
    return service_list_plans(db)

@router.get("/plans/{plan_id}", response_model=PlanDetail)
async def get_single_plan(plan_id: int, db: Session = Depends(get_db)):
    return service_get_plan(db, plan_id)
