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
    return unlisted

def shortlist_symbol(symbol):
    table.update(dict(symbol=symbol, shortlisted=1), ['symbol'])

def is_shortlisted(symbol):
    s = table.find_one(symbol=symbol)
    result = s['shortlisted']
    return result

def unlist_symbol(symbol):
    table.update(dict(symbol=symbol, shortlisted=0), ['symbol'])

def add_comment_for_symbol(data):
    symbol = data[0]
    comment = data[1]
    table.update(dict(symbol=symbol, comment=comment), ['symbol'])

def get_comment_for_symbol(symbol):
    s = table.find_one(symbol=symbol)
    try:
        comment = s['comment']
    except:
        comment = ""
    return comment