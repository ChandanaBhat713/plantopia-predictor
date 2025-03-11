
from rest_framework import serializers
from .models import PlantScan

class PlantScanSerializer(serializers.ModelSerializer):
    """Serializer for the PlantScan model."""
    imageUrl = serializers.SerializerMethodField()
    
    class Meta:
        model = PlantScan
        fields = ['id', 'disease', 'confidence', 'timestamp', 'imageUrl']
    
    def get_imageUrl(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url') and request is not None:
            return request.build_absolute_uri(obj.image.url)
        return None

class PredictionRequestSerializer(serializers.Serializer):
    """Serializer for prediction requests."""
    image = serializers.ImageField()

class PredictionResponseSerializer(serializers.Serializer):
    """Serializer for prediction responses."""
    disease = serializers.CharField()
    confidence = serializers.FloatField()
    description = serializers.CharField()
    treatment = serializers.CharField()
    sources = serializers.ListField(child=serializers.DictField(), required=False)

class TreatmentRequestSerializer(serializers.Serializer):
    """Serializer for treatment requests."""
    disease = serializers.CharField()

class PlantInfoRequestSerializer(serializers.Serializer):
    """Serializer for plant info requests."""
    plantName = serializers.CharField()
