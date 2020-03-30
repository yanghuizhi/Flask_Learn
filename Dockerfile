FROM python:3.6-alpine

RUN adduser -D FLask_Learn

WORKDIR /home/FLask_Learn

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY Flask_Learn.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP FLask_Learn.py

RUN chown -R FLask_Learn:FLask_Learn ./
USER FLask_Learn

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
