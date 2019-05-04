from os import getenv

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world from Python'


if __name__ == '__main__':
    port = getenv('PORT', "8080")

    app.run(host='0.0.0.0', port=int(port))
