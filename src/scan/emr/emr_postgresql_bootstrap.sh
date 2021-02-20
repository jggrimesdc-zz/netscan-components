#!/bin/bash
sudo wget https://jdbc.postgresql.org/download/postgresql-42.2.18.jar -P /usr/lib/spark/jars
sudo yum -y install gcc python-setuptools python-devel postgresql-devel
sudo /usr/bin/pip3 install --upgrade pip
sudo /usr/local/bin/pip3 install psycopg2-binary
