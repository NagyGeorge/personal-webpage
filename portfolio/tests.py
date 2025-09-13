from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project


class PortfolioModelTest(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project.",
            link="https://example.com",
            featured=True,
        )
        self.assertEqual(project.title, "Test Project")
        self.assertTrue(project.featured)


class PortfolioAPITest(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Test Project",
            description="This is a test project.",
            link="https://example.com",
            featured=True,
        )

    def test_get_projects(self):
        url = "/api/portfolio/projects/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_project_detail(self):
        url = f"/api/portfolio/projects/{self.project.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Project")
