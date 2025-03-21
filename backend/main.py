
import os
import time
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import our ML model utilities
from ml_model import load_model_into_memory
from app.routes import router

# Initialize FastAPI app
app = FastAPI(
    title="Plant Disease API",
    description="API for plant disease detection using TensorFlow Serving",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check TensorFlow Serving status when application starts
@app.on_event("startup")
def startup_event():
    load_model_into_memory()

# Mount static files directory for serving media
app.mount("/media", StaticFiles(directory="media"), name="media")

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
