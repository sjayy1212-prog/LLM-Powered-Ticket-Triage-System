from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.db.database import init_db
from app.api.routes_tickets import router as tickets_router
from app.api.routes_feedback import router as feedback_router
from app.api.routes_analytics import router as analytics_router

app = FastAPI(
    title="Ticket Triage AI",
    description="LLM-powered support ticket classification, routing, and response generation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets_router)
app.include_router(feedback_router)
app.include_router(analytics_router)


@app.on_event("startup")
def startup():
    logger.info("Initializing database...")
    init_db()
    logger.info("Ticket Triage AI is ready.")


@app.get("/health")
def health():
    return {"status": "ok"}