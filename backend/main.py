from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from routers import auth, users, models as models_router, code_generation, admin, payments
from config import Config

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=Config.APP_NAME,
    description=Config.APP_DESCRIPTION,
    version=Config.APP_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS.ALLOW_ORIGINS,
    allow_credentials=Config.CORS.ALLOW_CREDENTIALS,
    allow_methods=Config.CORS.ALLOW_METHODS,
    allow_headers=Config.CORS.ALLOW_HEADERS,
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(models_router.router)
app.include_router(code_generation.router)
app.include_router(admin.router)
app.include_router(payments.router)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to Code Generator API. See /docs for API documentation."
    }