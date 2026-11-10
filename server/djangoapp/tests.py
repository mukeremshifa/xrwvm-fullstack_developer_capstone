import json

from django.contrib.auth.models import User
from django.test import TestCase


class CapstoneApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="TestPass123!", first_name="Test", last_name="User"
        )

    def test_login_and_logout(self):
        response = self.client.post(
            "/djangoapp/login",
            data=json.dumps({"userName": "testuser", "password": "TestPass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Authenticated")
        self.assertEqual(self.client.get("/djangoapp/logout").status_code, 200)

    def test_dealer_endpoints(self):
        self.assertEqual(self.client.get("/djangoapp/get_dealers").json()["status"], 200)
        dealers = self.client.get("/djangoapp/get_dealers/Kansas").json()["dealers"]
        self.assertTrue(all(dealer["state"] == "Kansas" for dealer in dealers))
        self.assertEqual(self.client.get("/djangoapp/dealer/1").json()["dealer"][0]["id"], 1)

    def test_car_and_sentiment_endpoints(self):
        self.assertTrue(self.client.get("/djangoapp/get_cars").json()["CarModels"])
        self.assertEqual(
            self.client.get("/djangoapp/analyze/Fantastic%20services").json()["sentiment"],
            "positive",
        )
