FROM python:3.12-alpine

WORKDIR /app

COPY server.py .
COPY ./data/emojis.json .
COPY index.html .
COPY fonts/ ./fonts/

EXPOSE 7700

CMD ["python3", "server.py", "7700", "data/emojis.json"]