FROM python:3.9-slim

RUN adduser -D myuser
USER myuser

WORKDIR /app
ADD . /app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8

ENV PORT=8000

RUN apt-get update && apt-get install -y python3-pip gunicorn

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

RUN pipenv install --skip-lock --system --dev

EXPOSE $PORT
CMD gunicorn mysite.wsgi --bind 0.0.0.0:$PORT
