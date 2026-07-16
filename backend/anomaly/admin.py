from django.contrib import admin
from .models import DetectionHistory

@admin.register(DetectionHistory)
class DetectionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'filename',
        'model_name',
        'scaler_type',
        'contamination',
        'precision',
        'recall',
        'f1_score',
        'anomaly_count',
        'created_at'
    )

    search_fields = ('filename', 'model_name')
    list_filter = ('model_name',)
