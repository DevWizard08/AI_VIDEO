# 1. Base image
FROM python:3.11-slim

# 2. System deps: ImageMagick, pip and alias 'python'
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       imagemagick \
       python3-pip \
       python-is-python3 \
    && rm -rf /var/lib/apt/lists/*

# 3. Set working dir
WORKDIR /app

# 4. Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy app code
COPY . .

# 6. Flask env defaults
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 7. Expose port
EXPOSE 5000

# 8. Start server
CMD ["python", "app.py"]
