FROM python:3.12

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash appuser && \
    mkdir -p /backend/static /backend/media && \
    chown -R appuser:appuser /backend

WORKDIR /backend

<<<<<<< HEAD
# Копируем все файлы из текущей директории
=======
>>>>>>> 157948875a43b2f5f5f8199ec97e0f4a964353c2
COPY --chown=appuser:appuser . .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

USER appuser