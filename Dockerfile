# FROM python:3.13-slim
#
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
#
#
# WORKDIR /app
#
#
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         build-essential \
#         libpq-dev \
#         gcc \
#         libffi-dev \
#         libssl-dev \
#         libjpeg-dev \
#         zlib1g-dev \
#     && rm -rf /var/lib/apt/lists/*
#
#
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
#
# COPY . .
#
#
# EXPOSE 8000
#
#
# CMD ["bash", "-lc", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]


FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        libffi-dev \
        libssl-dev \
        libjpeg-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]