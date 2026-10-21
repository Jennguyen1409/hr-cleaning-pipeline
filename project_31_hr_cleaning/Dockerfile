FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy cron job file
COPY crontab /etc/cron.d/pipeline-cron
RUN chmod 0644 /etc/cron.d/pipeline-cron

# Run cron in foreground
CMD ["cron", "-f"]
