FROM ubuntu:trusty

RUN apt-get update && apt-get install -y \
    net-tools \
    curl \
    iputils-ping \
    iproute \
    && apt-get clean \
    && rm -rf /var/tmp/*

WORKDIR /usr/src/app

COPY . .

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - \
&& apt-get install -y nodejs \
&& npm install express

RUN chmod +x ./start.sh

ENV FLASK_APP server.js
ENV FLASK_PORT 3000

EXPOSE 3000

ENTRYPOINT ./start.sh
