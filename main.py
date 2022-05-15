import json
import logging
import time
from datetime import datetime, timezone
import urllib.request
import urllib.error
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils import driver_start, input_field, button_click, get_element, confirm_alert
import constants

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)

def main():
    try:
        with open("settings.json") as f:
            settings = json.load(f)

        driver = driver_start()
        
        logger.info('로그인')
        input_field(driver, constants.ID_USERID_INPUT, settings['userid'])
        input_field(driver, constants.ID_PASSWORD_INPUT, settings['password'])
        button_click(driver, By.ID, constants.ID_LOGIN_BUTTON)
        driver.get(constants.URL_TICKET_PAGE.format(settings['ticket_code']))

        waiting_reservation_time(settings)

        # 날짜 선택창으로 이동
        button_click(driver, By.ID, constants.ID_BUY_BUTTON)
        confirm_alert(driver)
        driver.switch_to.window(driver.window_handles[1])
        
        select_date(driver, settings['ticket_date'])
        find_seat(driver, settings["ticket_type"])

        logger.info('좌석 가격 선택')
        button_click(driver, By.CLASS_NAME, constants.CLASS_COUNTUP)
        btn = get_element(driver, By.CLASS_NAME, constants.CLASS_NEXT_STEP)
        if not btn.text == '결제방식 선택':
            # 버튼 클릭이 제대로 안된 경우 재시도
            time.sleep(1)
            button_click(driver, By.CLASS_NAME, constants.CLASS_COUNTUP)
        click_next_button(driver)
        
        logger.info('걸제 수단 무통장입금으로 선택')
        btn_other_wrapper = get_element(driver, By.CLASS_NAME, constants.CLASS_OTHERPAY)
        btn_other = btn_other_wrapper.find_element_by_xpath('.//div[@role="button"]')
        btn_other.send_keys(Keys.ENTER)

        logger.info('무통장 입금 은행 신한은행으로 선택')
        btn_bank = get_element(driver, By.XPATH, constants.XPATH_BTN_BANK)
        driver.execute_script("arguments[0].click();", btn_bank)
        # 동의하기
        allcheck_wrapper = get_element(driver, By.CLASS_NAME, 'allChk')
        allcheck = allcheck_wrapper.find_element_by_xpath('.//i')
        driver.execute_script("arguments[0].click();", allcheck)

        logger.info('최종 결제 버튼 클릭')
        try:
            click_next_button(driver)
            get_element(driver, By.CLASS_NAME, constants.CLASS_RESERVATION_NUMBER) 
        except Exception as error:
            # 에러 발생하면 alert 끄고 다시 한번 시도
            logger.info("결제 오류로 인한 재시도: {}".format(error))
            confirm_alert(driver)
            click_next_button(driver)
            get_element(driver, By.CLASS_NAME, constants.CLASS_RESERVATION_NUMBER) 

        logger.info('결과 페이지 다운로드')
        driver.save_screenshot("screenshot.png")

    except Exception as error:
        logger.error("ERROR: {}".format(error))


def waiting_reservation_time(settings):
    """
    예약 시간까지 기다리다가 예약시간이 되면 예약 버튼 클릭
    """
    # 예약 시간에 맞춰서 동작
    reservation_time = settings["reservation_time"]
    if reservation_time:
        reservation_timestamp = datetime.strptime(reservation_time, '%Y.%m.%d %H:%M:%S').timestamp()
        logger.info('예약 대기')
        while reservation_timestamp > get_server_time():
            time.sleep(1)
    logger.info('예약 시작')


def select_date(driver, ticket_date):
    """
    티켓 날짜 선택
    """
    logger.info('날짜 선택')
    try:
        month = get_element(driver, By.CLASS_NAME, constants.CLASS_MONTH)
        if int(month.text.split('.')[1]) < int(ticket_date.split('.')[1]):
            button_click(driver, By.CLASS_NAME, constants.CLASS_DATE_RIGHT_BUTTON)
            month = get_element(driver, By.CLASS_NAME, constants.CLASS_MONTH)
            if int(month.text.split('.')[1]) != int(ticket_date.split('.')[1]):
                time.sleep(1)

        calendar = get_element(driver, By.CLASS_NAME, constants.CLASS_CALENDAR_ACTIVE)
        
        date_list = calendar.find_elements(By.TAG_NAME, "button")
        for date in date_list:
            if int(date.text) == int(ticket_date.split('.')[2]):
                date.send_keys(Keys.ENTER)
                break

        button_click(driver, By.CLASS_NAME, constants.CLASS_DATE_CHOICE)
    except Exception as error:
        logger.error('Error(select_date): {}'.format(error))
        raise Exception("원하는 날짜 선택을 실패했습니다")


def find_seat(driver, seat_type):
    """
    seat_type: VIP, R, S
    """
    logger.info('좌석 선택')
    try:
        button_click(driver, By.XPATH, '//a[contains(@title,"{}석")]'.format(seat_type))
    except Exception as error:
        logger.error('Error(find_seat): {}'.format(error))
        raise Exception("좌석을 찾지 못했습니다")
    
    button_click(driver, By.ID, constants.ID_SEATS_BUTTON)


def click_next_button(driver):
    btn_wrapper = get_element(driver, By.CLASS_NAME, constants.CLASS_NEXT_STEP)
    btn = btn_wrapper.find_element_by_xpath('.//a')
    driver.execute_script("arguments[0].click();", btn)


def get_server_time():
    """
    인터파크 서버 시간 불러오기
    """
    date = urllib.request.urlopen(constants.URL_MAIN).headers['Date']
    date_time = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
    
    return date_time.timestamp()


if __name__ == "__main__":
    main()