from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from classification.models import ClassificationResult


class ClassificationIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="classification-integration",
            password="StrongPass123!",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_classification_results_are_retrievable_for_owner(self):
        ClassificationResult.objects.create(
            user=self.user,
            file_name="labelled.csv",
            model_name="random_forest",
            target_column="Target",
            accuracy=1,
            precision=1,
            recall=1,
            f1_score=1,
            confusion_matrix={},
            summary={},
            dataset_summary={},
            confusion_matrix_chart="chart.png",
        )
        response = self.client.get("/api/classification/results/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
