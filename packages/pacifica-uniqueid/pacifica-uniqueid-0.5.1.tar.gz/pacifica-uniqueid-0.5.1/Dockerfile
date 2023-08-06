FROM python:3.8

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir .
RUN pip install --no-cache-dir uwsgi pymysql psycopg2 cryptography
ENV PEEWEE_PROTO mysql
ENV PEEWEE_USER uniqueid
ENV PEEWEE_PASS uniqueid
ENV PEEWEE_PORT 3306
ENV PEEWEE_ADDR 127.0.0.1
ENV PEEWEE_DATABASE pacifica_uniqueid
EXPOSE 8051
ENTRYPOINT ["/bin/bash", "/usr/src/app/entrypoint.sh"]
