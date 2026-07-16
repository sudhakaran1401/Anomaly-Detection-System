from django.db import models
from django.contrib.auth.models import User


class AnomalyResult(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    file_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    total = models.IntegerField()
    normal = models.IntegerField()
    anomalies = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.file_name


class UploadedDataset(models.Model):

    file_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    columns = models.JSONField()
    results = models.JSONField()

    total = models.IntegerField(default=0)
    anomalies = models.IntegerField(default=0)
    normal = models.IntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.file_name


class DetectionHistory(models.Model):

    filename = models.CharField(
        max_length=255,
        db_index=True,
    )

    model_name = models.CharField(
        max_length=100,
        db_index=True,
    )

    scaler_type = models.CharField(max_length=100)

    contamination = models.FloatField(
        null=True,
        blank=True,
    )

    total_records = models.IntegerField()
    anomaly_count = models.IntegerField()

    dataset_type = models.CharField(
        max_length=20,
        default="unlabelled",
    )

    target_column = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    accuracy = models.FloatField(
        null=True,
        blank=True,
    )

    precision = models.FloatField(
        null=True,
        blank=True,
    )

    recall = models.FloatField(
        null=True,
        blank=True,
    )

    f1_score = models.FloatField(
        null=True,
        blank=True,
    )

    model_path = models.CharField(
        max_length=500,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.filename} - {self.model_name}"


class TrainedModel(models.Model):

    MODEL_CHOICES = [
        ("isolation_forest", "Isolation Forest"),
        ("lof", "Local Outlier Factor"),
        ("one_class_svm", "One Class SVM"),
        ("dbscan", "DBSCAN"),
    ]

    model_name = models.CharField(
        max_length=100,
        db_index=True,
    )

    algorithm = models.CharField(
        max_length=50,
        choices=MODEL_CHOICES,
    )

    dataset_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    precision = models.FloatField(
        null=True,
        blank=True,
    )

    recall = models.FloatField(
        null=True,
        blank=True,
    )

    f1_score = models.FloatField(
        null=True,
        blank=True,
    )

    anomaly_count = models.IntegerField(default=0)

    model_path = models.CharField(max_length=500)

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.model_name