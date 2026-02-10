from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sovilo's Aesthetics API",
    description="API for appointments, services, reviews and contact forms.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes.auth import router as auth_router

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/appointments")
async def create_appointment():
    # TODO: implement MongoDB insert + email sending
    return {"message": "Appointment endpoint stub"}


@app.post("/api/contact")
async def contact():
    # TODO: implement email sending
    return {"message": "Contact endpoint stub"}


@app.get("/api/services")
async def list_services():
    # TODO: return structured services data or fetch from DB
    return {"services": []}


@app.get("/api/reviews")
async def list_reviews():
    # TODO: return curated reviews
    return {"reviews": []}

