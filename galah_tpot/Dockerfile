FROM debian:latest

COPY dist/ /root/dist/

RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    libsqlite3-dev \
    wget

WORKDIR /galah

RUN git clone https://github.com/0x4D31/galah.git .

COPY dist/honeypot.json /galah/vertexapi.json

COPY dist/config/ /galah/config/

COPY dist/default.json /galah/templates

COPY dist/cert/key.pem /galah/cert/key.pem
COPY dist/cert/cert.pem /galah/cert/cert.pem

RUN mkdir /galah/logs

RUN wget https://golang.org/dl/go1.22.0.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz && \
    rm go1.22.0.linux-amd64.tar.gz && \
    ln -s /usr/local/go/bin/go /usr/bin/go

RUN CGO_ENABLED=1 go mod download && \
    CGO_ENABLED=1 go build -o galah ./cmd/galah

ENTRYPOINT ["./galah"]
