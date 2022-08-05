FROM python:3.10-slim as builder 

RUN apt update -y && apt install openssh-client -y
RUN mkdir -p /app/secrets && ssh-keygen -t rsa -b 4096 -f /app/secrets/ca_key -N ""

COPY . /app 
WORKDIR /app 

RUN pip3 install --no-cache-dir -r /app/requirements.txt 

ENV PYTHONUNBUFFERED=True
ENV TOKEN_KEY=default-password-fixme 

CMD gunicorn --bind :5000 app:app
