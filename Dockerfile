FROM ubuntu:16.04 

MAINTAINER Kailin "kailinluca@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt 

WORKDIR /app 

RUN pip install -r requirements.txt 

COPY . /app 

ENTRYPOINT ["python3"] 

CMD ["run.py"]

