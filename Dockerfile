# Smallest commonly-used Python base
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# (Optional but nice) add a non-root user for security
RUN addgroup -S app && adduser -S app -G app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Switch to non-root user
USER app

EXPOSE 8000

# If your file is app.py and Flask object is app = Flask(__name__)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers", "2", "--threads", "4", "--timeout", "60"]
