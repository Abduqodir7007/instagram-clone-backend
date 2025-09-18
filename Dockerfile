FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1    

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /app

RUN chmod +x /app/entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
 