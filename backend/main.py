
import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time
import datetime
import uvicorn

# Import our ML model utilities
from ml_model import load_model_into_memory, predict_leaf_disease

# Initialize FastAPI app
app = FastAPI(
    title="Plant Disease API",
    description="API for plant disease detection using CNN",
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

# Create necessary directories
os.makedirs("media/plant_images", exist_ok=True)
os.makedirs("media/temp_uploads", exist_ok=True)

# Load model when application starts
@app.on_event("startup")
def startup_event():
    load_model_into_memory()

# Mount static files directory for serving media
app.mount("/media", StaticFiles(directory="media"), name="media")

# In-memory database for scan history (replace with PostgreSQL in production)
plant_scans = []

# Pydantic models for request/response validation
class TreatmentResponse(BaseModel):
    disease: str
    treatment: str
    steps: List[str]

class PlantCare(BaseModel):
    water: str
    sunlight: str
    temperature: str
    airflow: Optional[str] = None

class PlantInfoResponse(BaseModel):
    name: str
    scientificName: str
    care: PlantCare
    preventionTips: List[str]

class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    description: str
    treatment: str
    sources: Optional[List[Dict[str, str]]] = None

class ScanResponse(BaseModel):
    id: str
    disease: str
    confidence: float
    timestamp: str
    imageUrl: str

# API endpoints
@app.post("/api/predict", response_model=PredictionResponse)
async def predict_plant_disease(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    
    # Save the uploaded image temporarily
    temp_file_path = f"media/temp_uploads/{uuid.uuid4()}{os.path.splitext(image.filename)[1]}"
    
    try:
        contents = await image.read()
        with open(temp_file_path, "wb") as f:
            f.write(contents)
        
        # Make prediction
        prediction_result = predict_leaf_disease(temp_file_path)
        
        # Check if there was an error
        if 'error' in prediction_result:
            raise HTTPException(status_code=500, detail=prediction_result['error'])
        
        # Save to permanent location
        permanent_file_path = f"media/plant_images/{uuid.uuid4()}{os.path.splitext(image.filename)[1]}"
        os.rename(temp_file_path, permanent_file_path)
        
        # Get the relative path for the URL
        relative_path = permanent_file_path.replace("media/", "")
        image_url = f"/media/{relative_path}"
        
        # Save scan to database
        scan_id = str(uuid.uuid4())
        plant_scans.append({
            "id": scan_id,
            "image": image_url,
            "disease": prediction_result['disease'],
            "confidence": prediction_result['confidence'],
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Add sources (demo data)
        sources = [
            {
                "title": "Plant Village Database",
                "url": "https://plantvillage.psu.edu/"
            },
            {
                "title": "Agricultural Extension Service",
                "url": "https://extension.org/"
            }
        ]
        
        # Prepare response data
        response_data = {
            "disease": prediction_result['disease'],
            "confidence": prediction_result['confidence'],
            "description": prediction_result['description'],
            "treatment": prediction_result['treatment'],
            "sources": sources
        }
        
        return response_data
    
    except Exception as e:
        # Clean up temporary file if it exists
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up temporary file if it exists
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass

@app.get("/api/treatment/{disease}", response_model=TreatmentResponse)
async def get_treatment(disease: str):
    # Demo treatment data
    treatments = {
        "Apple___Apple_scab": "Apply fungicides early in the growing season. Remove and destroy infected leaves. Use resistant varieties if possible.",
        "Tomato___Early_blight": "Remove infected leaves. Apply fungicides. Mulch around plants. Avoid overhead watering. Rotate crops."
    }
    
    treatment = treatments.get(disease, "No specific treatment found for this disease.")
    
    return {
        "disease": disease,
        "treatment": treatment,
        "steps": [
            "Remove all infected leaves and dispose of them properly.",
            "Apply appropriate fungicide according to label instructions.",
            "Improve air circulation around plants.",
            "Water at the base of plants to avoid wetting foliage.",
            "Rotate crops in future growing seasons."
        ]
    }

@app.get("/api/plant-info/{plant_name}", response_model=PlantInfoResponse)
async def get_plant_info(plant_name: str):
    # Demo plant info data
    plants_info = {
        "tomato": {
            "name": "Tomato",
            "scientificName": "Solanum lycopersicum",
            "care": {
                "water": "Regular watering, 1-2 inches per week",
                "sunlight": "Full sun, 6-8 hours daily",
                "temperature": "65-85°F (18-29°C)",
                "airflow": "Good ventilation to prevent fungal diseases"
            },
            "preventionTips": [
                "Rotate crops every 3-4 years",
                "Use disease-resistant varieties",
                "Provide proper spacing for air circulation",
                "Water at the base to keep foliage dry",
                "Remove and destroy diseased plant material"
            ]
        },
        "apple": {
            "name": "Apple",
            "scientificName": "Malus domestica",
            "care": {
                "water": "1 inch of water per week during growing season",
                "sunlight": "Full sun, 6-8 hours daily",
                "temperature": "60-80°F (15-27°C)",
                "airflow": "Proper pruning for good air circulation"
            },
            "preventionTips": [
                "Proper pruning to improve air circulation",
                "Clean up fallen leaves and fruit",
                "Apply dormant sprays before bud break",
                "Use disease-resistant varieties",
                "Manage insect pests promptly"
            ]
        }
    }
    
    plant_info = plants_info.get(plant_name.lower(), {
        "name": plant_name.capitalize(),
        "scientificName": "Not available",
        "care": {
            "water": "General care information not available",
            "sunlight": "General care information not available",
            "temperature": "General care information not available",
            "airflow": "General care information not available"
        },
        "preventionTips": [
            "Use disease-resistant varieties",
            "Practice crop rotation",
            "Maintain good air circulation",
            "Water properly, avoiding wet foliage",
            "Monitor regularly for early detection of issues"
        ]
    })
    
    return plant_info

@app.get("/api/history", response_model=List[ScanResponse])
async def get_scan_history():
    # Convert our in-memory database to response format
    scans = []
    for scan in plant_scans:
        scans.append({
            "id": scan["id"],
            "disease": scan["disease"],
            "confidence": scan["confidence"],
            "timestamp": scan["timestamp"],
            "imageUrl": scan["image"]
        })
    return scans

@app.get("/api/history/{scan_id}", response_model=ScanResponse)
async def get_scan_detail(scan_id: str):
    # Find scan in our in-memory database
    for scan in plant_scans:
        if scan["id"] == scan_id:
            return {
                "id": scan["id"],
                "disease": scan["disease"],
                "confidence": scan["confidence"],
                "timestamp": scan["timestamp"],
                "imageUrl": scan["image"]
            }
    
    raise HTTPException(status_code=404, detail="Scan not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
