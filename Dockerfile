FROM python:3.8-alpine

RUN apk update

RUN \
 apk add --no-cache postgresql-libs nodejs npm curl bash git && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev openssl-dev libffi-dev python3-dev

# SETUP PYTHON PKGS
RUN pip install --upgrade pip
RUN pip install cassandra-migrate
RUN pip install pylint psycopg2 yoyo-migrations awscli

# INSTALL KUBERNETES
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
 && chmod +x ./kubectl \
 && mv ./kubectl /usr/local/bin

# SETUP TERRAFORM ENVIRONMENT
RUN wget --quiet https://releases.hashicorp.com/terraform/0.13.4/terraform_0.13.4_linux_amd64.zip \
    && unzip terraform_0.13.4_linux_amd64.zip \
    && rm terraform_0.13.4_linux_amd64.zip \
    && mv terraform /usr/bin/terraform \
    && terraform version

# PRE-INSTALL NODE DEPS FOR BUILD SCRIPTS
COPY package.json package.json
RUN npm install
RUN npm install -g ts-node
