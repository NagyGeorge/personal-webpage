from django.urls import path

from .views import PostDetailView, PostListView, TagListView

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("tags/", TagListView.as_view(), name="tag-list"),
]
