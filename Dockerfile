FROM python:3.10-slim

WORKDIR /app

# install git so pip can clone from GitHub
RUN apt-get update \
 && apt-get install -y git \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
