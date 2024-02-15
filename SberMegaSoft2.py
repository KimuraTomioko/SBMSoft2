from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import pandas as pd
from gologin import GoLogin
from gologin import getRandomPort
import http.client
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

name = 'Александр'
surname = 'Мершин'
birth_date = '30072002'
password = 'Vasgen43!'
link_first_product = 'https://megamarket.ru/catalog/details/stiralnaya-mashina-uzkaya-indesit-iwsd-5085-cis--100000042634_19808/'
link_second_product = 'https://megamarket.ru/catalog/details/kronshteyn-tvek-rifar-63-shtyrevoy-ploskiy-100063091775/#?related_search=%D0%BA%D1%80%D0%BE%D0%BD%D1%88%D1%82%D0%B5%D0%B9%D0%BD'
link_multicart = 'https://megamarket.ru/multicart/'
address = 'Москва, 3-я Парковая улица, 54 к2'
comment ='контактный номер телефона +7(926) 046-73-13'
promo_code = 'EZ'
real_phone = '9260461312'

def get_profile_ids():
    conn = http.client.HTTPSConnection("api.gologin.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWE4MWEyODc3ZWYzOGIyMGFkNTQ2NGEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWFlMGI0NGQ4OTUzYWQ4MmU0NGUyM2EifQ.dr4Y6SGw6TnpsLMCnl4yTgvmDszSjUwViVKMJsX5wYg',
      'Content-Type': 'application/json'
    }
    conn.request("GET", "/browser/v2", payload, headers)
    res = conn.getresponse()
    data = res.read()

    # Преобразование JSON-строки в словарь Python
    response_data = json.loads(data.decode("utf-8"))

    # Получение списка профилей
    profiles = response_data.get("profiles", [])

    # Извлечение значений id из каждого профиля
    profile_ids = [profile.get("id") for profile in profiles]

    return profile_ids


def open_browser(profile_id):
    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWE4MWEyODc3ZWYzOGIyMGFkNTQ2NGEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWFlMGI0NGQ4OTUzYWQ4MmU0NGUyM2EifQ.dr4Y6SGw6TnpsLMCnl4yTgvmDszSjUwViVKMJsX5wYg",
        "profile_id": profile_id
    })

    debugger_address = gl.start()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
    return driver, gl

def login_to_megamarket(driver):
    driver.get('https://megamarket.ru/')
    wait = WebDriverWait(driver, 1200)
    wait.until(EC.url_to_be('https://megamarket.ru/'))
    time.sleep(5)
    driver.get(link_first_product)
    time.sleep(10)

    try:
        # Ждем, пока кнопка станет кликабельной
        buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="catalog-buy-button__button btn lg"]'))
        )

        # Нажимаем на кнопку с помощью JavaScript
        driver.execute_script("arguments[0].click();", buy_button)
    except Exception as e:
        print('Product is already bought!!!')
    finally:
        driver.get(link_second_product)

    time.sleep(10)

    try:
        # Ждем, пока кнопка станет кликабельной
        second_buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="catalog-buy-button__button btn lg"]'))
        )

        # Нажимаем на кнопку с помощью JavaScript
        driver.execute_script("arguments[0].click();", second_buy_button)
    except Exception as e:
        print('Product is already bought!!!')
    finally:
        # Открытие страницы
        driver.get("https://megamarket.ru/multicart/")


    checkout_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-checkout")))

    # Нажатие на кнопку
    checkout_button.click()

    time.sleep(10)
    
    try:
        # Ждем, пока кнопка станет кликабельной
        later_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-link btn-block checkout-sber-wallet__decline xl"]'))
        )

        driver.execute_script("arguments[0].click();", later_button)
    except Exception as e:
        print('Didnt find')
    finally:
        time.sleep(10)
    
    address_input = wait.until(EC.visibility_of_element_located((By.NAME, "address-string")))
    address_input.clear()
    address_input.send_keys(address)

    time.sleep(5)

    comment_textarea = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea.text-input.xl")))
    comment_textarea.clear()
    comment_textarea.send_keys(comment)

    time.sleep(5)

    promo_code_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.text-input.fix-label.sm")))
    promo_code_input.clear()
    promo_code_input.send_keys(promo_code)

    time.sleep(5)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="SberPay"]')))

    # Нажатие на кнопку
    button.click()

    time.sleep(5)

    pay_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "sber-pay-button__submit")]'))
    )

    # Нажимаем на кнопку
    pay_button.click()

    time.sleep(10)
    
    # Найти поле ввода
    phone_input = driver.find_element(By.XPATH, '//input[contains(@class, "text-input")]')

    # Кликнуть на поле ввода, чтобы убедиться, что оно активно
    phone_input.click()

    # Очистить поле ввода
    phone_input.clear()
    
    # Кликнуть на поле ввода, чтобы убедиться, что оно активно
    phone_input.click()

    # Ввести данные из переменной real_phone
    phone_input.send_keys(real_phone)

    time.sleep(5)

    # Найти кнопку
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "submit-button__button-spinner-container")]'))
    )

    # Нажать на кнопку
    submit_button.click()
    time.sleep(5)


def main():
    profile_ids = get_profile_ids()

    for profile_id in profile_ids:
        driver, gl = open_browser(profile_id)

        try:
            login_to_megamarket(driver)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            driver.quit()
            gl.stop()
            time.sleep(3)

if __name__ == "__main__":
    main()
