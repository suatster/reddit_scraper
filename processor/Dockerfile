FROM python:3.12.4

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl 


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./processor
