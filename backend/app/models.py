
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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
