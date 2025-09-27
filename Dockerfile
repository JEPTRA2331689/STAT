FROM python:3.10-slim-buster

WORKDIR /Stat-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

WORKDIR /Stat-app/stat

RUN flask db init

RUN flask db migrate

RUN flask db upgrade

WORKDIR /Stat-app

CMD ["python3","main.py"]
