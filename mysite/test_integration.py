from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth.models import User
from django.template import Context, RequestContext
from django.template.loader import render_to_string
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from blog.models import Post, Tag
from portfolio.models import Project


@pytest.mark.integration
class HTMXIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create multiple posts for pagination testing
        self.posts = []
        for i in range(25):  # Create enough posts for multiple pages
            post = Post.objects.create(
                title=f"Test Post {i:02d}",
                slug=f"test-post-{i:02d}",
                author=self.user,
                body=(
                    f"Content for test post {i}. "
                    "This is a longer content to test excerpt functionality."
                ),
                published=True,
            )
            self.posts.append(post)

    @pytest.mark.htmx
    def test_htmx_blog_pagination_first_page(self):
        """Test HTMX request for first page of blog posts"""
        headers = {"HTTP_HX_REQUEST": "true"}
        response = self.client.get(reverse("blog_index"), **headers)

        self.assertEqual(response.status_code, 200)
        # Should not contain full HTML structure
        self.assertNotContains(response, "<html>")
        self.assertNotContains(response, "<head>")
        self.assertNotContains(response, "<nav>")

        # Should contain posts content
        self.assertContains(response, "Test Post")
        # Should contain pagination button if there are more posts
        self.assertContains(response, "Load More Posts")

    @pytest.mark.htmx
    def test_htmx_blog_pagination_second_page(self):
        """Test HTMX request for second page of blog posts"""
        headers = {"HTTP_HX_REQUEST": "true"}
        response = self.client.get(reverse("blog_index") + "?page=2", **headers)

        self.assertEqual(response.status_code, 200)
        # Should be partial template
        self.assertNotContains(response, "<html>")
        # Should contain different posts than first page
        self.assertContains(response, "Test Post")

    @pytest.mark.htmx
    def test_htmx_blog_pagination_last_page(self):
        """Test HTMX request for last page (no more pagination)"""
        headers = {"HTTP_HX_REQUEST": "true"}
        response = self.client.get(reverse("blog_index") + "?page=3", **headers)

        self.assertEqual(response.status_code, 200)
        # On last page, should not have "Load More Posts" button
        # The template logic should determine if pagination button appears

    @pytest.mark.htmx
    def test_htmx_request_headers_detection(self):
        """Test that HTMX headers are properly detected"""
        # Regular request
        response = self.client.get(reverse("blog_index"))
        self.assertContains(response, "<html>")  # Full page

        # HTMX request
        headers = {"HTTP_HX_REQUEST": "true"}
        response = self.client.get(reverse("blog_index"), **headers)
        self.assertNotContains(response, "<html>")  # Partial page

    @pytest.mark.htmx
    def test_htmx_pagination_post_content(self):
        """Test that paginated posts contain proper content and formatting"""
        headers = {"HTTP_HX_REQUEST": "true"}
        response = self.client.get(reverse("blog_index"), **headers)

        # Check for proper article structure
        self.assertContains(response, "<article")
        self.assertContains(response, "hover:text-blue-600")  # CSS classes
        self.assertContains(response, "Read more →")  # Read more links


@pytest.mark.frontend
class TemplateIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_template_inheritance_chain(self):
        """Test that template inheritance works correctly"""
        response = self.client.get(reverse("home"))

        # Check base template elements
        self.assertContains(response, "<nav")
        self.assertContains(response, "<footer")
        self.assertContains(response, "My Site")  # Site title

        # Check content block is populated
        self.assertContains(response, "Welcome to My Site")

    def test_template_static_file_loading(self):
        """Test that templates properly reference static files"""
        response = self.client.get(reverse("home"))

        # Check CSS references
        self.assertContains(response, "/static/site.css")

        # Check external library references
        self.assertContains(response, "htmx.org")
        self.assertContains(response, "tailwindcss.com")

    def test_template_url_reversing(self):
        """Test that URL reversing works in templates"""
        response = self.client.get(reverse("home"))

        # Check navigation URLs
        self.assertContains(response, 'href="/about/"')
        self.assertContains(response, 'href="/projects/"')
        self.assertContains(response, 'href="/blog/"')
        self.assertContains(response, 'href="/contact/"')

    def test_template_context_variables(self):
        """Test that context variables are properly passed to templates"""
        # Create test data
        tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            body="Test content",
            published=True,
        )
        post.tags.add(tag)

        project = Project.objects.create(
            title="Test Project", description="Test description"
        )

        response = self.client.get(reverse("home"))

        # Check that latest posts and projects are shown
        self.assertContains(response, post.title)
        self.assertContains(response, project.title)

    def test_template_conditional_rendering(self):
        """Test conditional rendering in templates"""
        # Test empty state
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No blog posts yet")
        self.assertContains(response, "No projects yet.")

        # Create content and test populated state
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            body="Test content",
            published=True,
        )

        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "No blog posts yet")
        self.assertContains(response, post.title)


@pytest.mark.integration
class ContactFormIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("apps.core.tasks.send_contact_email.delay")
    def test_contact_form_full_workflow(self, mock_send_email):
        """Test complete contact form submission workflow"""
        # GET request - should show form
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Get in Touch")

        # POST request - should process form and redirect
        form_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, this is a test message.",
            "website": "",  # honeypot
        }

        response = self.client.post(reverse("contact"), form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check that Celery task was called
        mock_send_email.assert_called_once_with(
            "John Doe", "john@example.com", "Hello, this is a test message."
        )

        # Check success message appears
        messages = list(response.context["messages"])
        self.assertTrue(any("Thank you" in str(message) for message in messages))

    def test_contact_form_csrf_protection(self):
        """Test that CSRF protection is working"""
        form_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Test message",
            "website": "",
        }

        # Submit without CSRF token should fail
        response = self.client.post(reverse("contact"), form_data)
        self.assertEqual(response.status_code, 403)  # CSRF failure

    def test_contact_form_honeypot_integration(self):
        """Test honeypot field integration"""
        form_data = {
            "name": "Spam Bot",
            "email": "spam@example.com",
            "message": "Spam message",
            "website": "https://spam.com",  # honeypot filled
        }

        with patch("apps.core.tasks.send_contact_email.delay") as mock_send_email:
            response = self.client.post(reverse("contact"), form_data)
            self.assertEqual(response.status_code, 302)  # Redirects
            # Should not send email for honeypot submissions
            mock_send_email.assert_not_called()


@pytest.mark.integration
class EndToEndNavigationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create sample content
        self.post = Post.objects.create(
            title="Sample Post",
            slug="sample-post",
            author=self.user,
            body="Sample content",
            published=True,
        )

    def test_complete_site_navigation(self):
        """Test navigation through all main pages"""
        # Start at home
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        # Navigate to about
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

        # Navigate to projects
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 200)

        # Navigate to blog
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)

        # Navigate to blog detail
        response = self.client.get(
            reverse("blog_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)

        # Navigate to contact
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_navigation_links_work(self):
        """Test that navigation links in templates work correctly"""
        response = self.client.get(reverse("home"))

        # Extract navigation URLs and test they work
        nav_urls = ["/about/", "/projects/", "/blog/", "/contact/"]

        for url in nav_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_blog_navigation_flow(self):
        """Test blog-specific navigation flow"""
        # Go to blog index
        response = self.client.get(reverse("blog_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

        # Click on blog post
        response = self.client.get(
            reverse("blog_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.body)

        # Check "Back to Blog" link works
        self.assertContains(response, "Back to Blog")
