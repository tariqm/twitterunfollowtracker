FROM python:3.10-slim-buster
RUN mkdir /app
ADD ./app /app
COPY ./config.ini /app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python", "app.py" ]