import requests
import json
from datetime import datetime
from config.settings import header_api, HOST_API, PORT_API
from _common.common import save_data_to_database_server, dequeue_all_data_in_database
from config.settings import database_local
from _database.redisclient import RedisQueues


def call_api(method, url, header, result='json'):
    data = requests.request(method, url=url, headers=header)

    if result == 'json':
        return data.json()
    elif result == 'status':
        return data.status_code
    elif result == 'content':
        return data.content
    elif result == 'text':
        return data.text


def get_api_data_json(type_test):
    url = f'http://{HOST_API}:{PORT_API}/cd/recheck/get/' + type_test
    data = call_api('GET', url, header_api, 'json')
    save_data_to_database_server(data, database_local)
    list_ids, list_dict = dequeue_all_data_in_database(database_local, type_test)

    return list_dict[::-1]


def push_data_error_to_server(list_error):
    url = f"http://{HOST_API}:{PORT_API}/cd/valid-search-social/push/list-error"
    list_data = {
        "channel": "channel",
        "data": []
    }
    for data in list_error:
        data['time_error'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        list_data["data"].append(data)

    payload = json.dumps(list_data)
    headers = {
        'x-access-tokens': 'b19060ee-7314-458d-8093-c2c3124b421f',
        'Content-Type': 'application/json'
    }

    requests.request("PUT", url, headers=headers, data=payload)
