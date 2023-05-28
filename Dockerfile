FROM <image-name>

WORKDIR /<directory-name>

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .dockerignore /

COPY ./app ./app

ENV API_KEY=<$The_API_KEY>

CMD ["gunicorn", "--bind=0.0.0.0:8000", "app.server:app"]

EXPOSE 8000