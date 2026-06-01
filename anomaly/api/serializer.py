from rest_framework import serializers
from anomaly.models import AnomalyResult


class FileUploadSerializer(serializers.Serializer):

    file = serializers.FileField()


class AnomalyResultSerializer(serializers.ModelSerializer):

    class Meta:

        model = AnomalyResult

        fields = "__all__"