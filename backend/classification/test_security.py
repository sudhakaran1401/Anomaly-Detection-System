from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from classification.models import ClassificationResult


class ClassificationSecurityTests(TestCase):
    def test_user_cannot_read_another_users_classification_result(self):
        owner = User.objects.create_user(username="class-owner", password="StrongPass123!")
        attacker = User.objects.create_user(username="class-attacker", password="StrongPass123!")
        result = ClassificationResult.objects.create(
            user=owner,
            file_name="private.csv",
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
        client = APIClient()
        client.force_authenticate(attacker)
        response = client.get(f"/api/classification/results/{result.pk}/")
        self.assertEqual(response.status_code, 404)
