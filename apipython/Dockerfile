FROM ubuntu:latest

# Set up system
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /app
WORKDIR /app

# requirements
RUN pip install -r requirements.txt

# run
ENTRYPOINT ["python"]
CMD ["src/app.py"]
