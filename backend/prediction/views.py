
import os
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings

from .models import PlantScan
from .serializers import (
    PlantScanSerializer, 
    PredictionRequestSerializer, 
    PredictionResponseSerializer,
    TreatmentRequestSerializer,
    PlantInfoRequestSerializer
)
from .ml_model import predict_leaf_disease

class PredictAPIView(APIView):
    """API view for plant disease prediction."""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        serializer = PredictionRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            
            # Save the uploaded image temporarily
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', image_file.name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            with open(temp_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            try:
                # Make prediction
                prediction_result = predict_leaf_disease(temp_path)
                
                # Check if there was an error
                if 'error' in prediction_result:
                    return Response({'error': prediction_result['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Save scan to database
                plant_scan = PlantScan(
                    image=image_file,
                    disease=prediction_result['disease'],
                    confidence=prediction_result['confidence']
                )
                plant_scan.save()
                
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
                
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                return Response(response_data, status=status.HTTP_200_OK)
                
            except Exception as e:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TreatmentAPIView(APIView):
    """API view for retrieving treatment for a specific disease."""
    
    def get(self, request, disease, *args, **kwargs):
        # Demo treatment data
        treatments = {
            "Apple___Apple_scab": "Apply fungicides early in the growing season. Remove and destroy infected leaves. Use resistant varieties if possible.",
            "Tomato___Early_blight": "Remove infected leaves. Apply fungicides. Mulch around plants. Avoid overhead watering. Rotate crops."
        }
        
        treatment = treatments.get(disease, "No specific treatment found for this disease.")
        
        return Response({
            "disease": disease,
            "treatment": treatment,
            "steps": [
                "Remove all infected leaves and dispose of them properly.",
                "Apply appropriate fungicide according to label instructions.",
                "Improve air circulation around plants.",
                "Water at the base of plants to avoid wetting foliage.",
                "Rotate crops in future growing seasons."
            ]
        }, status=status.HTTP_200_OK)

class PlantInfoAPIView(APIView):
    """API view for retrieving plant information."""
    
    def get(self, request, plant_name, *args, **kwargs):
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
                "temperature": "General care information not available"
            },
            "preventionTips": [
                "Use disease-resistant varieties",
                "Practice crop rotation",
                "Maintain good air circulation",
                "Water properly, avoiding wet foliage",
                "Monitor regularly for early detection of issues"
            ]
        })
        
        return Response(plant_info, status=status.HTTP_200_OK)

class HistoryAPIView(APIView):
    """API view for retrieving scan history."""
    
    def get(self, request, *args, **kwargs):
        scans = PlantScan.objects.all()
        serializer = PlantScanSerializer(scans, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class HistoryDetailAPIView(APIView):
    """API view for retrieving a specific scan."""
    
    def get(self, request, scan_id, *args, **kwargs):
        try:
            scan = PlantScan.objects.get(id=scan_id)
            serializer = PlantScanSerializer(scan, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PlantScan.DoesNotExist:
            return Response({"error": "Scan not found"}, status=status.HTTP_404_NOT_FOUND)
