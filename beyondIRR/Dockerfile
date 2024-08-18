FROM python:3.11.2

WORKDIR /app

RUN apt-get update && apt-get install -y openssl

RUN openssl genpkey -algorithm RSA -out private_key.pem && \
    openssl rsa -pubout -in private_key.pem -out public_key.pem

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /app

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD python manage.py runserver 0.0.0.0:8000
