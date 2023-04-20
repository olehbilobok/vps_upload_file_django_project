FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

WORKDIR /upload_project

COPY requirements.txt /upload_project/

RUN pip install -r requirements.txt

RUN pip install django-redis

COPY . /upload_project/

EXPOSE 8000

