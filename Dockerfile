FROM python:3.11
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . djangoTelegram
WORKDIR ./djangoTelegram
EXPOSE 8000
