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
from selenium.webdriver.common.keys import Keys

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
cancel_deliver = 'отменить доставку'
none_actual = 'Заказ неактуален'


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
    driver.get('https://megamarket.ru/personal/profile')

    # Найти поле ввода по атрибуту inputmode="numeric"
    input_element1 = driver.find_element(By.CSS_SELECTOR, 'input[type="text"][inputmode="numeric"]')

    # Получить значение из поля ввода
    tele_num = input_element1.get_attribute('value')

    print(tele_num)

    # Найти второе поле ввода по тегу input и индексу
    input_elements = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
    second_input_element = input_elements[4]

    # Получить значение из второго поля ввода
    value = second_input_element.get_attribute('value')

    print(value)

    driver.get('https://megamarket.ru/personal/order/')

    time.sleep(10)
    
    # Найти все div-элементы с классом "order-item"
    div_elements = driver.find_elements(By.CLASS_NAME,"order-item")

    # Извлечь id из каждого div-элемента и добавить в список
    id_order = [div.get_attribute("id") for div in div_elements]

    cancel_orders = []

    for i in range(len(id_order)):
        driver.get(f'https://megamarket.ru/personal/order/view/{id_order[i - 1]}')
        time.sleep(2)
        # Найти все блоки с классом "order-delivery-details"
        order_blocks = driver.find_elements(By.CLASS_NAME, "order-delivery-details")

        # Переменная для хранения максимальной цены
        max_price = 0

        # Пустой список для хранения номеров заказов, которые нужно отменить на текущей странице
        page_cancel_orders = []

        # Проход по каждому блоку
        for block in order_blocks:
            # Получить цену и номер заказа из текущего блока
            price_element = block.find_element(By.CLASS_NAME, "order-goods-list__item-price")
            price = float(price_element.text.replace(" ₽", "").replace(" ", "").replace(",", "."))
            
            order_id_element = block.find_element(By.CLASS_NAME, "order-delivery-details__id")
            order_id = order_id_element.text.replace("№ ", "").replace(" ", "")
            
            # Если цена текущего блока выше максимальной цены, обновить максимальную цену и добавить номер заказа в список
            if price > max_price:
                max_price = price
                page_cancel_orders = [order_id]
            # Если цена текущего блока равна максимальной цене, добавить номер заказа в список
            elif price == max_price:
                page_cancel_orders.append(order_id)

        # Добавить номера заказов со страницы в общий список
        cancel_orders.extend(page_cancel_orders)

    print("NUMBERS OF ORDERS TO CANCEL:", cancel_orders)

    print(cancel_orders)

    operator1 = 'оператор'
    operator2 = 'оператор'
    message_to_operator = f'Хотел бы отменить доставки: {", ".join(cancel_orders)}'
    second_message_to_operator = f'Причина: передумал'
    third_message_to_operator = f'Александр Мершин, {tele_num}, {value}'
    accept = 'Да'


    time.sleep(5)
    driver.get('https://megamarket.ru/help/article/168953374/')
    time.sleep(5)
    # Находим кнопку по классу
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'btn-link'))
    )

    # Нажимаем на кнопку
    button.click()

    time.sleep(10)

    # Найти поле ввода сообщения
    message_input = driver.find_element(By.CSS_SELECTOR, '.webim-message-area')

    # Очистить поле ввода сообщения (на всякий случай)
    message_input.clear()

    # Ввести текст из переменной cancel_deliver
    message_input.send_keys(operator1)

    # Нажать клавишу Enter
    message_input.send_keys(Keys.ENTER)

    time.sleep(15)

    # Ввести текст из переменной cancel_deliver
    message_input.send_keys(operator2)

    # Нажать клавишу Enter
    message_input.send_keys(Keys.ENTER)

    time.sleep(15)

    # Ввести текст из переменной cancel_deliver
    message_input.send_keys(message_to_operator)

    # Нажать клавишу Enter
    message_input.send_keys(Keys.ENTER)

    time.sleep(10)

    message_input.send_keys(second_message_to_operator)

    message_input.send_keys(Keys.ENTER)

    time.sleep(2)

    message_input.send_keys(third_message_to_operator)

    message_input.send_keys(Keys.ENTER)

    time.sleep(6)

    message_input.send_keys(accept)

    message_input.send_keys(Keys.ENTER)

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
            time.sleep(5)

if __name__ == "__main__":
    main()