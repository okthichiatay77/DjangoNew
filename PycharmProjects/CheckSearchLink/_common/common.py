import ast
import json

from _database.redisclient import RedisQueues, RedisClient
from config.settings import regex_valid_datetime, name_queue_telegram, name_queue_zalo, name_queue_facebook


def get_name_queue(type_data):
    if type_data.lower() == 'social-telegram':
        return name_queue_telegram
    elif type_data.lower() == 'social-zalo':
        return name_queue_zalo
    elif type_data.lower() == 'social-facebook':
        return name_queue_facebook


def check_validate_input_user(dictionary):
    msg_error = []
    try:
        channel = dictionary['channel']
        data = dictionary['data']
    except:
        msg_error.append('Input của bạn phải có 3 trường: id, channel, data')
    else:
        if not isinstance(channel, str):
            msg_error.append('Trường channel của bạn phải là dạng chuỗi')
        elif channel == '':
            msg_error.append('Trường channel của bạn không được để trống')

        if (not isinstance(data, list)) and (not isinstance(data, dict)):
            msg_error.append('data của bạn phải là dạng list hoặc dict')
        elif data == [] or data == {}:
            msg_error.append('Trường data của bạn không được để trống')

        for row in data:
            try:
                id = row['id']
                title = row['title']
                link = row['link']
                action = row['action']
                time_action = row['time_action']
                type_data = row['type']
            except:
                msg_error.append('Bắt buộc có 6 trường: id, title, link, time_action, action, type')
            else:
                if not isinstance(id, str):
                    msg_error.append('Data: trường id phải dạng chuỗi số')
                elif id == '':
                    msg_error.append('Data: trường id không được để trống')

                if not isinstance(title, str):
                    msg_error.append('Data: Trường title phải là dạng chuỗi')
                elif title == '':
                    msg_error.append('Data: trường title không được để trống')

                if not isinstance(link, str):
                    msg_error.append('Data: Trường link phải là dạng chuỗi')
                elif link == '':
                    msg_error.append('Data: trường link không được để trống')

                if not isinstance(action, str):
                    msg_error.append('Data: Trường action phải là dạng chuỗi')
                elif (action != 'insert') and (action != 'update') and (action != 'delete'):
                    msg_error.append('Data: Trường action chỉ có 3 trạng thái: insert, update, delete')

                if not isinstance(time_action, str):
                    msg_error.append('Data: Trường time_action phải là dạng chuỗi')
                elif not regex_valid_datetime.match(time_action):
                    msg_error.append('Data: Trường time_action phải theo format: %d-%m-%Y %H:%M:%S')

                if (not isinstance(type_data, str)) and (not isinstance(type_data, list)):
                    msg_error.append('Data: Trường type phải là dạng chuỗi, hoặc list')
                elif isinstance(type_data, str):
                    if type_data != 'social-telegram' and type_data != 'social-zalo' and type_data != 'social-facebook':
                        msg_error.append('Data: type chỉ có 3 loại: social-telegram, social-zalo, social-facebook')

    return msg_error


def save_data_to_database_server(record, config):
    redis_queue_tele = RedisQueues(name_queue_telegram, 'queue', config)
    redis_queue_zalo = RedisQueues(name_queue_zalo, 'queue', config)
    redis_queue_facebook = RedisQueues(name_queue_facebook, 'queue', config)
    redis_client = RedisClient(config)

    for data in record['data']:
        id_data = data['id']
        type_data = data['type']
        string_json = convert_dict_to_string_json(data)

        if isinstance(type_data, str):
            if type_data.lower() == 'social-telegram':
                save_social_link_to_database_telegram(redis_queue_tele, redis_client, string_json, id_data)
            elif type_data.lower() == 'social-zalo':
                save_social_link_to_database_zalo(redis_queue_zalo, redis_client, string_json, id_data)
            elif type_data.lower() == 'social-facebook':
                save_social_link_to_database_facebook(redis_queue_facebook, redis_client, string_json, id_data)
        elif isinstance(type_data, list):
            for Type in type_data:
                if Type.lower() == 'social-telegram':
                    save_social_link_to_database_telegram(redis_queue_tele, redis_client, string_json, id_data)
                elif Type.lower() == 'social-zalo':
                    save_social_link_to_database_zalo(redis_queue_zalo, redis_client, string_json, id_data)
                elif Type.lower() == 'social-facebook':
                    save_social_link_to_database_facebook(redis_queue_facebook, redis_client, string_json, id_data)


