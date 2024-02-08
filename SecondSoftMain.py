from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

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

def open_browser():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_megamarket(driver, phone):
    driver.get("https://megamarket.ru/login/")
    time.sleep(7)
    login_button = driver.find_element(By.CLASS_NAME, "auth-main__phone-login")
    login_button.click()
    time.sleep(5)
    phone_input = driver.find_element(By.CLASS_NAME, "text-input")
    phone_input.send_keys(phone)
    time.sleep(15)
    get_code_button = driver.find_element(By.CLASS_NAME, "login-form__submit")
    get_code_button.click()
    wait = WebDriverWait(driver, 1200)
    wait.until(EC.url_to_be('https://megamarket.ru/'))
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
    address_input.send_keys(address)

    time.sleep(5)

    comment_textarea = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea.text-input.xl")))
    comment_textarea.send_keys(comment)

    time.sleep(5)

    promo_code_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.text-input.fix-label.sm")))
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

    # Очистить поле ввода
    phone_input.clear()

    # Ввести данные из переменной real_phone
    phone_input.send_keys(real_phone)

    time.sleep(10)

    # Найти кнопку
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "submit-button__button-spinner-container")]'))
    )

    # Нажать на кнопку
    submit_button.click()

    time.sleep(10)

def main():
    
    phone = '9384293264'
    driver = open_browser()

    try:
        login_to_megamarket(driver, phone)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()