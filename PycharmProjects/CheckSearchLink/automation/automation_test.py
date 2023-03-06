import time
from collections import defaultdict

from selenium.webdriver.common.keys import Keys

from _common.msg_telegram import send_group_test
from _database.redisclient import RedisClient
from automation.selenium_driver import FireFoxDriver
from config import config, settings
from src.handle_data import handle_search_link


redis_client = RedisClient(settings.database_local)


class AutomationTest(FireFoxDriver):

    def __init__(self):
        super().__init__()

        self.list_error = []
        self.count_time_error = defaultdict(int)

    """ Đi đến telegram web"""
    def go_to_telegram(self):
        self.get_domain(settings.domain_telegram)

    """ Đi đến group test link trên telegram"""
    def go_to_group(self):
        link_group = settings.domain_group_test_link
        self.get_domain(link_group)

    """ Nếu có thông báo alert thì access """
    def click_alert(self):
        try:
            element = self.get_element(config.xpath_alert)
            self.click_to_element(element)
        except:
            pass

    """ Nhập link muốn test """
    def input_link_to_group(self, value):
        element = self.get_element(config.xpath_input_msg)
        element.send_keys(value)
        time.sleep(0.5)
        element.send_keys(Keys.ENTER)

    def chain_action(self, list_dict):
        check_unique_id = []
        self.go_to_telegram()
        """ Đợi 30 nếu chưa có cookie từng đăng nhập tele. Phải đăng nhập = tay"""
        time.sleep(30)
        self.go_to_group()
        self.click_alert()

        for data in list_dict + self.list_error:
            id_link = data['id']
            if id_link not in check_unique_id:
                if data in self.list_error:
                    self.list_error.remove(data)

                print(data)
                self.input_link_to_group(data['link'])
                time.sleep(10)

                """ Check """
                has_error = handle_search_link(self.get_source_code(), data)

                if has_error:
                    self.if_errored(data, id_link)
                else:
                    """ Nếu một lần đầu tiên lỗi lần thứ hai pass -> xóa data"""
                    if self.count_time_error[id_link] == 1:
                        try:
                            del self.count_time_error[id_link]
                        except:
                            pass

                check_unique_id.append(data['id'])

    def auto_keep_status(self, time_repeat):
        for i in range(time_repeat * 2):
            try:
                element = self.get_element(config.xpath_keep_status)
                self.click_to_element(element)
                time.sleep(1)
                self.click_to_element(element)
            except:
                pass
            time.sleep(30)

    def if_errored(self, data, id_link):
        if data not in self.list_error:
            self.list_error.append(data)
        self.count_time_error[id_link] += 1

        if self.count_time_error[id_link] > settings.ERROR_LIMITED:
            send_group_test(data['link'] + ' -----------> is Error')
            self.list_error.remove(data)
            del self.count_time_error[id_link]
