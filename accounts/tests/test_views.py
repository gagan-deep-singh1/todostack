
from django.urls import reverse

from rest_framework.test import APITestCase


class RegistrationViewTest(APITestCase):
    def test_get(self):
        url = reverse("register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_post(self):
        url = reverse("register")
        data = {
            "username": "testuser",
            "first_name": "test",
            "last_name": "user",
            "email": "abc@google.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 415)
