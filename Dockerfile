FROM python:3.8

RUN apt-get update

COPY . /demodesk

WORKDIR /demodesk

RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "entrypoint.sh"]

