FROM python:3.9-slim

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

 CMD ["flask", "run", "--host=0.0.0.0"]