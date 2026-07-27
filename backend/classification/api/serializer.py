from rest_framework import serializers

from classification.models import ClassificationResult


class FileUploadSerializer(serializers.Serializer):

    file = serializers.FileField()

    def validate_file(self, value):

        if not value.name.endswith(".csv"):
            raise serializers.ValidationError(
                "Only CSV files are allowed."
            )

        return value


class ClassificationResultSerializer(serializers.ModelSerializer):

    class Meta:

        model = ClassificationResult

        fields = [
            "id",
            "user",
            "file_name",
            "model_name",
            "target_column",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "roc_auc",
            "confusion_matrix",
            "summary",
            "dataset_summary",
            "confusion_matrix_chart",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]