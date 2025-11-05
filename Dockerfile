FROM python:3.12.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.2.1"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-interaction

COPY app .

RUN chmod +x prestart.sh
RUN chmod +x main.py

ENTRYPOINT ["./prestart.sh"]
CMD ["uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8000"]
