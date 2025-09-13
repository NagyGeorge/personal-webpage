from celery import shared_task
from django.core.mail import send_mail
from .models import Post


@shared_task
def send_post_notification(post_id):
    try:
        post = Post.objects.get(id=post_id)
        send_mail(
            f'New blog post: {post.title}',
            f'A new blog post "{post.title}" has been published.',
            'noreply@mysite.com',
            ['admin@mysite.com'],
            fail_silently=False,
        )
        return f'Notification sent for post: {post.title}'
    except Post.DoesNotExist:
        return f'Post with id {post_id} not found'