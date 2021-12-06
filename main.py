"""
https://platform.chaordicsystems.com/raas/v2/clients/usaflex/products/115977936
"""

import csv
import requests
import base64
import os
import json
from more_itertools import unique_everseen

PLAT_USER = os.getenv('PLAT_USER')
PLAT_PASSWORD = os.getenv('PLAT_PASSWORD')

auth = f'{PLAT_USER}:{PLAT_PASSWORD}'
auth_bytes = auth.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
PLATFORM_AUTHORIZATION = base64_bytes.decode('ascii')


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


with open('data/usaflex_raw_ids-teste.csv', 'r') as file:
    ids_list = [id[0] for id in unique_everseen(csv.reader(file))]


with open('data/usaflex_parsed_ids.csv', 'w') as parsed_file:
    write_config = csv.writer(parsed_file)

    for id in ids_list:
        is_plat_prod = is_plat_product('usaflex', id)
        print(is_plat_prod)

        if is_plat_product('usaflex', id):
            write_config.writerow([id])
