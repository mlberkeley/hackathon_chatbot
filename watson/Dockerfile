FROM ubuntu:latest
MAINTAINER ML[At]B "ml.at.berkeley@gmail"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . ./image
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["setup.py"]