import time
from sys import platform
from selenium import webdriver
from gologin import GoLogin
from gologin import getRandomPort
from selenium.webdriver.chrome.service import Service

from gologin import GoLogin

gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWE4MWEyODc3ZWYzOGIyMGFkNTQ2NGEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWFlMGI0NGQ4OTUzYWQ4MmU0NGUyM2EifQ.dr4Y6SGw6TnpsLMCnl4yTgvmDszSjUwViVKMJsX5wYg",
	"profile_id": '65c3ec517c5388a32c343451',
	})



debugger_address = gl.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.python.org")

time.sleep(30)
driver.quit()
time.sleep(10)
gl.stop()