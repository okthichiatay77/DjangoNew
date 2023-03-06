import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from config.settings import COOKIE_FIREFOX, PATH_FIREFOX, PAGE_LOAD_STRATEGY, IMPLICITLY_WAIT, PAGE_LOAD_TIMEOUT

chromedriver_autoinstaller.install()


def customFireFox():
    myprofile = webdriver.FirefoxProfile(COOKIE_FIREFOX)
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = PAGE_LOAD_STRATEGY
    driver = webdriver.Firefox(firefox_profile=myprofile, executable_path=PATH_FIREFOX, options=options)
    driver.implicitly_wait(IMPLICITLY_WAIT)
    driver.maximize_window()
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    return driver


def customChrome():
    option = Options()
    option.page_load_strategy = PAGE_LOAD_STRATEGY
    option.add_argument("--enable-extensions")
    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(100)
    driver.maximize_window()
    return driver
