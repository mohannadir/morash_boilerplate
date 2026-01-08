FROM python:3.10

# Install dependencies
RUN apt-get update && apt-get install -y \
    gettext nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy application code
COPY . /app/

# Copy wait-for-it script
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the development server with auto-reload
CMD ["./wait-for-it.sh", "postgres:5432", "--", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
