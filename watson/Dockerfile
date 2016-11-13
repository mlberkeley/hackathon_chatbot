FROM ubuntu:latest
MAINTAINER mlatberkeley "ml.at.berkeley@gmail"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . ./image
WORKDIR ./image
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]