
import datetime
from typing import List, Dict, Any

# In-memory database for scan history (replace with PostgreSQL in production)
plant_scans: List[Dict[str, Any]] = []

def add_scan(scan_id: str, image_url: str, disease: str, confidence: float) -> None:
    """Add a new scan to the in-memory database."""
    plant_scans.append({
        "id": scan_id,
        "image": image_url,
        "disease": disease,
        "confidence": confidence,
        "timestamp": datetime.datetime.now().isoformat()
    })

def get_all_scans() -> List[Dict[str, Any]]:
    """Get all scans from the in-memory database."""
    return plant_scans

def get_scan_by_id(scan_id: str) -> Dict[str, Any]:
    """Get a specific scan by its ID."""
    for scan in plant_scans:
        if scan["id"] == scan_id:
            return scan
    return None
