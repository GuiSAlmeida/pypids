import requests
import json
import base64


def make_plat_auth(user, password):
    auth_str = f'{user}:{password}'
    auth_bytes = auth_str.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    plat_authorization = base64_bytes.decode('ascii')
    return f'Basic {plat_authorization}'


def get_plat_product(apikey, id, user, password):
    ENDPOINT = f'https://platform.chaordicsystems.com/raas/v2' \
        f'/clients/{apikey}/products/{id}'

    plat_authorization = make_plat_auth(user, password)

    try:
        response = requests.get(
            ENDPOINT,
            headers={'Authorization': plat_authorization}
        )
        return json.loads(response.text)

    except Exception as e:
        print(f'Error on get_plat_product: {e}')
        return {}
