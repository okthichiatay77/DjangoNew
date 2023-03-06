from api import get_api_data_json
from automation.automation_test import AutomationTest

time_repeat = 5
type_test = 'social-telegram'


def main():
    auto_test = AutomationTest()
    while True:
        print('----------------------------- Start: Test search link -----------------------------------')
        list_dict = get_api_data_json(type_test)
        auto_test.chain_action(list_dict)
        result = auto_test.list_error
        print(result)
        print('----------------------------------- End: Test -------------------------------------------')
        auto_test.auto_keep_status(time_repeat)


if __name__ == '__main__':
    main()
