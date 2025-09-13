# My Site

Django project with blog, portfolio, and status monitoring capabilities.

## Features

- **Blog App**: CRUD operations for blog posts with tags, powered by Django REST Framework
- **Portfolio App**: Showcase projects with descriptions, links, and screenshots
- **Status App**: Health check endpoint (`/healthz`) and Prometheus metrics (`/metrics`)
- **Celery Integration**: Background task processing with Redis as broker
- **PostgreSQL Database**: Production-ready database configuration
- **Docker Support**: Complete containerization with docker-compose
- **CI/CD Pipeline**: GitHub Actions for testing and Docker image building

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd my-site
   ```

2. **Set up virtual environment using UV** (recommended)
   ```bash
   pip install uv
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   # or using make
   make install
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database and Redis settings
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   # or using make
   make migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   # or using make
   make createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   # or using make
   make run
   ```

8. **Start Celery worker** (in another terminal)
   ```bash
   celery -A mysite worker --loglevel=info
   # or using make
   make celery-worker
   ```

### Docker Development

1. **Start all services**
   ```bash
   docker-compose up -d
   # or using make
   make docker-up
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Endpoints

### Blog API
- `GET /api/blog/posts/` - List all published posts
- `GET /api/blog/posts/{slug}/` - Get specific post by slug
- `GET /api/blog/tags/` - List all tags

### Portfolio API
- `GET /api/portfolio/projects/` - List all projects
- `GET /api/portfolio/projects/{id}/` - Get specific project

### Status Endpoints
- `GET /healthz/` - Health check endpoint
- `GET /metrics/` - Prometheus metrics

## Available Make Commands

```bash
make install         # Install dependencies
make dev-install     # Install dev dependencies
make run            # Start development server
make migrate        # Run database migrations
make createsuperuser # Create Django superuser
make test           # Run tests
make lint           # Run linting (black, isort, flake8)
make format         # Format code (black, isort)
make docker-up      # Start Docker services
make docker-down    # Stop Docker services
make backup         # Create database backup
make celery-worker  # Start Celery worker
make celery-beat    # Start Celery beat scheduler
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_*`: PostgreSQL database connection settings
- `REDIS_URL`: Redis connection URL

## Database Backup

Create database backups using the custom management command:

```bash
python manage.py backup_db --output-dir backups/
```

Backups are automatically created via Celery tasks and old backups are cleaned up periodically.

## Development

### Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

**Important**: Pre-commit hooks are required and will run automatically on every commit. They will prevent commits that don't pass formatting and linting checks. To run manually:
```bash
pre-commit run --all-files
```

### Testing

Run tests with pytest:
```bash
pytest
# or
make test
```

### Adding New Apps

1. Create the app: `python manage.py startapp appname`
2. Add to `INSTALLED_APPS` in `mysite/settings.py`
3. Create models, views, and URLs
4. Run migrations: `make migrate`

## Production Deployment

1. Set environment variables appropriately
2. Use Docker or build from source
3. Configure reverse proxy (nginx/Apache)
4. Set up SSL certificates
5. Configure monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run linting and tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
