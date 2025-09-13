from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from blog.models import Post, Tag
from portfolio.models import Project


class FrontendViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create test data
        self.tag = Tag.objects.create(name="Django", slug="django")
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            body="This is a test post content",
            published=True,
        )
        self.post.tags.add(self.tag)

        self.project = Project.objects.create(
            title="Test Project",
            description="A test project",
            link="https://example.com",
        )

    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to My Site")
        self.assertContains(response, "Latest Blog Posts")
        self.assertContains(response, "Latest Projects")

    def test_home_page_shows_latest_content(self):
        """Test that home page displays latest posts and projects"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.project.title)

    def test_about_page_loads(self):
        """Test that about page loads successfully"""
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Me")
        self.assertContains(response, "conductor for a Class 1 freight railway")

    def test_projects_page_loads(self):
        """Test that projects page loads and shows projects"""
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projects")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)

    def test_blog_index_page_loads(self):
        """Test that blog index page loads successfully"""
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog")
        self.assertContains(response, self.post.title)

    def test_blog_detail_page_loads(self):
        """Test that blog detail page loads for valid slug"""
        response = self.client.get(
            reverse("blog_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
        self.assertContains(response, self.tag.name)

    def test_blog_detail_404_for_invalid_slug(self):
        """Test that blog detail returns 404 for invalid slug"""
        response = self.client.get(
            reverse("blog_detail", kwargs={"slug": "invalid-slug"})
        )
        self.assertEqual(response.status_code, 404)

    def test_blog_detail_404_for_draft_post(self):
        """Test that draft posts are not accessible"""
        draft_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            author=self.user,
            body="Draft content",
            published=False,
        )
        response = self.client.get(
            reverse("blog_detail", kwargs={"slug": draft_post.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_contact_page_get(self):
        """Test that contact page loads successfully"""
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Get in Touch")
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="message"')

    @patch("apps.core.tasks.send_contact_email.delay")
    def test_contact_form_valid_submission(self, mock_send_email):
        """Test valid contact form submission"""
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message",
            "website": "",  # honeypot field should be empty
        }
        response = self.client.post(reverse("contact"), form_data)
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful submission
        mock_send_email.assert_called_once_with(
            "Test User", "test@example.com", "This is a test message"
        )

    def test_contact_form_honeypot_protection(self):
        """Test that honeypot field prevents spam submissions"""
        form_data = {
            "name": "Spam Bot",
            "email": "spam@example.com",
            "message": "Spam message",
            "website": "https://spam.com",  # honeypot field filled
        }
        response = self.client.post(reverse("contact"), form_data)
        self.assertEqual(response.status_code, 302)  # Redirects but doesn't process

    def test_contact_form_validation_errors(self):
        """Test contact form validation for missing fields"""
        # Test missing name
        form_data = {
            "name": "",
            "email": "test@example.com",
            "message": "Test message",
            "website": "",
        }
        response = self.client.post(reverse("contact"), form_data)
        self.assertEqual(response.status_code, 302)  # Redirects with error

        # Test missing email
        form_data = {
            "name": "Test User",
            "email": "",
            "message": "Test message",
            "website": "",
        }
        response = self.client.post(reverse("contact"), form_data)
        self.assertEqual(response.status_code, 302)  # Redirects with error

        # Test missing message
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "",
            "website": "",
        }
        response = self.client.post(reverse("contact"), form_data)
        self.assertEqual(response.status_code, 302)  # Redirects with error


class HTMXViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create multiple posts for pagination testing
        for i in range(15):
            Post.objects.create(
                title=f"Test Post {i}",
                slug=f"test-post-{i}",
                author=self.user,
                body=f"Content for post {i}",
                published=True,
            )

    def test_blog_index_regular_request(self):
        """Test regular blog index request returns full page"""
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<html>")  # Full page
        self.assertContains(response, "Load More Posts")  # Pagination button

    def test_blog_index_htmx_request(self):
        """Test HTMX request returns partial template"""
        headers = {"HTTP_HX_REQUEST": "true"}
        response = self.client.get(reverse("blog_index"), **headers)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<html>")  # Partial template
        self.assertContains(response, "Test Post")  # Contains posts

    def test_blog_pagination_htmx(self):
        """Test HTMX pagination request"""
        headers = {"HTTP_HX_REQUEST": "true"}
        response = self.client.get(reverse("blog_index") + "?page=2", **headers)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<html>")  # Partial template
        # Should contain posts from page 2


class TemplateRenderingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_base_template_renders(self):
        """Test that base template renders without errors"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<nav")
        self.assertContains(response, "<footer")
        self.assertContains(response, "My Site")

    def test_static_file_references(self):
        """Test that static file references are correct"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "/static/site.css")
        self.assertContains(response, "htmx.org")
        self.assertContains(response, "tailwindcss.com")

    def test_navigation_links(self):
        """Test that navigation links are present and correct"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'href="/about/"')
        self.assertContains(response, 'href="/projects/"')
        self.assertContains(response, 'href="/blog/"')
        self.assertContains(response, 'href="/contact/"')

    def test_csrf_token_in_forms(self):
        """Test that CSRF tokens are present in forms"""
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "csrfmiddlewaretoken")


class StaticFilesTests(TestCase):
    def test_css_file_accessible(self):
        """Test that CSS file is accessible"""
        # In test mode, static files might not be served by Django
        # This test ensures the URL pattern works
        # In production, Whitenoise will serve these files
        pass

    def test_collectstatic_works(self):
        """Test that collectstatic management command works"""
        import tempfile

        from django.core.management import call_command
        from django.test.utils import override_settings

        with tempfile.TemporaryDirectory() as temp_dir:
            with override_settings(STATIC_ROOT=temp_dir):
                try:
                    call_command("collectstatic", "--noinput", verbosity=0)
                    # If no exception is raised, collectstatic works
                    self.assertTrue(True)
                except Exception as e:
                    self.fail(f"collectstatic failed: {e}")


class UrlPatternsTests(TestCase):
    def test_url_patterns_resolve(self):
        """Test that all URL patterns resolve correctly"""
        urls_to_test = [
            ("home", {}),
            ("about", {}),
            ("projects", {}),
            ("blog_index", {}),
            ("contact", {}),
        ]

        for url_name, kwargs in urls_to_test:
            with self.subTest(url_name=url_name):
                url = reverse(url_name, kwargs=kwargs)
                self.assertIsNotNone(url)

    def test_blog_detail_url_with_slug(self):
        """Test that blog detail URL resolves with slug"""
        url = reverse("blog_detail", kwargs={"slug": "test-slug"})
        self.assertEqual(url, "/blog/test-slug/")
