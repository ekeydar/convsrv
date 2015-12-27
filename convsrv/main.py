import os.path
import tempfile

from PIL import Image
from flask import Flask, Response, request, send_file
import logging

DEBUG = False
KEY = None
HOST=None
PORT=None

try:
    from local_settings import *
except ImportError:
    pass

app = Flask(__name__)


@app.route('/')
def home():
    return 'HELLO'


@app.route('/api/conv/', methods=['POST'])
def api_conv():
    if KEY:
        key = request.form['key']
        if key != KEY:
            return Response(status=403)
    source_file = request.files['source']
    from_ext = os.path.splitext(source_file.filename)[1]
    to_ext = '.' + request.form['to']
    from_fid, from_fname = tempfile.mkstemp(suffix=from_ext)
    to_fid, to_fname = tempfile.mkstemp(suffix=to_ext)
    os.close(from_fid)
    os.close(to_fid)
    source_file.save(from_fname)
    conv(from_fname, to_fname)
    resp = send_file(to_fname)
    os.unlink(to_fname)
    os.unlink(from_fname)
    return resp


def conv(from_fname, to_fname):
    img = Image.open(from_fname)
    img.load()
    img.save(to_fname)


app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(logging.StreamHandler())

app.logger.info('DEBUG = %s',DEBUG)
app.logger.info('KEY = %s',KEY)

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
