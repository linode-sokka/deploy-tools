FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

RUN python setup.py install
RUN chmod +x configure_sokka.py
ENTRYPOINT ["/app/configure_sokka.py"]
