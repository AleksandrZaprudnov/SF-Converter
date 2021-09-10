import json
import requests
from config import keys, API_KEY


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, amount: str):

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не корректное значение валюты {amount}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}' \
f'&base=EUR&symbols={quote_ticker}')

        total_base = json.loads(r.content)['rates'][keys[quote]]

        return total_base
