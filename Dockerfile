# Base image
FROM python:3.9

# Install ImageMagick
RUN apt-get update && apt-get install -y imagemagick

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for ImageMagick
ENV IMAGEMAGICK_BINARY=/usr/bin/convert

# Expose port
EXPOSE 5000

# Start server
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
