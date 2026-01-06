FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5000
EXPOSE 5000

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Environment variable to bind to 0.0.0.0
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["./entrypoint.sh"]
