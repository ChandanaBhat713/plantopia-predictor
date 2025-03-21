
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from .models import TreatmentResponse, PlantInfoResponse, PredictionResponse, ScanResponse
from .database import add_scan, get_all_scans, get_scan_by_id
from .utils import save_uploaded_image, get_demo_sources, get_demo_treatments, get_demo_plants_info
from ml_model import predict_leaf_disease

# Initialize router
router = APIRouter(prefix="/api")

@router.post("/predict", response_model=PredictionResponse)
async def predict_plant_disease(image: UploadFile = File(...)):
    temp_file_path, permanent_file_path = save_uploaded_image(image)
    
    try:
        contents = await image.read()
        with open(temp_file_path, "wb") as f:
            f.write(contents)
        
        # Make prediction using TensorFlow Serving
        prediction_result = predict_leaf_disease(temp_file_path)
        
        # Check if there was an error
        if 'error' in prediction_result:
            raise HTTPException(status_code=500, detail=prediction_result['error'])
        
        # Save to permanent location
        os.rename(temp_file_path, permanent_file_path)
        
        # Get the relative path for the URL
        relative_path = permanent_file_path.replace("media/", "")
        image_url = f"/media/{relative_path}"
        
        # Save scan to database
        scan_id = str(uuid.uuid4())
        add_scan(scan_id, image_url, prediction_result['disease'], prediction_result['confidence'])
        
        # Add sources (demo data)
        sources = get_demo_sources()
        
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

@router.get("/treatment/{disease}", response_model=TreatmentResponse)
async def get_treatment(disease: str):
    # Demo treatment data
    treatments = get_demo_treatments()
    
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

@router.get("/plant-info/{plant_name}", response_model=PlantInfoResponse)
async def get_plant_info(plant_name: str):
    # Demo plant info data
    plants_info = get_demo_plants_info()
    
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

@router.get("/history", response_model=List[ScanResponse])
async def get_scan_history():
    # Convert our in-memory database to response format
    scans = []
    for scan in get_all_scans():
        scans.append({
            "id": scan["id"],
            "disease": scan["disease"],
            "confidence": scan["confidence"],
            "timestamp": scan["timestamp"],
            "imageUrl": scan["image"]
        })
    return scans

@router.get("/history/{scan_id}", response_model=ScanResponse)
async def get_scan_detail(scan_id: str):
    # Find scan in our in-memory database
    scan = get_scan_by_id(scan_id)
    if scan:
        return {
            "id": scan["id"],
            "disease": scan["disease"],
            "confidence": scan["confidence"],
            "timestamp": scan["timestamp"],
            "imageUrl": scan["image"]
        }
    
    raise HTTPException(status_code=404, detail="Scan not found")
