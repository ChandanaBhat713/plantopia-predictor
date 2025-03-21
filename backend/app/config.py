
import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# API Settings
API_V1_STR = "/api"
PROJECT_NAME = "Plant Disease API"
PROJECT_DESCRIPTION = "API for plant disease detection using TensorFlow Serving"
PROJECT_VERSION = "1.0.0"

# CORS Settings
CORS_ORIGINS = ["*"]  # For production, specify your frontend domain
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Media Settings
MEDIA_DIR = os.path.join(BASE_DIR, "media")
UPLOAD_DIR = os.path.join(MEDIA_DIR, "uploads")
TEMP_DIR = os.path.join(MEDIA_DIR, "temp")

# TensorFlow Serving Configuration
TF_SERVING_HOST = os.environ.get("TF_SERVING_HOST", "localhost")
TF_SERVING_PORT = os.environ.get("TF_SERVING_PORT", "8501")
TF_SERVING_MODEL_NAME = os.environ.get("TF_SERVING_MODEL_NAME", "leaf_disease_model")
TF_SERVING_URL = f"http://{TF_SERVING_HOST}:{TF_SERVING_PORT}/v1/models/{TF_SERVING_MODEL_NAME}:predict"

# Database Settings
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "plant_disease_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Model Classes and Metadata
DISEASE_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

# Ensure directories exist
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
