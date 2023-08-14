FROM civisanalytics/datascience-python:latest

ENV CODE_DIR=/home/code
RUN mkdir -p $CODE_DIR
COPY ./code $CODE_DIR
WORKDIR $CODE_DIR
