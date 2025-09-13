from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.blog.models import Post
from apps.core.tasks import send_contact_email
from apps.portfolio.models import Project


def home(request):
    latest_posts = Post.objects.filter(status="published").order_by("-created_at")[:3]
    latest_projects = Project.objects.order_by("-id")[:6]

    context = {
        "latest_posts": latest_posts,
        "latest_projects": latest_projects,
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")


def projects(request):
    projects_list = Project.objects.order_by("-id")
    context = {"projects": projects_list}
    return render(request, "projects.html", context)


def blog_index(request):
    posts_list = Post.objects.filter(status="published").order_by("-created_at")
    paginator = Paginator(posts_list, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # If HTMX request, return only the posts partial
    if request.headers.get("HX-Request"):
        return render(request, "blog/_posts.html", {"page_obj": page_obj})

    context = {"page_obj": page_obj}
    return render(request, "blog/index.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    context = {"post": post}
    return render(request, "blog/detail.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        honeypot = request.POST.get("website", "").strip()

        # Simple honeypot check
        if honeypot:
            messages.error(request, "Invalid submission.")
            return HttpResponseRedirect(reverse("contact"))

        # Basic validation
        if not all([name, email, message]):
            messages.error(request, "All fields are required.")
            return HttpResponseRedirect(reverse("contact"))

        # Enqueue Celery task
        send_contact_email.delay(name, email, message)
        messages.success(request, "Thank you! Your message has been sent.")
        return HttpResponseRedirect(reverse("contact"))

    return render(request, "contact.html")
