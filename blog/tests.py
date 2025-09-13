from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post, Tag


class BlogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.tag = Tag.objects.create(name="Python")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Python")
        self.assertEqual(self.tag.slug, "python")

    def test_post_creation(self):
        post = Post.objects.create(
            title="Test Post",
            body="This is a test post.",
            author=self.user,
            published=True,
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.slug, "test-post")
        self.assertTrue(post.published)


class BlogAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            body="This is a test post.",
            author=self.user,
            published=True,
        )

    def test_get_posts(self):
        url = "/api/blog/posts/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_post_detail(self):
        url = f"/api/blog/posts/{self.post.slug}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Post")
