FROM civisanalytics/datascience-python:latest

ENV CODE_DIR=/home/code
RUN mkdir -p $CODE_DIR
COPY ./code $CODE_DIR
COPY ./requirements.txt $CODE_DIR/requirements.txt
WORKDIR $CODE_DIR
RUN pip install -r requirements.txt

