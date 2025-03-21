
import datetime
from typing import List, Dict, Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import DATABASE_URL

# Connect to the PostgreSQL database
def get_db_connection():
    """Create a connection to the PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn

def initialize_database():
    """Initialize the database by creating required tables if they don't exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create plant_scans table if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS plant_scans (
        id VARCHAR(36) PRIMARY KEY,
        image_url VARCHAR(255) NOT NULL,
        disease VARCHAR(255) NOT NULL,
        confidence FLOAT NOT NULL,
        timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def add_scan(scan_id: str, image_url: str, disease: str, confidence: float) -> None:
    """Add a new scan to the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO plant_scans (id, image_url, disease, confidence, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (scan_id, image_url, disease, confidence, datetime.datetime.now())
    )
    
    conn.commit()
    cur.close()
    conn.close()

def get_all_scans() -> List[Dict[str, Any]]:
    """Get all scans from the database."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT id, image_url as image, disease, confidence, timestamp FROM plant_scans ORDER BY timestamp DESC")
    scans = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return scans

def get_scan_by_id(scan_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific scan by its ID."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT id, image_url as image, disease, confidence, timestamp FROM plant_scans WHERE id = %s", (scan_id,))
    scan = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return scan
