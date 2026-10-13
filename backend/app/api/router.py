
from fastapi import APIRouter

from app.api.routes import (
    health,
    profile,
    skills,
    education,
    projects,
    experiences,
    resume,
    jobs,
    agent
)

api_router = APIRouter()


api_router.include_router(
    health.router
)


api_router.include_router(
    profile.router
)

api_router.include_router(
    skills.router
)

api_router.include_router(
    education.router
)

api_router.include_router(
    projects.router
)

api_router.include_router(
    experiences.router
)

api_router.include_router(
    resume.router
)

api_router.include_router(
    jobs.router
)

api_router.include_router(
    agent.router
)