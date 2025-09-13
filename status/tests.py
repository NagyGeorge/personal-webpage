from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class StatusViewTest(APITestCase):
    def test_healthz_endpoint(self):
        url = reverse("healthz")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("status", response.data)
        self.assertIn("checks", response.data)
