FROM python:3

COPY . /app
WORKDIR /app

# requirements
RUN pip install -r requirements.txt

# run
ENTRYPOINT ["python"]
CMD ["src/app.py"]
