import requests
from bs4 import BeautifulSoup

from config import config


def handle_search_link(source_code, data):
    if data['action'] == 'delete':
        has_error = check_status_delete(data)
    else:
        has_error = check_status_insert_or_update(source_code, data)
    return has_error


def check_status_delete(data):
    link = data['link']
    status = requests.request('HEAD', link).status_code
    if status == 200:
        return True
    return False


def check_status_insert_or_update(source_code, data):
    check = None
    soup = BeautifulSoup(source_code, 'html.parser')

    check_1 = soup.find('div', attrs={'class': config.class_div_check})
    check_2 = soup.find('div', attrs={'class': config.class_div_check_2})

    if check_1:
        check = check_1
    elif check_2:
        check = check_2

    try:
        title = check.find('p', attrs={'class': config.class_title})
        description = check.find('p', attrs={'class': config.class_description})
        link = check.find('a', attrs={'class': config.class_main_domain})
    except:
        return True
    else:
        if not title:
            return True
        elif not link:
            return True
        elif not description:
            return True

    return False

