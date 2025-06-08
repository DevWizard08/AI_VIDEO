# 1. Base image
FROM python:3.11-slim

# 2. System deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       imagemagick \
       python3-pip \
       python-is-python3 \
       fontconfig \
       wget \
       git \
       ffmpeg \
       espeak-ng \
       libespeak-ng-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Fix ImageMagick policies
RUN for f in /etc/ImageMagick-*/policy.xml; do \
      if [ -f "$f" ]; then \
        sed -i '/<policy domain="path" rights="none" pattern="@\*"\/>/d' "$f"; \
        sed -i '/<policy domain="coder" rights="none" pattern="MVG"\/>/d' "$f"; \
        sed -i '/<policy domain="coder" rights="none" pattern="TXT"\/>/d' "$f"; \
      fi; \
    done

# 4. Install font
RUN wget -qO /usr/share/fonts/truetype/LeelawadeeUI-Bold.ttf \
      https://raw.githubusercontent.com/streetsamurai00mi/ttf-ms-win10/build/LeelaUIb.ttf
RUN fc-cache -f -v

# 5. Set working dir
WORKDIR /app

# 6. Copy and install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 7. Install Coqui TTS + server
RUN pip install TTS==0.22.0

# 8. Download and cache a model (optional but smart)
RUN python3 -c "from TTS.utils.manage import ModelManager; ModelManager().download_model('tts_models/en/ljspeech/tacotron2-DDC')"

# 9. Copy app files
COPY . .

# 10. Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 11. Environment
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 12. Expose port
EXPOSE 5000

# 13. Start both services
CMD ["/start.sh"]
