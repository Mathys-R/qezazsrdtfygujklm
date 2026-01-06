FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]
