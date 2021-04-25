from decimal import Decimal

import requests

from .models import Currency


def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'

    response = requests.get(url)

    data = response.json()
    source = 1
    currency_map = {
        840: 1,
        978: 2,
    }
    for row in data:
        if row['currencyCodeA'] in currency_map and row['currencyCodeB'] == 980:
            buy = round(Decimal(row['rateBuy']), 2)
            sale = round(Decimal(row['rateSell']), 2)
            currency = currency_map[row['currencyCodeA']]
            cr_last = Currency.objects.filter(currency=currency, source=source).last()
            if cr_last is None or (cr_last.buy != buy or cr_last.sale != sale):
                Currency.objects.create(currency=currency, source=source, buy=buy, sale=sale)


def parse_vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)

    data = response.json()
    source = 2
    currency_map = {
        'Dollar': 1,
        'Euro': 2,
    }
    for row in data:
        if row in currency_map:
            buy = Decimal(data.get(row)['buy'])
            sale = Decimal(data.get(row)['sale'])
            currency = currency_map[row]
            cr_last = Currency.objects.filter(currency=currency, source=source).last()
            if cr_last is None or (cr_last.buy != buy or cr_last.sale != sale):
                Currency.objects.create(currency=currency, source=source, buy=buy, sale=sale)


def parse_yahoo():
    from yahoofinancials import YahooFinancials
    from datetime import date, timedelta

    yesterday = str(date.today() - timedelta(days=1))

    currencies = ['USDUAH=X', 'EURUAH=X']
    yahoo_financials_currencies = YahooFinancials(currencies)
    data = yahoo_financials_currencies.get_historical_price_data(yesterday, yesterday, 'daily')

    source = 3
    currency_map = {
        'USDUAH=X': 1,
        'EURUAH=X': 2,
    }
    for row in data:
        if row in currency_map:
            buy = round(Decimal(data.get(row)['prices'][0]['close']), 2)
            sale = round(Decimal(data.get(row)['prices'][0]['close']), 2)
            currency = currency_map[row]
            cr_last = Currency.objects.filter(currency=currency, source=source).last()
            if cr_last is None or (cr_last.buy != buy or cr_last.sale != sale):
                Currency.objects.create(currency=currency, source=source, buy=buy, sale=sale)
