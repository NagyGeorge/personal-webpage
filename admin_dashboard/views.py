from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from blog.models import Post
from portfolio.models import Project


def admin_required(view_func):
    """Decorator to ensure only allowed admin email can access admin views"""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/google/login/")

        if request.user.email != settings.ALLOWED_ADMIN_EMAIL:
            messages.error(request, "You don't have permission to access this area.")
            return redirect("/")

        return view_func(request, *args, **kwargs)

    return wrapper


@admin_required
def dashboard_view(request):
    """Main admin dashboard with overview stats"""
    context = {
        "total_posts": Post.objects.count(),
        "published_posts": Post.objects.filter(published=True).count(),
        "draft_posts": Post.objects.filter(published=False).count(),
        "total_projects": Project.objects.count(),
        "featured_projects": Project.objects.filter(featured=True).count(),
        "recent_posts": Post.objects.order_by("-created_at")[:5],
        "recent_projects": Project.objects.order_by("-created_at")[:5],
    }
    return render(request, "admin_dashboard/dashboard.html", context)


def access_denied_view(request):
    """View for when user doesn't have admin access"""
    return render(request, "admin_dashboard/access_denied.html")
