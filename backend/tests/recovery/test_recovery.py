from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class RecoveryTests(TestCase):
    """Checks that common invalid/interrupted flows recover safely."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="recovery_user", password="StrongPass123!"
        )
        self.api_client = APIClient()
        self.api_client.force_authenticate(self.user)
        self.client.force_login(self.user)

    def test_invalid_csv_upload_returns_controlled_error_page(self):
        bad_file = SimpleUploadedFile(
            "not-a-csv.txt", b"this is not csv", content_type="text/plain"
        )
        response = self.client.post(
            reverse("home"), {"file": bad_file, "model_name": "isolation_forest"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["error"], "Only CSV files are allowed.")

    def test_missing_anomaly_export_session_returns_controlled_response(self):
        response = self.api_client.get("/api/anomaly/download/csv/")
        self.assertIn(response.status_code, [200, 404])

    def test_missing_classification_result_returns_404(self):
        response = self.api_client.get("/api/classification/results/999999/")
        self.assertEqual(response.status_code, 404)

    def test_expired_session_returns_to_login_for_protected_page(self):
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])
