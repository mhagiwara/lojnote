# Lojnote webserver Dockerfile

FROM python:3.6.4

RUN apt-get update
RUN apt-get upgrade -y

RUN useradd -d /home/jbopre -m jbopre

RUN pip install Flask

USER jbopre

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/python", "/home/jbopre/lojnote/webserver/main.py"]
