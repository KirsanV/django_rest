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


FROM python:3.13-slim as builder

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
RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.13-slim as final

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        zlib1g \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

RUN chown -R appuser:appuser /app
USER appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]