# Lojnote webserver Dockerfile

FROM python:2.7.14

ENV REQ_TXT requirements.txt

RUN apt-get update
RUN apt-get upgrade -y

RUN useradd -d /home/jbopre -m jbopre

COPY $REQ_TXT $REQ_TXT
RUN pip install -r $REQ_TXT

USER jbopre

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/python", "/home/jbopre/lojnote/webserver/main.py"]
