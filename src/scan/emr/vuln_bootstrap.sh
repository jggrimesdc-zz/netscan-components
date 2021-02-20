#!/bin/bash
sudo aws s3 cp s3://emr-cyberscan-bootstrap/spark-cassandra-connector-assembly-2.5.1.jar /usr/lib/spark/jars/
sudo yum -y install gcc python-setuptools python-devel postgresql-devel
sudo /usr/bin/pip3 install --upgrade pip
sudo /usr/local/bin/pip3 install psycopg2-binary
sudo /usr/local/bin/pip3 install pandas
sudo /usr/local/bin/pip3 install cpe
