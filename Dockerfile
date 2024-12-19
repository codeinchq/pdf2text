FROM python:3.9-slim

ARG PORT=5000
ENV debian_frontend=noninteractive
ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/share/nltk_data

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /usr/share/nltk_data && \
    python -m nltk.downloader -d $NLTK_DATA punkt_tab

COPY app.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE $PORT
ENTRYPOINT ["/app/entrypoint.sh"]
