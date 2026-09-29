from fastapi import APIRouter
from .endpoints import health, employees, machines, orders, tasks, production, telemetry, maintenance, incidents

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(machines.router, prefix="/machines", tags=["machines"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(production.router, prefix="/production", tags=["production"])
api_router.include_router(telemetry.router, prefix="/telemetry", tags=["telemetry"])
api_router.include_router(maintenance.router, prefix="/maintenance", tags=["maintenance"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
