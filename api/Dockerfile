FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# System deps kept minimal. Add only if needed later.
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /app/requirements.txt
# Intentionally install now in the image, but this file is not executed by the init script.
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app

EXPOSE 8000
# Placeholder command. You will adjust after wiring app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
