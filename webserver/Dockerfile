# Lojnote webserver Dockerfile

FROM python:2.7.14

ENV INSTALL_PATH /code
ENV REQ_TXT requirements.txt

WORKDIR $INSTALL_PATH

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y default-jre

RUN useradd jbopre

COPY $REQ_TXT $REQ_TXT
RUN pip install -r $REQ_TXT

# USER jbopre

EXPOSE 5000

# ENTRYPOINT ["/usr/local/bin/python", "/home/jbopre/lojnote/webserver/main.py"]
