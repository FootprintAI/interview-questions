# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
ADD requirements.txt /code/
COPY locustfile.py /code/
RUN pip install -r requirements.txt
ADD . /code/
