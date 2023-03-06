import json
from functools import wraps

from flask import Flask, jsonify, request

from _common.common import check_validate_input_user, save_data_to_database_server, convert_database_to_data,\
    dequeue_all_data_in_database
from config.settings import HOST_API, PORT_API, config, access_token_api

app = Flask(__name__)
app.config['SECRET_KEY'] = access_token_api


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({
                'status': False,
                'message': 'a valid token is missing'
            }), 401
        if token == app.config['SECRET_KEY']:
            pass
        else:
            return jsonify({
                "status": False,
                "message": "Token is invalid"
            }), 401

        return f(*args, **kwargs)

    return decorator


@app.route('/cd/recheck/push', methods=['PUT'])
@token_required
def valid_search_social():
    if request.method == 'PUT':
        record = json.loads(request.data)
        result_msg = check_validate_input_user(record)
        if result_msg:
            result = {
                'status': False,
                'message': result_msg
            }
            return jsonify(result), 401

        result = {
            'status': True,
            "message": 'Success',
            "data": record['data']
        }
        """ save to database """
        save_data_to_database_server(record, config)
        return jsonify(result)

    return jsonify({
        'status': False,
        'message': ""
    }), 401


@app.route('/cd/recheck/get/<string:type_data>', methods=['GET'])
@token_required
def get_search_link(type_data):
    if type_data != 'social-telegram' and type_data != 'social-zalo' and type_data != 'social-facebook':
        result = {
            'status': False,
            'msg': 'bạn chỉ được lấy ba loại: social-telegram, social-zalo, social-facebook'
        }
        return jsonify(result), 401

    # list_ids, record = convert_database_to_data(config, type_data)
    list_ids, record = dequeue_all_data_in_database(config, type_data)
    length = len(record)
    result = {
        'status': True,
        'msg': 'Success',
        'count': length,
        'data': record
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(host=HOST_API, port=PORT_API, debug=True)
