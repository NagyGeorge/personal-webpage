from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Tag
from .serializers import PostSerializer, TagSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tags']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    lookup_field = 'slug'


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer