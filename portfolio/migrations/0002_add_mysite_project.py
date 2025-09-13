from django.db import migrations


def add_mysite_project(apps, schema_editor):
    """Add the my-site project to the portfolio"""
    Project = apps.get_model('portfolio', 'Project')

    Project.objects.get_or_create(
        title='Django Portfolio & Blog Platform',
        defaults={
            'description': 'A full-stack Django web application featuring a personal blog, project portfolio, and health monitoring. Built with modern deployment practices including Docker, CI/CD pipelines, and Railway hosting.',
            'technologies': 'Django, PostgreSQL, Redis, Celery, Docker, HTMX, Tailwind CSS, GitHub Actions',
            'github_url': 'https://github.com/georgehogarth/my-site',
            'live_url': 'https://my-site-production.up.railway.app/',
        }
    )


def remove_mysite_project(apps, schema_editor):
    """Remove the my-site project from the portfolio"""
    Project = apps.get_model('portfolio', 'Project')

    Project.objects.filter(
        title='Django Portfolio & Blog Platform'
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_mysite_project,
            reverse_code=remove_mysite_project,
        ),
    ]
