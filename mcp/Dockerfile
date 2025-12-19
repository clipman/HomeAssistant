FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir requests

COPY run.sh /run.sh
COPY app /app

RUN chmod +x /run.sh

CMD ["/run.sh"]
