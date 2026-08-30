from unittest.mock import patch

import pandas as pd
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class AcceptanceWorkflowTests(TestCase):
    """Acceptance-level checks for the main ADS user journeys."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="acceptance_user", password="StrongPass123!"
        )
        self.api_client = APIClient()
        self.csv = SimpleUploadedFile(
            "acceptance.csv",
            b"feature_1,feature_2\n1,2\n2,3\n3,100\n",
            content_type="text/csv",
        )

    def fake_detection(self):
        return {
            "result_df": pd.DataFrame({"feature_1": [1.0], "result": ["Normal"]}),
            "total": 1,
            "anomalies": 0,
            "normal": 1,
            "scatter_data": [],
            "normal_score_data": [0.1],
            "anomaly_score_data": [],
            "score_data": [0.1],
            "saved_path": "/tmp/acceptance-result.csv",
            "evaluation": None,
        }

    def test_login_home_and_logout_acceptance_flow(self):
        response = self.client.post(
            reverse("login"),
            {"username": "acceptance_user", "password": "StrongPass123!"},
        )
        self.assertRedirects(response, reverse("home"))

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    @patch("anomaly.api.views.AnomalyService.process_anomalies")
    def test_authenticated_anomaly_detection_acceptance_flow(self, process):
        process.return_value = self.fake_detection()
        self.api_client.force_authenticate(self.user)

        response = self.api_client.post(
            "/api/anomaly/analyze/",
            {
                "file": self.csv,
                "model_name": "isolation_forest",
                "scaler_type": "standard",
                "contamination": "0.05",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["data"]["filename"], "acceptance.csv")
        process.assert_called_once()

    def test_protected_home_requires_authentication(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])
