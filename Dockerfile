FROM python:3-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apk --no-cache add --virtual .build-deps build-base && \
    pip install -r requirements.txt && \
    apk del .build-deps
COPY . ./
CMD ["python3", "-u", "server.py"]
