import type {
  EstimateRequest,
  EstimateResponse,
  SavePlanRequest,
  SavePlanResponse,
  PlanSummary,
  PlanDetail,
} from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorData.detail || `HTTP Error ${res.status}`);
  }

  return res.json();
}

export async function postEstimate(req: EstimateRequest): Promise<EstimateResponse> {
  return apiFetch<EstimateResponse>("/estimate", {
    method: "POST",
    body: JSON.stringify(req),
  });
}

export async function savePlan(req: SavePlanRequest): Promise<SavePlanResponse> {
  return apiFetch<SavePlanResponse>("/plans", {
    method: "POST",
    body: JSON.stringify(req),
  });
}

export async function listPlans(): Promise<PlanSummary[]> {
  return apiFetch<PlanSummary[]>("/plans");
}

export async function getPlan(id: number): Promise<PlanDetail> {
  return apiFetch<PlanDetail>(`/plans/${id}`);
}
