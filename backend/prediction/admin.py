
from django.contrib import admin
from .models import PlantScan

@admin.register(PlantScan)
class PlantScanAdmin(admin.ModelAdmin):
    list_display = ('disease', 'confidence', 'timestamp')
    list_filter = ('disease', 'timestamp')
    search_fields = ('disease',)
    readonly_fields = ('id', 'confidence', 'timestamp')
