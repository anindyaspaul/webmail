FROM python:3.8

RUN apt-get update

COPY . /webmail

WORKDIR /webmail

RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "entrypoint.sh"]
