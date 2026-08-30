from rest_framework import serializers
from anomaly.models import AnomalyResult, DetectionHistory


class FileUploadSerializer(serializers.Serializer):

    file = serializers.FileField()


class AnomalyResultSerializer(serializers.ModelSerializer):

    class Meta:

        model = AnomalyResult

        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]

class DetectionHistorySerializer(serializers.ModelSerializer):

    class Meta:

        model = DetectionHistory

        fields = "__all__"
        read_only_fields = [
            "id", "user", "created_at", "filename", "model_name", "scaler_type",
            "contamination", "total_records", "anomaly_count", "dataset_type",
            "target_column", "accuracy", "precision", "recall", "f1_score", "model_path",
        ]