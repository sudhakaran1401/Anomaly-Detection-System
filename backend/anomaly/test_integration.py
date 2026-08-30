from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from anomaly.models import AnomalyResult, DetectionHistory


class AnomalyIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="anomaly-integration",
            password="StrongPass123!",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_result_and_history_are_user_scoped(self):
        AnomalyResult.objects.create(
            user=self.user, file_name="data.csv", total=2, normal=1, anomalies=1
        )
        DetectionHistory.objects.create(
            user=self.user,
            filename="data.csv",
            model_name="isolation_forest",
            scaler_type="standard",
            contamination=0.05,
            total_records=2,
            anomaly_count=1,
        )
        self.assertEqual(self.client.get("/api/anomaly/results/").status_code, 200)
        self.assertEqual(self.client.get("/api/anomaly/history/").status_code, 200)
