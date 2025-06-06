# 1. Base image
FROM python:3.11-slim

# 2. System deps: ImageMagick, pip, alias 'python', plus fontconfig and wget
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       imagemagick \
       python3-pip \
       python-is-python3 \
       fontconfig \
       wget \
    && rm -rf /var/lib/apt/lists/*

# 3. Remove ImageMagick security-policy lines that block "@*" (and MVG/TXT) so TextClip works
RUN for f in /etc/ImageMagick-*/policy.xml; do \
      if [ -f "$f" ]; then \
        sed -i '/<policy domain="path" rights="none" pattern="@\*"\/>/d' "$f"; \
        sed -i '/<policy domain="coder" rights="none" pattern="MVG"\/>/d' "$f"; \
        sed -i '/<policy domain="coder" rights="none" pattern="TXT"\/>/d' "$f"; \
      fi; \
    done

# 4. Download Leelawadee UI Bold from a public GitHub repo and install into system fonts
#    (this comes from streetsamurai00mi/ttf-ms-win10, which bundles Windows 10 fonts in a Linux-friendly repo) :contentReference[oaicite:0]{index=0}
RUN wget -qO /usr/share/fonts/truetype/LeelawadeeUI-Bold.ttf \
      https://raw.githubusercontent.com/streetsamurai00mi/ttf-ms-win10/build/LeelaUIb.ttf

# 5. Rebuild font cache so ImageMagick can find Leelawadee UI Bold
RUN fc-cache -f -v

# 6. Set working dir
WORKDIR /app

# 7. Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copy app code
COPY . .

# 9. Flask env defaults
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 10. Expose port
EXPOSE 5000

# 11. Start server
CMD ["python", "app.py"]
