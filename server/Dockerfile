FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV DJANGO_SETTINGS_MODULE=djangoproj.settings
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn djangoproj.wsgi:application --bind 0.0.0.0:8000"]
