# FROM civisanalytics/datascience-python:latest
FROM python:3.9-slim

ENV CODE_DIR=/home/code
RUN mkdir -p $CODE_DIR
COPY ./code $CODE_DIR
COPY ./requirements.txt $CODE_DIR/requirements.txt
WORKDIR $CODE_DIR
RUN pip install -r requirements.txt

