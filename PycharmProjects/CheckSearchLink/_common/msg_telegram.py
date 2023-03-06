import requests


config_bot = {
    'Mybotthongbao': {
        'token': '5918466688:AAFnVMvST56qCzR1djauAuJiI0zRZIqaMxM'
    },
    'Other_test': {
        'token': '5812056009:AAFuXXeOMwM5Vr5OeOi6Ofaz6Ac4ObwznI8'
    }
}

config_chat = {
    'fe': {
        'chat_id': "-1001808746204",
        "name": 'Cảnh báo frontend'
    },
    'Other_test': {
        'chat_id': "-684425391",
        "name": 'Test Group'
    }
}


def send_telegram(token, chat_id, msg):
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    url_request = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
    requests.request('POST', url_request, headers=headers, timeout=10)


def send_msg_warning_frontend(msg):
    token = config_bot['Mybotthongbao']['token']
    chat_id = config_chat['fe']['chat_id']
    return send_telegram(token, chat_id, msg)


def send_group_test(msg):
    token = config_bot['Other_test']['token']
    chat_id = config_chat['Other_test']['chat_id']
    return send_telegram(token, chat_id, msg)


# requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='api.telegram.org', port=443): Read timed out.
# (read timeout=10)
