FROM python:3

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn EpicEvent.wsgi:application --bind 0.0.0.0:$PORT