import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from helper import Helper
import time


def main():
    helper = Helper()
    helper.firebase_auth()

    firefox_binary_path = helper.get_firefox_binary_path()
    driver = __load_web_whatsapp_in_firefox(firefox_binary_path)

    while True:
        try:
            first_chat = driver.find_element(By.XPATH, '//div[@role="listitem"][1]')
            first_chat.click()

            active_chat = driver.find_element(By.CSS_SELECTOR, 'div._ajyl').text

            last_log_message = Helper.read_last_message()
            lines = [line.strip() for line in active_chat.splitlines() if line.strip()]
            last_message = lines[-2] + " " + lines[-1]
            if last_message != last_log_message and Helper.check_text_in_blacklist(last_message):
                reciever = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"] div._ak8q').text
                Helper.write_log(datetime.datetime.now(), active_chat, last_message, reciever)

            time.sleep(5)
            driver.refresh()
            time.sleep(5)
        except:
            continue


def __load_web_whatsapp_in_firefox(firefox_binary_path):
    options = Options()
    options.binary_location = firefox_binary_path

    service = Service(executable_path='./geckodriver.exe')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get('https://web.whatsapp.com')
    return driver


if __name__ == "__main__":
    main()
