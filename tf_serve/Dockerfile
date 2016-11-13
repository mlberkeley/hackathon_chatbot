FROM tensorflow/tensorflow

COPY . ./image
WORKDIR ./image
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]