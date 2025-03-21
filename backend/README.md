
# Plant Disease Detection FastAPI Backend with TensorFlow Serving

This is a FastAPI backend for the Plant Disease Detection application. It uses TensorFlow Serving to serve a CNN model that predicts plant diseases from uploaded images.

## Setup Instructions

### 1. Install requirements:
```
pip install -r requirements.txt
```

### 2. Set up TensorFlow Serving:

#### Option 1: Using Docker (Recommended)
```bash
# Pull the TensorFlow Serving Docker image
docker pull tensorflow/serving

# Run TensorFlow Serving container
docker run -p 8501:8501 \
  --mount type=bind,source=/path/to/models/leaf_disease_model,target=/models/leaf_disease_model \
  -e MODEL_NAME=leaf_disease_model \
  tensorflow/serving
```

#### Option 2: Install TensorFlow Serving directly
Follow the [official TensorFlow Serving installation guide](https://www.tensorflow.org/tfx/serving/setup).

Then run:
```bash
tensorflow_model_server --rest_api_port=8501 \
  --model_name=leaf_disease_model \
  --model_base_path=/path/to/models/leaf_disease_model
```

### 3. Prepare your model:
Convert your Keras model to TensorFlow SavedModel format:

```python
import tensorflow as tf

# Load your Keras model
model = tf.keras.models.load_model('leaf_disease_model.keras')

# Save as TensorFlow SavedModel format
tf.saved_model.save(model, '/path/to/models/leaf_disease_model/1/')
```

The version number directory (1/) is required by TensorFlow Serving.

### 4. Run the FastAPI server:
```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000/api/`

### 5. Environment Variables (Optional):
You can configure the following environment variables:
- `TF_SERVING_HOST`: Hostname for TensorFlow Serving (default: localhost)
- `TF_SERVING_PORT`: Port for TensorFlow Serving (default: 8501)
- `TF_SERVING_MODEL_NAME`: Name of the model in TensorFlow Serving (default: leaf_disease_model)

### 6. Automatic API Documentation:
FastAPI provides automatic API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- **POST /api/predict** - Upload an image for disease prediction
- **GET /api/treatment/{disease}** - Get treatment for a specific disease
- **GET /api/plant-info/{plant_name}** - Get information about a specific plant
- **GET /api/history** - Get scan history
- **GET /api/history/{scan_id}** - Get details for a specific scan

## Model Information

The API uses TensorFlow Serving to serve a CNN model for plant disease detection. Make sure to set up TensorFlow Serving with your model correctly.
