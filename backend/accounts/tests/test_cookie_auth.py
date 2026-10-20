from django.test import Client, TestCase
from accounts.models import User

class CookieAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("cookie@test.mx", "demo1234", role=User.Role.PATIENT)
        self.client = Client(enforce_csrf_checks=True)

    def test_login_scopes_tokens_for_the_api_and_refresh_requires_csrf(self):
        csrf = self.client.get("/api/v1/auth/csrf").json()["csrfToken"]
        login = self.client.post("/api/v1/auth/login", {"email": self.user.email, "password": "demo1234"})
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.cookies["access_token"]["path"], "/api/v1/")
        self.assertEqual(login.cookies["refresh_token"]["path"], "/api/v1/")
        self.assertEqual(self.client.post("/api/v1/auth/refresh").status_code, 403)
        self.assertEqual(self.client.post("/api/v1/auth/refresh", HTTP_X_CSRFTOKEN=csrf).status_code, 200)
