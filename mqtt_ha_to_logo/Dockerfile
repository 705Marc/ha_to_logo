FROM python:3.11-alpine

WORKDIR /app

# Abhängigkeiten installieren
RUN pip install --no-cache-dir paho-mqtt

# Skript kopieren
COPY main.py /app/main.py

# Unbuffered Python output
ENV PYTHONUNBUFFERED=1

CMD [ "python", "-u", "/app/main.py" ]