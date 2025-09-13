FROM python:3.12-slim

WORKDIR /app

# Accept SECRET_KEY as build argument for collectstatic
ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

# Run collectstatic with the provided SECRET_KEY
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["./entrypoint.sh"]
