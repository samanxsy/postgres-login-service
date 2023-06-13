FROM python:3.10-alpine

WORKDIR /login-system

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .dockerignore /

COPY ./backend ./backend

COPY ./tests ./tests

COPY setup.cfg ./

ENV SESSION_KEY=$SESSION_KEY

ENV DB_NAME=$DB_NAME

ENV DB_USER=$DB_USER

ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

CMD ["gunicorn", "--bind=0.0.0.0:8000", "backend.server:app"]

EXPOSE 8000
