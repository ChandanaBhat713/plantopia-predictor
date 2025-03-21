
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import configuration and ML model utilities
from app.config import (
    PROJECT_NAME, 
    PROJECT_DESCRIPTION, 
    PROJECT_VERSION,
    CORS_ORIGINS, 
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS,
    MEDIA_DIR
)
from ml_model import load_model_into_memory
from app.routes import router

# Initialize FastAPI app
app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=PROJECT_VERSION
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Check TensorFlow Serving status when application starts
@app.on_event("startup")
def startup_event():
    load_model_into_memory()

# Mount static files directory for serving media
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
