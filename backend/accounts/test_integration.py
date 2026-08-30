from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationIntegrationTests(TestCase):
    def test_login_logout_workflow(self):
        User.objects.create_user(username="integration", password="StrongPass123!")
        response = self.client.post(
            reverse("login"),
            {"username": "integration", "password": "StrongPass123!"},
        )
        self.assertEqual(response.status_code, 302)
        logout = self.client.post(reverse("logout"))
        self.assertIn(logout.status_code, (200, 302))

    def test_invalid_credentials_stay_on_login(self):
        response = self.client.post(
            reverse("login"),
            {"username": "missing", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials")
