import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from helper import Helper


def main():
    helper = Helper()
    helper.firebase_auth()

    firefox_binary_path = helper.get_firefox_binary_path()
    driver = __load_web_whatsapp_in_firefox(firefox_binary_path)

    input('\nScan the QR code from Whatsapp Web & Open the contact which you want to track. \n\nPress Enter to continue...')
    while True:
        try:
            active_chat = driver.find_element(By.CSS_SELECTOR, 'div._ajyl').text
            last_message = Helper.read_last_log()
            if last_message != active_chat:
                if Helper.check_text_in_blacklist(active_chat):
                    reciever = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"] div._ak8q').text
                    Helper.write_log(datetime.datetime.now(), active_chat, reciever)
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
