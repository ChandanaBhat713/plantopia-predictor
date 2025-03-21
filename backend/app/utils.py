
import os
import uuid
from fastapi import UploadFile, HTTPException

def save_uploaded_image(image: UploadFile) -> tuple[str, str]:
    """
    Save an uploaded image and return the file paths.
    
    Args:
        image: The uploaded image file
        
    Returns:
        tuple: (temp_file_path, permanent_file_path)
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    
    # Create necessary directories
    os.makedirs("media/plant_images", exist_ok=True)
    os.makedirs("media/temp_uploads", exist_ok=True)
    
    # Save the uploaded image temporarily
    temp_file_path = f"media/temp_uploads/{uuid.uuid4()}{os.path.splitext(image.filename)[1]}"
    
    return temp_file_path, f"media/plant_images/{uuid.uuid4()}{os.path.splitext(image.filename)[1]}"

def get_demo_sources() -> list:
    """Return demo data sources."""
    return [
        {
            "title": "Plant Village Database",
            "url": "https://plantvillage.psu.edu/"
        },
        {
            "title": "Agricultural Extension Service",
            "url": "https://extension.org/"
        }
    ]

def get_demo_treatments() -> dict:
    """Return demo treatment data."""
    return {
        "Apple___Apple_scab": "Apply fungicides early in the growing season. Remove and destroy infected leaves. Use resistant varieties if possible.",
        "Tomato___Early_blight": "Remove infected leaves. Apply fungicides. Mulch around plants. Avoid overhead watering. Rotate crops."
    }

def get_demo_plants_info() -> dict:
    """Return demo plant information data."""
    return {
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
