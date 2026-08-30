from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from anomaly.models import AnomalyResult, DetectionHistory


class ReliabilityTests(TestCase):
    """Repeated read/authorization checks for stable service behavior."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="reliability_user", password="StrongPass123!"
        )
        self.api_client = APIClient()
        self.api_client.force_authenticate(self.user)
        for index in range(3):
            AnomalyResult.objects.create(
                user=self.user,
                file_name=f"dataset-{index}.csv",
                total=10,
                normal=9,
                anomalies=1,
            )
            DetectionHistory.objects.create(
                user=self.user,
                filename=f"dataset-{index}.csv",
                model_name="isolation_forest",
                scaler_type="standard",
                contamination=0.05,
                total_records=10,
                anomaly_count=1,
            )

    def test_repeated_result_reads_are_consistent(self):
        first = self.api_client.get("/api/anomaly/results/")
        second = self.api_client.get("/api/anomaly/results/")
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json(), second.json())

    def test_repeated_history_reads_are_consistent(self):
        first = self.api_client.get("/api/anomaly/history/")
        second = self.api_client.get("/api/anomaly/history/")
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json(), second.json())

    def test_repeated_protected_requests_do_not_mutate_results(self):
        before = AnomalyResult.objects.count()
        for _ in range(5):
            response = self.api_client.get("/api/anomaly/results/")
            self.assertEqual(response.status_code, 200)
        self.assertEqual(AnomalyResult.objects.count(), before)
