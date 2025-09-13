.PHONY: run migrate createsuperuser test lint install dev-install docker-up docker-down

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install black isort flake8 pre-commit pytest pytest-django pytest-cov

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser

test:
	pytest

lint:
	black --check .
	isort --check-only .
	flake8 .

format:
	black .
	isort .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

backup:
	python manage.py shell -c "from apps.core.tasks import backup_db; backup_db.delay()"

celery-worker:
	celery -A mysite worker --loglevel=info

celery-beat:
	celery -A mysite beat --loglevel=info

celery-flower:
	celery -A mysite flower --basic-auth=${FLOWER_USER:-admin}:${FLOWER_PASS:-admin}

shell:
	python manage.py shell

collectstatic:
	python manage.py collectstatic --noinput