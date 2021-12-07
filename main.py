"""
https://platform.chaordicsystems.com/raas/v2/clients/usaflex/products/115977936
"""

import csv
import requests
import base64
import os
import json
from more_itertools import unique_everseen
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

PLAT_USER = os.getenv('PLAT_USER')
PLAT_PASSWORD = os.getenv('PLAT_PASSWORD')

auth_str = f'{PLAT_USER}:{PLAT_PASSWORD}'
auth_bytes = auth_str.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
PLATFORM_AUTHORIZATION = base64_bytes.decode('ascii')

app = Flask(__name__)


def is_plat_product(apikey, id):
    try:
        ENDPOINT = f'https://platform.chaordicsystems.com/raas/v2' \
            f'/clients/{apikey}/products/{id}'
        response = requests.get(
            ENDPOINT,
            headers={'Authorization': f'Basic {PLATFORM_AUTHORIZATION}'}
        )
        response_dict = json.loads(response.text)

        if 'AVAILABLE' in response_dict['status']:
            return True

    except Exception as e:
        print(f'Error on get_classes: {e}')
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    file = request.files.get("file")
    apikey = request.form.get('apikey')

    filename = file.filename
    file.save(os.path.join('data', filename))

    with open(f'data/{filename}', 'r') as file:
        ids_list = [id[0] for id in unique_everseen(csv.reader(file))]

    with open(f'output/{filename}.csv', 'w') as parsed_file:
        write_config = csv.writer(parsed_file)
        parsed_list = []
        for id in ids_list:
            if is_plat_product(apikey, id):
                write_config.writerow([id])
                parsed_list.append(id)

    return render_template('list.html', apikey=apikey, list=parsed_list)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
