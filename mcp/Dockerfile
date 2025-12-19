FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends jq && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir requests

COPY run.sh /run.sh
COPY app /app

RUN chmod +x /run.sh

CMD ["/run.sh"]
