
from django.urls import path
from .views import (
    PredictAPIView, 
    TreatmentAPIView, 
    PlantInfoAPIView,
    HistoryAPIView,
    HistoryDetailAPIView
)

urlpatterns = [
    path('predict', PredictAPIView.as_view(), name='predict'),
    path('treatment/<str:disease>', TreatmentAPIView.as_view(), name='treatment'),
    path('plant-info/<str:plant_name>', PlantInfoAPIView.as_view(), name='plant-info'),
    path('history', HistoryAPIView.as_view(), name='history'),
    path('history/<str:scan_id>', HistoryDetailAPIView.as_view(), name='history-detail'),
]
