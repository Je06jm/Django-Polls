FROM python:3.9-slim

RUN apt-get update && apt-get install gunicorn -y

WORKDIR /app
COPY . .

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8

ENV PORT=8000

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN python3 manage.py collectstatic --noinput

EXPOSE $PORT
CMD gunicorn mysite.wsgi --bind 0.0.0.0:$PORT
