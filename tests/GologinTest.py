import time
from sys import platform
from selenium import webdriver
from gologin import GoLogin
from gologin import getRandomPort
from selenium.webdriver.chrome.service import Service

from gologin import GoLogin


profile_creating = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWE4MWEyODc3ZWYzOGIyMGFkNTQ2NGEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWFlMGI0NGQ4OTUzYWQ4MmU0NGUyM2EifQ.dr4Y6SGw6TnpsLMCnl4yTgvmDszSjUwViVKMJsX5wYg",
	})

profile_id = profile_creating.create({
    "name": 'profile_mac',
    "os": 'mac',
    "navigator": {
        "language": 'en-US',
        "userAgent": 'random',
        "resolution": '1024x768',
        "platform": 'mac',
    },
    'proxy': {
        'mode': 'gologin', # Specify 'none' if not using proxy
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

print('profile id=', profile_id);

# gl.update({
#     "id": 'yU0Pr0f1leiD',
#     "name": 'profile_mac2',
# });

profile = profile_creating.getProfile(profile_id);

print('new profile name=', profile.get("name"));

# gl.delete('yU0Pr0f1leiD')

gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWE4MWEyODc3ZWYzOGIyMGFkNTQ2NGEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWFlMGI0NGQ4OTUzYWQ4MmU0NGUyM2EifQ.dr4Y6SGw6TnpsLMCnl4yTgvmDszSjUwViVKMJsX5wYg",
	"profile_id": profile_id
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