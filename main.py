import csv
import os
from more_itertools import unique_everseen
from flask import Flask, render_template, request
from utils import get_plat_product
from dotenv import load_dotenv

load_dotenv()
PLAT_USER = os.getenv('PLAT_USER')
PLAT_PASSWORD = os.getenv('PLAT_PASSWORD')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    parsed_list = []
    sanitized = 0

    file = request.files.get("file")
    apikey = request.form.get('apikey')

    filename = file.filename
    file.save(os.path.join('static', filename))

    with open(f'static/{filename}', 'r') as input_file:
        unique_list = [id[0] for id in unique_everseen(csv.reader(input_file))]

    with open(f'static/output-{filename}', 'w') as output_file:
        write_config = csv.writer(output_file)

        for id in unique_list:
            product = get_plat_product(apikey, id, PLAT_USER, PLAT_PASSWORD)

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
    app.run(debug=True, host='0.0.0.0')
