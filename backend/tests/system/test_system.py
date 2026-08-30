from unittest.mock import patch

import pandas as pd
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from anomaly.models import AnomalyResult, DetectionHistory


class SystemTests(TestCase):
    """Cross-layer system checks covering UI authentication and API persistence."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="system_user", password="StrongPass123!"
        )

    def fake_detection(self):
        return {
            "result_df": pd.DataFrame({"feature": [1.0], "result": ["Normal"]}),
            "total": 1,
            "anomalies": 0,
            "normal": 1,
            "scatter_data": [],
            "normal_score_data": [0.1],
            "anomaly_score_data": [],
            "score_data": [0.1],
            "saved_path": "/tmp/system-result.csv",
            "evaluation": None,
        }

    @patch("anomaly.services.anomaly_service.detect_anomalies")
    def test_login_to_api_detection_to_history_system_flow(self, detect):
        detect.return_value = {
            "df": pd.DataFrame({
                "feature": [1.0, 2.0, 3.0],
                "anomaly_score": [0.1, 0.2, 0.3],
                "pca_x": [0.0, 0.1, 0.2],
                "pca_y": [0.0, 0.1, 0.2],
                "result": ["Normal", "Normal", "Normal"],
            }),
            "model_path": None,
        }
        self.api_client = APIClient()
        self.api_client.force_authenticate(self.user)
        login = self.client.post(
            reverse("login"),
            {"username": "system_user", "password": "StrongPass123!"},
        )
        self.assertRedirects(login, reverse("home"))

        upload = SimpleUploadedFile(
            "system.csv", b"feature\n1\n2\n3\n", content_type="text/csv"
        )
        response = self.api_client.post(
            "/api/anomaly/analyze/",
            {
                "file": upload,
                "model_name": "isolation_forest",
                "scaler_type": "standard",
                "contamination": "0.05",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AnomalyResult.objects.filter(user=self.user).count(), 1)
        self.assertEqual(DetectionHistory.objects.filter(user=self.user).count(), 1)

        history = self.api_client.get("/api/anomaly/history/")
        self.assertEqual(history.status_code, 200)
        history_payload = history.json()
        history_results = history_payload.get("results", history_payload) if isinstance(history_payload, dict) else history_payload
        self.assertEqual(history_results[0]["filename"], "system.csv")
