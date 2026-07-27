from django.db import models
from django.contrib.auth.models import User


class ClassificationResult(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="classification_results",
    )

    file_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    model_name = models.CharField(
        max_length=100,
    )

    target_column = models.CharField(
        max_length=100,
        blank=True,
    )

    accuracy = models.FloatField()

    precision = models.FloatField()

    recall = models.FloatField()

    f1_score = models.FloatField()

    roc_auc = models.FloatField( null=True, blank=True, )

    confusion_matrix = models.JSONField()

    summary = models.JSONField()

    dataset_summary = models.JSONField()

    confusion_matrix_chart = models.CharField(
        max_length=255,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.file_name