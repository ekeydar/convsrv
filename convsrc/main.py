from flask import Flask, Response


from .local_settings import *
DEBUG = False
KEY = None

app = Flask(__name__)

@app.route('/api/conv/', methods=['POST'])
def conv():
    pass

if __name__ == '__main__':
    app.run(debug=DEBUG)



