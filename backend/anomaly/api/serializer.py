from rest_framework import serializers
from anomaly.models import AnomalyResult, DetectionHistory


class FileUploadSerializer(serializers.Serializer):

    file = serializers.FileField()


class AnomalyResultSerializer(serializers.ModelSerializer):

    class Meta:

        model = AnomalyResult

        fields = "__all__"

class DetectionHistorySerializer(serializers.ModelSerializer):

    class Meta:

        model = DetectionHistory

        fields = "__all__"