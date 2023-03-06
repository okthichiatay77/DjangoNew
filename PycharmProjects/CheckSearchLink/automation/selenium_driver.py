from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from automation.setup import customFireFox


class FireFoxDriver:

    def __init__(self):
        self.driver = customFireFox()

    def get_domain(self, domain):
        self.driver.get(domain)

    def close_driver(self):
        self.driver.close()

    def refresh_page(self):
        self.driver.refresh()

    def get_source_code(self):
        return self.driver.page_source

    def get_title(self):
        return self.driver.title

    def get_cur_url(self):
        return self.driver.current_url

    def get_element(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def click_to_element(self, element):
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def is_element_displayed(self, element):
        return element.is_displayed()

    def switch_to_mew_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def get_element_text(self, element):
        return element.text

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_element_and_click(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

    def hover_to_element(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    def screen_shot(self, file_name):
        try:
            self.driver.save_screenshot(file_name)
        except:
            print('Khong the chup anh man hinh')
