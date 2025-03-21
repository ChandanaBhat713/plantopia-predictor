
import os
import numpy as np
import time
import json
import requests
from PIL import Image
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Configuration for TensorFlow Serving
TF_SERVING_HOST = os.environ.get("TF_SERVING_HOST", "localhost")
TF_SERVING_PORT = os.environ.get("TF_SERVING_PORT", "8501")
TF_SERVING_MODEL_NAME = os.environ.get("TF_SERVING_MODEL_NAME", "leaf_disease_model")
TF_SERVING_URL = f"http://{TF_SERVING_HOST}:{TF_SERVING_PORT}/v1/models/{TF_SERVING_MODEL_NAME}:predict"

# Disease classes and descriptions (same as before)
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
    # Add more disease classes as per your model
]

DISEASE_DESCRIPTIONS = {
    "Apple___Apple_scab": "Apple scab is a fungal disease caused by Venturia inaequalis that affects apple trees.",
    "Apple___Black_rot": "Black rot is a fungal disease caused by Botryosphaeria obtusa affecting apples.",
    "Apple___Cedar_apple_rust": "Cedar apple rust is a fungal disease caused by Gymnosporangium juniperi-virginianae.",
    "Apple___healthy": "This is a healthy apple leaf with no signs of disease.",
    "Tomato___Early_blight": "Early blight is a fungal disease caused by Alternaria solani affecting tomatoes.",
    "Tomato___Late_blight": "Late blight is a devastating disease caused by Phytophthora infestans.",
    "Tomato___Leaf_Mold": "Leaf mold is caused by the fungus Passalora fulva, prevalent in humid conditions.",
    "Tomato___Septoria_leaf_spot": "Septoria leaf spot is a fungal disease that causes small, circular spots.",
    "Tomato___Spider_mites": "Spider mites are tiny pests that cause stippling and yellowing of tomato leaves.",
    "Tomato___Target_Spot": "Target spot is caused by the fungus Corynespora cassiicola.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "TYLCV is a viral disease transmitted by whiteflies.",
    "Tomato___Tomato_mosaic_virus": "ToMV is a viral disease causing mottled leaves and stunted growth.",
    "Tomato___healthy": "This is a healthy tomato leaf with no signs of disease."
    # Add more descriptions as needed
}

DISEASE_TREATMENTS = {
    "Apple___Apple_scab": "Apply fungicides early in the growing season. Remove and destroy infected leaves. Use resistant varieties if possible. Improve air circulation by proper pruning.",
    "Apple___Black_rot": "Remove and destroy infected plant parts. Apply fungicides during the growing season. Prune to improve air circulation. Control insects that create wounds for infection.",
    "Apple___Cedar_apple_rust": "Remove nearby cedar or juniper trees if possible. Apply fungicides in spring. Use resistant apple varieties. Keep the orchard clean of debris.",
    "Apple___healthy": "Continue good cultural practices: proper watering, fertilization, and regular monitoring for early detection of issues.",
    "Tomato___Early_blight": "Remove infected leaves. Apply fungicides. Mulch around plants. Avoid overhead watering. Rotate crops. Use resistant varieties if available.",
    "Tomato___Late_blight": "Apply fungicides preventatively. Remove infected plants immediately. Avoid overhead irrigation. Ensure good air circulation. Plant resistant varieties.",
    "Tomato___Leaf_Mold": "Improve air circulation. Reduce humidity. Apply fungicides. Remove infected leaves. Avoid overhead watering. Use resistant varieties.",
    "Tomato___Septoria_leaf_spot": "Remove infected leaves. Apply fungicides. Avoid overhead watering. Use mulch to prevent soil splash. Rotate crops. Clean up debris in fall.",
    "Tomato___Spider_mites": "Spray plants with water to dislodge mites. Apply insecticidal soap or neem oil. Introduce predatory mites. Maintain proper humidity levels.",
    "Tomato___Target_Spot": "Remove infected leaves. Apply fungicides. Avoid overhead watering. Ensure proper plant spacing for air circulation. Rotate crops.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Control whitefly populations. Remove and destroy infected plants. Use reflective mulches. Plant resistant varieties. Use physical barriers like row covers.",
    "Tomato___Tomato_mosaic_virus": "Remove and destroy infected plants. Control aphids. Wash hands and tools after handling infected plants. Plant resistant varieties. Avoid working in wet gardens.",
    "Tomato___healthy": "Maintain good cultural practices: proper watering, fertilization, and regular monitoring for early detection of issues."
    # Add more treatments as needed
}

