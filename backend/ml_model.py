
import os
import numpy as np
import time
import json
import requests
from PIL import Image
import logging
from typing import Dict, Any, Optional

from app.config import (
    TF_SERVING_URL, 
    TF_SERVING_HOST, 
    TF_SERVING_PORT, 
    TF_SERVING_MODEL_NAME,
    DISEASE_CLASSES,
)

logger = logging.getLogger(__name__)

# Disease descriptions moved to config.py
from app.data.descriptions import DISEASE_DESCRIPTIONS, DISEASE_TREATMENTS

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
