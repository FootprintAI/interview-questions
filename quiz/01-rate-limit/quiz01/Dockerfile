# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY Pytest_test.py /code/
COPY locustfile.py /code/
RUN pip install -r requirements.txt
COPY . /code/
