FROM python:3.7-slim

ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY . ./

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
