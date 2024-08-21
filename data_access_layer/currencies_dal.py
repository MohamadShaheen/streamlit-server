import os
import copy
import currencyapicom
import mongodb_connection
from fastapi import HTTPException

currency_api_key = os.getenv('CURRENCY_API_KEY')
database = mongodb_connection.client['currency_database']
collection = database['currencies']
client = currencyapicom.Client(currency_api_key)

def store_currencies():
    collection.delete_many({})
    currencies = client.currencies()
    currencies = currencies['data']

    currencies_to_insert = []
    for value in currencies.values():
        currency_data = {
            'code': value['code'],
            'name': value['name'],
        }
        currencies_to_insert.append(currency_data)

    collection.insert_many(copy.deepcopy(currencies_to_insert))
    return currencies_to_insert

def retrieve_all_currencies():
    db_currencies = collection.find({}, {'_id': 0})

    if not db_currencies:
        raise HTTPException(status_code=404, detail='No currencies found')

    currencies = [currency for currency in db_currencies]
    return currencies

def convert_currencies(from_currency: str, to_currency: str, amount: float):
    db_from_currency = collection.find_one({'code': from_currency}, {'_id': 0})

    if not db_from_currency:
        raise HTTPException(status_code=404, detail="'From' currency not found")

    db_to_currency = collection.find_one({'code': to_currency}, {'_id': 0})

    if not db_to_currency:
        raise HTTPException(status_code=404, detail="'To' currency not found")

    conversion_rate = client.latest(from_currency, currencies=[to_currency])
    conversion_rate = conversion_rate['data'][to_currency]['value']
    return round(conversion_rate * amount, 2)