def convert_database_to_data(config, type_data):
    """ Lấy dữ liệu từ database và chuyển element thành dạng dict của python """
    name_queue = get_name_queue(type_data)
    redis_queue = RedisQueues(name_queue, 'queue', config)
    redis_client = RedisClient(config)
    list_ids = []
    for value in redis_client.list_full_item(name_queue):
        list_ids.append(convert_string_json_to_dict(value))

    list_dict = []
    for item in redis_queue.get_all_item():
        list_dict.append(convert_string_json_to_dict(item))

    return list_ids, list_dict


def dequeue_all_data_in_database(config, type_data):
    """ Lấy dữ liệu theo dạng queue từ database và chuyển element thành dạng dict của python """
    namequeue = get_name_queue(type_data)
    redis_queue = RedisQueues(namequeue, 'queue', config)
    redis_client = RedisClient(config)
    list_ids = []
    for value in redis_client.list_full_item(namequeue):
        redis_client.list_remove(namequeue, value)
        list_ids.append(convert_string_json_to_dict(value))

    list_dict = []
    for item in redis_queue.get_all_item():
        redis_queue.dequeue(item)
        list_dict.append(convert_string_json_to_dict(item))

    return list_ids, list_dict


def get_data_of_database(config):
    """ Lấy dữ liệu từ database vẫn dạng byte """
    rd = RedisQueues(name_queue_telegram, 'queue', config)
    rd1 = RedisClient(config)
    list_ids = []
    for x in rd1.list_full_item(name_queue_telegram):
        list_ids.append(x)

    list_dict = []
    for i in rd.get_all_item():
        list_dict.append(i)

    return list_ids, list_dict


def save_social_link_to_database_telegram(redis_queue_tele, redis_client, string_json, id_data):
    if bytes(id_data, 'utf-8') in redis_client.list_full_item(name_queue_telegram):
        for row in redis_queue_tele.get_all_item():
            if id_data in str(row):
                redis_queue_tele.dequeue(row)
                break

    redis_client.list_push(name_queue_telegram, id_data)
    redis_queue_tele.enqueue(string_json)


def save_social_link_to_database_zalo(redis_queue_zalo, redis_client, string_json, id_data):
    if bytes(id_data, 'utf-8') in redis_client.list_full_item(name_queue_zalo):
        for row in redis_queue_zalo.get_all_item():
            if id_data in str(row):
                redis_queue_zalo.dequeue(row)
                break

    redis_client.list_push(name_queue_zalo, id_data)
    redis_queue_zalo.enqueue(string_json)


def save_social_link_to_database_facebook(redis_queue_facebook, redis_client, string_json, id_data):
    if bytes(id_data, 'utf-8') in redis_client.list_full_item(name_queue_facebook):
        for row in redis_queue_facebook.get_all_item():
            if id_data in str(row):
                redis_queue_facebook.dequeue(row)
                break

    redis_client.list_push(name_queue_facebook, id_data)
    redis_queue_facebook.enqueue(string_json)


""" Convert """
def convert_string_json_to_dict(string):
    if isinstance(string, dict):
        return string
    return ast.literal_eval(string.decode('utf-8'))


def convert_dict_to_string_json(dict):
    return json.dumps(dict, ensure_ascii=False, sort_keys=True)


def subtract_between_datetime_to_second(old_time, new_time):
    return int((new_time - old_time).total_seconds())
