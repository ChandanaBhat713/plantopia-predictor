
from django.db import models
import uuid
import os

def get_image_path(instance, filename):
    """Generate a unique path for uploaded images."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('plant_images', filename)

class PlantScan(models.Model):
    """Model to store plant disease scan results."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_image_path)
    disease = models.CharField(max_length=255)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.disease} - {self.confidence:.2f} - {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
