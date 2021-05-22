import requests
import dataset

db = dataset.connect('sqlite:///symbol_info.db')
table = db['symbols']

#manual use, erase shortlisted values
def update_symbols():
    r = requests.get("https://api-adapter.backend.currency.com/api/v1/exchangeInfo")
    for i in r.json()['symbols']:
        table.insert(dict(symbol=i['symbol'], name=i['name'], sector=i['sector'], industry=i['industry'], shortlisted = 0 ))

def get_shortlisted_symbols():
    shortlisted = table.find(shortlisted=1)
    shortlisted = [i['symbol'] for i in shortlisted]
    return shortlisted

def get_all_unlisted_symbols():
    symbols = table.find(shortlisted = 0)
    unlisted = [i['symbol'] for i in symbols]
    print(unlisted)
    return unlisted

def shortlist_symbol(symbol):
    table.update(dict(symbol=symbol, shortlisted=1), ['symbol'])

def unlist_symbol(symbol):
    table.update(dict(symbol=symbol, shortlisted=0), ['symbol'])

get_shortlisted_symbols()