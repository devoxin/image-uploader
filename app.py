import json
import os
import random
import re

from flask import Flask, render_template, request

# Configurable Options
debug = False
include_port = False
storage = os.path.basename('files')
port = 8080
domain = 'http://localhost'  # Include subdomain if required

if debug or include_port:
    domain += f':{port}'

app = Flask(__name__)
extension_regex = re.compile("\.[a-z0-9]+$", re.IGNORECASE)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        attachment = request.files.get('image', None)

        if not attachment:
            return json.dumps({'status': 400, 'error': 'Missing file "attachment"'}), 200

        extension = extension_regex.match(attachment.filename)

        file_ext = extension.group().lower() if extension else '.png'
        file_name = generate_hex() + file_ext
        file_path = os.path.join(storage, file_name)
        attachment.save(file_path)

        return json.dumps({'status': 200, 'url': f'{domain}/{file_name}'}), 200


def generate_hex(length=10):  # Defaults to 10
    return f"%0{length}x" % random.randrange(16**length)


if __name__ == '__main__':
    if debug:
        app.run(port=port)
    else:
        app.run(host='0.0.0.0', port=port)
