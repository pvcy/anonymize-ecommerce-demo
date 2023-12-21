FROM python:3.10-slim-bullseye

ADD ./src /app

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["./docker-entrypoint.sh"]

