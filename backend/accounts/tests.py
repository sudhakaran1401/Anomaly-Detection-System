from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="webuser", password="StrongPass123!")

    def test_login_with_valid_credentials_redirects_to_upload(self):
        response = self.client.post(
            reverse("login"),
            {"username": "webuser", "password": "StrongPass123!"},
        )
        self.assertRedirects(response, reverse("home"))

    def test_login_with_invalid_credentials_stays_on_login(self):
        response = self.client.post(
            reverse("login"),
            {"username": "webuser", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials")

    def test_upload_page_requires_login(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_logout_ends_session(self):
        self.client.login(username="webuser", password="StrongPass123!")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

class JWTIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jwtuser", password="StrongPass123!")

    def test_token_endpoint_returns_access_and_refresh_tokens(self):
        response = self.client.post(
            "/api/token/",
            {"username": "jwtuser", "password": "StrongPass123!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_token_endpoint_rejects_invalid_credentials(self):
        response = self.client.post(
            "/api/token/",
            {"username": "jwtuser", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 401)
