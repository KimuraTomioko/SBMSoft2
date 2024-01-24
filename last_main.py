from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from gologin import GoLogin
from gologin import getRandomPort
from selenium.webdriver.chrome.service import Service

name = 'Александр'
surname = 'Мершин'
birth_date = '30072002'
password = 'Vasgen43!'


def open_browser(phone):
    profile_creating = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWE4MWEyODc3ZWYzOGIyMGFkNTQ2NGEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWFlMGI0NGQ4OTUzYWQ4MmU0NGUyM2EifQ.dr4Y6SGw6TnpsLMCnl4yTgvmDszSjUwViVKMJsX5wYg",
    })

    profile_id = profile_creating.create({
        "name": f'profile_{phone}',
        "os": 'mac',
        "navigator": {
            "language": 'en-US',
            "userAgent": 'random',
            "resolution": '1024x768',
            "platform": 'mac',
        },
        'proxy': {
            'mode': 'none', # Specify 'none' if not using proxy
            'autoProxyRegion': 'us' 
            # "host": '',
            # "port": '',
            # "username": '',
            # "password": '',
        },
        "webRTC": {
            "mode": "alerted",
            "enabled": True,
        },
        "storage": {
            "local":        True,   # Local Storage is special browser caches that websites may use for user tracking in a way similar to cookies. 
                                    # Having them enabled is generally advised but may increase browser profile loading times.
    
            "extensions":   True,   # Extension storage is a special cotainer where a browser stores extensions and their parameter. 
                                    # Enable it if you need to install extensions from a browser interface.
                                
            "bookmarks":    True,   # This option enables saving bookmarks in a browser interface.
                                
            "history":      True,   # Warning! Enabling this option may increase the amount of data required 
                                    # to open/save a browser profile significantly. 
                                    # In the interests of security, you may wish to disable this feature, 
                                    # but it may make using GoLogin less convenient.
                                
            "passwords":    True,   # This option will save passwords stored in browsers.
                                    # It is used for pre-filling login forms on websites. 
                                    # All passwords are securely encrypted alongside all your data.
                                
            "session":      True,   # This option will save browser session. It is used to save last open tabs.
                                
            "indexedDb":    False   # IndexedDB is special browser caches that websites may use for user tracking in a way similar to cookies. 
                                    # Having them enabled is generally advised but may increase browser profile loading times.
        }
    });
    
    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWE4MWEyODc3ZWYzOGIyMGFkNTQ2NGEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWFlMGI0NGQ4OTUzYWQ4MmU0NGUyM2EifQ.dr4Y6SGw6TnpsLMCnl4yTgvmDszSjUwViVKMJsX5wYg",
        "profile_id": profile_id
        })

    debugger_address = gl.start()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)

    driver = webdriver.Chrome(options=chrome_options)
    return driver, gl

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
    driver.get('https://megamarket.ru/personal/loyalty')

def create_sber_id(driver, phone, name, surname, birth_date, password, gmail):
    try:
        create_sber_id_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.sbid-button span.sbid-button__text"))
        )
        driver.execute_script("arguments[0].click();", create_sber_id_button)
    except Exception as e:
        print(f"Не удалось найти и нажать на кнопку: {e}")

    time.sleep(30)
    phone_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-testid="phoneNumber-input"][type="tel"]'))
    )
    ActionChains(driver).move_to_element(phone_input).click().send_keys(phone).perform()
    time.sleep(10)
    continue_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="phoneNumber-nextButton"][type="submit"]')
    continue_button.click()
    time.sleep(50)
    first_name_input = driver.find_element(By.NAME, 'firstName')
    first_name_input.send_keys(name)
    time.sleep(2)
    last_name_input = driver.find_element(By.NAME, 'lastName')
    last_name_input.send_keys(surname)
    time.sleep(2)
    dob_input = driver.find_element(By.NAME, 'dob')
    dob_input.send_keys(birth_date)
    time.sleep(2)
    dpassword_input = driver.find_element(By.NAME, 'password')
    dpassword_input.send_keys(password)
    time.sleep(2)
    dpassword_confirm_input = driver.find_element(By.NAME, 'confirmPassword')
    dpassword_confirm_input.send_keys(password)
    time.sleep(2)
    email_conf = driver.find_element(By.NAME, 'email')
    email_conf.send_keys(gmail)
    time.sleep(3)
    create_sber_id_button = driver.find_element(By.XPATH, '//button[contains(.,"Создать Сбер ID")]')
    create_sber_id_button.click()
    time.sleep(20)
    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@type="checkbox"]//input[@type="checkbox"]'))
    )

    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(5)
    join_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@class="btn profile-loyalty-no-join-program__button"]'))
    )

    # Выполним клик по найденному элементу
    driver.execute_script("arguments[0].click();", join_button)
    time.sleep(15)


def main():
    # Чтение данных из Excel-файла
    excel_data = pd.read_excel('C:\\Users\\zimar\\Desktop\\SBMSoft\\Sim.xlsx', header=None)

    for index, row in excel_data.iterrows():
        phone = row[0]  # Номер телефона в первом столбце
        email = row[2]  # Электронная почта в третьем столбце

        driver, gl = open_browser(phone)

        try:
            login_to_megamarket(driver, phone)
            create_sber_id(driver, phone, name, surname, birth_date, password, email)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            driver.quit()
            gl.stop()
            time.sleep(3)
           

if __name__ == "__main__":
    main()