def check_tf_serving_status() -> bool:
    """Check if TensorFlow Serving is available."""
    try:
        response = requests.get(f"http://{TF_SERVING_HOST}:{TF_SERVING_PORT}/v1/models/{TF_SERVING_MODEL_NAME}")
        if response.status_code == 200:
            logger.info("TensorFlow Serving is available")
            return True
        else:
            logger.error(f"TensorFlow Serving returned status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error connecting to TensorFlow Serving: {str(e)}")
        return False

def load_model_into_memory():
    """Check if TensorFlow Serving is available."""
    if check_tf_serving_status():
        logger.info("TensorFlow Serving is ready to handle predictions")
    else:
        logger.warning("TensorFlow Serving is not available. Please start TensorFlow Serving with the appropriate model.")
        logger.warning("Example command: tensorflow_model_server --rest_api_port=8501 --model_name=leaf_disease_model --model_base_path=/path/to/models/leaf_disease_model")

def preprocess_image(image_path):
    """Loads and preprocesses an image for model prediction."""
    try:
        img = Image.open(image_path).convert('RGB')  # Ensure 3-channel RGB
        img = img.resize((224, 224))  # Resize to model's input size
        img_array = np.array(img) / 255.0  # Normalize pixel values (0-1)
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise

def predict_leaf_disease(image_path):
    """Runs inference using TensorFlow Serving and returns the predicted class and metadata."""
    try:
        # Preprocess the image
        img_array = preprocess_image(image_path)
        
        # Create the request payload
        payload = {
            "signature_name": "serving_default",
            "instances": [img_array.tolist()]
        }
        
        # Measure inference time
        start_time = time.time()
        
        # Make request to TensorFlow Serving
        response = requests.post(TF_SERVING_URL, json=payload)
        
        if response.status_code != 200:
            logger.error(f"Error from TensorFlow Serving: {response.text}")
            return {
                "error": f"TensorFlow Serving returned status code {response.status_code}",
                "disease": "Error",
                "confidence": 0.0,
                "description": "An error occurred during prediction",
                "treatment": ""
            }
        
        end_time = time.time()
        
        # Parse the response
        predictions = response.json()["predictions"][0]
        
        # Get the predicted class
        predicted_class_index = np.argmax(predictions)
        confidence_score = float(np.max(predictions))  # Convert to Python float for JSON serialization
        
        # Get class name, description, and treatment
        if predicted_class_index < len(DISEASE_CLASSES):
            disease_name = DISEASE_CLASSES[predicted_class_index]
            description = DISEASE_DESCRIPTIONS.get(disease_name, "No description available")
            treatment = DISEASE_TREATMENTS.get(disease_name, "No treatment information available")
        else:
            disease_name = f"Unknown (Class {predicted_class_index})"
            description = "No description available for this class"
            treatment = "No treatment information available"
        
        logger.info(f"Prediction: {disease_name}, Confidence: {confidence_score:.4f}")
        logger.info(f"Inference Time: {end_time - start_time:.6f} seconds")
        
        # Return a dictionary with the prediction results
        return {
            "disease": disease_name,
            "confidence": confidence_score,
            "description": description,
            "treatment": treatment,
            "inference_time": end_time - start_time
        }
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        return {
            "error": str(e),
            "disease": "Error",
            "confidence": 0.0,
            "description": "An error occurred during prediction",
            "treatment": ""
        }
