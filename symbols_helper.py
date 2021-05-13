import requests
import json

r = requests.get("https://api-adapter.backend.currency.com/api/v1/exchangeInfo")
for i in r.json()['symbols']:
    print(i['symbol']," - ", i['name']," - ", i['sector']," - ", i['industry'])