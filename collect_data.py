import json
import requests
import schedule
import time
from urllib3 import disable_warnings, exceptions

import logs


disable_warnings(exceptions.InsecureRequestWarning)

FAVORITE = ("USD", "EUR", "RUB", "GBP", "CNY")
day_currencies = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'
month_currencies = 'https://www.nbrb.by/api/exrates/rates?periodicity=1'


def get_currencies(url):
    """Возвращает JSON с курсами валют НБ РБ."""
    try:
        with requests.get(url, verify=False) as response:
            return response.json()
    except Exception as e:
        print(e)
        return 


def store_day_all_currencies():
    """Записывает JSON с основными валютами на диск."""
    count = 5
    while count:
        data = get_currencies(day_currencies)
        
        if data:
            with open('./data/day_all_currencies.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return
        else:
            count -= 1
            time.sleep(10)
    return "Невозможно получить данные за день"


def store_month_all_currencies():
    """Записывает JSON с остальными валютами на диск."""
    count = 5
    
    while count:
        data = get_currencies(month_currencies)
        if data:
            with open('./data/month_all_currencies.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return
        else:
            count -= 1
            time.sleep(10)
    return "Невозможно получить данные за месяц"


def store_favorite_currencies():
    """Записывает JSON с избранными валютами на диск."""

    favorite_currencies = []
    
    with open('./data/day_all_currencies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for currency in data:
            if currency['Cur_Abbreviation'] in FAVORITE:
                favorite_currencies.append(currency)

    with open('./data/favorite_currencies.json', 'w', encoding='utf-8') as file:
        json.dump(favorite_currencies, file, ensure_ascii=False, indent=4)
    return


# schedule.every().day.at("00:05").do(store_day_all_currencies)
# schedule.every().day.at("00:07").do(store_favorite_currencies)
# schedule.every().day.at("00:10").do(store_month_all_currencies)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


if __name__ == "__main__":
    store_day_all_currencies()
    store_month_all_currencies()
    store_favorite_currencies()
    print("Все данные сохранены")

# docker run -d --mount type=bind,source="$(pwd)"/logs,target=/app/logs -v "$(pwd)"/data:/app/data fenick/nbrb:latest