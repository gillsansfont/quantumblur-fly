FROM python:3.10-slim

WORKDIR /app

# 1) install git so pip can fetch from GitHub
RUN apt-get update \
 && apt-get install -y git \
 && rm -rf /var/lib/apt/lists/*

# 2) install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) copy your app code
COPY . .

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
