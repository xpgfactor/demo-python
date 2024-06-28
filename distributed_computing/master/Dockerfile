FROM python:3.12-slim

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get upgrade -y

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY main.py .

CMD ["python", "main.py"]