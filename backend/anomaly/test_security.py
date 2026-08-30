from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from anomaly.models import AnomalyResult, DetectionHistory


class AnomalyResourceSecurityTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", password="StrongPass123!"
        )
        self.attacker = User.objects.create_user(
            username="attacker", password="StrongPass123!"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.attacker)

    def test_anomaly_result_is_user_scoped(self):
        result = AnomalyResult.objects.create(
            user=self.owner, file_name="owner.csv",
            total=3, normal=2, anomalies=1,
        )
        self.assertEqual(
            self.client.get(f"/api/anomaly/results/{result.pk}/").status_code,
            404,
        )

    def test_detection_history_is_user_scoped(self):
        history = DetectionHistory.objects.create(
            user=self.owner,
            filename="owner.csv",
            model_name="isolation_forest",
            scaler_type="standard",
            contamination=0.05,
            total_records=3,
            anomaly_count=1,
        )
        response = self.client.get(f"/api/anomaly/history/{history.pk}/")
        self.assertEqual(response.status_code, 404)
