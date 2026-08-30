from unittest.mock import patch

import pandas as pd
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from anomaly.models import AnomalyResult, DetectionHistory


class RegressionTests(TestCase):
    """High-value regression checks for previously critical application flows."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="regression_user", password="StrongPass123!"
        )
        self.other = User.objects.create_user(
            username="regression_other", password="StrongPass123!"
        )
        self.api_client = APIClient()
        self.api_client.force_authenticate(self.user)

    def detection_result(self):
        return {
            "result_df": pd.DataFrame({"amount": [1.0], "result": ["Normal"]}),
            "total": 1,
            "anomalies": 0,
            "normal": 1,
            "scatter_data": [],
            "normal_score_data": [0.1],
            "anomaly_score_data": [],
            "score_data": [0.1],
            "saved_path": "/tmp/regression-result.csv",
            "evaluation": None,
        }

    def test_login_regression(self):
        self.client.logout()
        response = self.client.post(
            reverse("login"),
            {"username": "regression_user", "password": "StrongPass123!"},
        )
        self.assertRedirects(response, reverse("home"))

    def test_anomaly_results_remain_user_scoped(self):
        AnomalyResult.objects.create(
            user=self.user, file_name="mine.csv", total=1, normal=1, anomalies=0
        )
        AnomalyResult.objects.create(
            user=self.other, file_name="other.csv", total=1, normal=0, anomalies=1
        )
        response = self.api_client.get("/api/anomaly/results/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        results = payload.get("results", payload) if isinstance(payload, dict) else payload
        self.assertEqual([r["file_name"] for r in results], ["mine.csv"])

    def test_history_clear_does_not_delete_other_user_records(self):
        mine = DetectionHistory.objects.create(
            user=self.user,
            filename="mine.csv",
            model_name="isolation_forest",
            scaler_type="standard",
            contamination=0.05,
            total_records=1,
            anomaly_count=0,
        )
        other = DetectionHistory.objects.create(
            user=self.other,
            filename="other.csv",
            model_name="lof",
            scaler_type="standard",
            contamination=0.05,
            total_records=1,
            anomaly_count=1,
        )
        response = self.api_client.delete("/api/anomaly/history/clear/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(DetectionHistory.objects.filter(pk=mine.pk).exists())
        self.assertTrue(DetectionHistory.objects.filter(pk=other.pk).exists())

    def test_invalid_anomaly_parameters_still_return_400(self):
        upload = SimpleUploadedFile(
            "regression.csv", b"amount,frequency\n1,2\n2,3\n", content_type="text/csv"
        )
        response = self.api_client.post(
            "/api/anomaly/analyze/",
            {
                "file": upload,
                "model_name": "isolation_forest",
                "scaler_type": "standard",
                "contamination": "0.5",
            },
        )
        self.assertEqual(response.status_code, 400)

    @patch("anomaly.api.views.AnomalyService.process_anomalies")
    def test_core_detection_response_contract_remains_stable(self, process):
        process.return_value = self.detection_result()
        upload = SimpleUploadedFile(
            "regression.csv", b"amount,frequency\n1,2\n2,3\n", content_type="text/csv"
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
        data = response.json()["data"]
        for key in ("filename", "total", "anomalies", "normal"):
            self.assertIn(key, data)
