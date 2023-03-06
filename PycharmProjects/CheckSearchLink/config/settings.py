import re


""" AUTOMATION """
PAGE_LOAD_STRATEGY = 'eager'
# eager, normal, none

IMPLICITLY_WAIT = 20
PAGE_LOAD_TIMEOUT = 300

COOKIE_FIREFOX = r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\v30qbljk.default-release"
PATH_FIREFOX = r"C:\Program Files\Mozilla Firefox\geckodriver.exe"

domain_telegram = 'https://web.telegram.org/'
domain_group_test_link = 'https://web.telegram.org/z/#-821037550'
ERROR_LIMITED = 3

""" API """
HOST_API = '192.168.20.99'
PORT_API = 8000


regex_date = re.compile(r'^[\d]{2}-[\d]{2}-[\d]{4}$')
regex_valid_datetime = re.compile(r'^[\d]{2}-[\d]{2}-[\d]{4}\s[\d]{2}:[\d]{2}:[\d]{2}$')


""" DATABASE SERVER """
config = {
    'host': '192.168.19.77',
    'port': 3001,
    'db': 1,
    'password': 'bbbsf34@45dfdfvbnvbvb3SFKKJgjs'
}

""" DATABASE LOCAL """
database_local = {
    'host': 'localhost',
    'port': 6379,
    'db': 1,
    'password': ''
}

# queue server: list TEST

name_queue_telegram = 'list_social_telegram'
name_queue_zalo = 'list_social_zalo'
name_queue_facebook = 'list_social_facebook'

# queue server: list error
name_list_error = 'list_errors'
name_queue_error = 'list_errors:queue'


header_api = {
    'x-access-tokens': 'b19060ee-7314-458d-8093-c2c3124b421f'
}

access_token_api = 'b19060ee-7314-458d-8093-c2c3124b421f'
