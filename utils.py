import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException

import constants


DOM_WAIT_TIMEOUT = 10

def driver_start():
    """
    selenium driver 실행
    """
    mobile_emulation = {
        "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    }

    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    # 사람처럼 보이게 하는 옵션들
    options.add_argument("disable-gpu")   # 가속 사용 x
    options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
    options.headless = True

    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
    driver.get(constants.URL_MAIN)

    return driver


def get_element(driver, by, value, timeout=int(DOM_WAIT_TIMEOUT)):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)), 'Timed out waiting for getting element')


def button_click(driver, by, value, timeout=int(DOM_WAIT_TIMEOUT)):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)), 'Timed out waiting for button {}'.format(value)).send_keys(Keys.ENTER)


def input_field(driver, id, input_value):
    """
    id의 input Element에 input_value 입력
    """
    elem = get_element(driver, By.ID, id)
    elem.send_keys(input_value)
    if input_value != elem.get_attribute('value'):
        time.sleep(2)


def confirm_alert(driver):
    time.sleep(2)
    try:
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        pass
