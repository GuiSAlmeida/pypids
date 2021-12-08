"""
https://platform.chaordicsystems.com/raas/v2/clients/usaflex/products/115977936
"""

import csv
import os
from more_itertools import unique_everseen
from flask import Flask, render_template, request
from utils import get_plat_product, make_auth
from dotenv import load_dotenv

load_dotenv()
PLAT_USER = os.getenv('PLAT_USER')
PLAT_PASSWORD = os.getenv('PLAT_PASSWORD')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def add():
    file = request.files.get("file")
    apikey = request.form.get('apikey')
    parsed_list = []
    sanitized = 0
    plat_authorization = make_auth(PLAT_USER, PLAT_PASSWORD)

    filename = file.filename
    file.save(os.path.join('data', filename))

    with open(f'data/{filename}', 'r') as file:
        ids_list = [id[0] for id in unique_everseen(csv.reader(file))]

    with open(f'output/{filename}.csv', 'w') as parsed_file:
        write_config = csv.writer(parsed_file)
        for id in ids_list:
            product = get_plat_product(apikey, id, plat_authorization)
            if 'status' in product and 'AVAILABLE' in product['status']:
                write_config.writerow([id])
                parsed_list.append(id)
            else:
                sanitized += 1

    return render_template(
        'list.html',
        apikey=apikey,
        list=parsed_list,
        list_len=len(parsed_list),
        sanitazed=sanitized
    )


if __name__ == "__main__":
    app.run(debug=True)
