import json
import requests
import schedule
import time


FAVORITE = ("USD", "EUR", "RUB", "GBP")

day_currencies = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'
month_currencies = 'https://www.nbrb.by/api/exrates/rates?periodicity=1'


def get_currencies(url=day_currencies):
    """Возвращает JSON с курсами валют НБ РБ."""
    r = requests.get(url)
    resp = r.json()
    return resp


def store_day_all_currencies():
    """Записывает JSON с основными валютами на диск."""
    data = get_currencies()

    with open('./data/day_all_currencies.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return


def store_month_all_currencies():
    """Записывает JSON с остальными валютами на диск."""
    data = get_currencies(url=month_currencies)

    with open('./data/month_all_currencies.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return


def store_favorite_currencies():
    """Записывает JSON с избранными валютами на диск."""

    favorite_currencies = []
    data = get_currencies()

    for curr in data:
        cur = {}
        if curr.get("Cur_Abbreviation") in FAVORITE:
            cur[curr["Cur_Abbreviation"]] = curr
            favorite_currencies.append(cur)

    with open('./data/favorite_currencies.json', 'w', encoding='utf-8') as file:
        json.dump(favorite_currencies, file, ensure_ascii=False, indent=4)
    return


schedule.every().day.at("00:01").do(store_day_all_currencies)
schedule.every().day.at("00:02").do(store_favorite_currencies)
schedule.every().day.at("00:05").do(store_month_all_currencies)


if __name__ == '__main__':
    store_month_all_currencies()
    store_day_all_currencies()
    store_favorite_currencies()
    while True:
        schedule.run_pending()
        time.sleep(30)
