from pathlib import Path
import requests
import json

"""
HИсточник: https://5ka.ru/special_offers/
Задача организовать сбор данных,
необходимо иметь метод сохранения данных в .json файлы
результат: Данные скачиваются с источника, при вызове метода/
функции сохранения в файл скачанные данные сохраняются в Json файлы, 
для каждой категории товаров должен быть создан отдельный файл и содержать товары 
исключительно соответсвующие данной категории.
пример структуры данных для файла:
нейминг ключей можно делать отличным от примера

{
"name": "имя категории",
"code": "Код соответсвующий категории (используется в запросах)",
"products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
}
"""

temp_file = Path(__file__).parent.joinpath("temp2.html")

url = "https://5ka.ru/api/v2/special_offers/?categories=698&page=1"
# "https://5ka.ru/api/v2/categories/"
# url = "https://5ka.ru/special_offers/"

headers = {
 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"
}

response = requests.get(url, headers=headers)
# temp_file.write_bytes(response.content)

data: dict = response.json()
print(data.keys())
print(data["next"])
# print(response.json())

''' data['results']'''
with open('sw_templates.json', 'w') as f:
    json.dump(data['results'], f, ensure_ascii=False)


""" сюда сложить dict из запроса"""
# categories_file = {
# "name": "имя категории",
# "code": "Код соответсвующий категории (используется в запросах)",
# "products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
# }
