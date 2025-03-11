
# Plant Disease Detection Backend API

This is a Django REST API backend for the Plant Disease Detection application. It uses a CNN model to predict plant diseases from uploaded images.

## Setup Instructions

### 1. Install requirements:
```
pip install -r requirements.txt
```

### 2. Add your CNN model:
Place your trained CNN model file at:
```
prediction/ml_models/leaf_disease_model.keras
```

### 3. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (optional):
```
python manage.py createsuperuser
```

### 5. Run the development server:
```
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

- **POST /api/predict** - Upload an image for disease prediction
- **GET /api/treatment/{disease}** - Get treatment for a specific disease
- **GET /api/plant-info/{plant_name}** - Get information about a specific plant
- **GET /api/history** - Get scan history
- **GET /api/history/{scan_id}** - Get details for a specific scan

## Model Information

The API uses a CNN model for plant disease detection. Make sure to place your trained model file at the correct location.
