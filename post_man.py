import http.client
import json

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

# Создание словаря name : id
name_id_dict = {profile.get("name"): profile.get("id") for profile in profiles}

print(name_id_dict)

