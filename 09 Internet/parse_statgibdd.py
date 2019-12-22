import requests
import json

url = "http://stat.gibdd.ru/map/getDTPCardData"

# некоторые интернет-источники требуют, чтобы вы передавали параметры запроса отдельно
# в этом случае вы не можете задать параметры запроса в url и должны дополнительно передать данныые, как правило,
# в формате json
# payload - фильтр данных для ресурса stat.gibdd.ru
payload = {"data": "{\"date\":[\"MONTHS:1.2019\",\"MONTHS:2.2019\"],"
                   "\"ParReg\":\"45\",\"order\":{\"type\":\"1\",\"fieldName\":\"dat\"},"
                   "\"reg\":\"45268592\",\"ind\":\"1\",\"st\":\"1\",\"en\":\"16\"}"}

payload2 = {"data": ""}
req_data = {
    "date": ["MONTHS:1.2019", "MONTHS:2.2019", "MONTHS:3.2019", "MONTHS:4.2019", "MONTHS:5.2019", "MONTHS:6.2019",
             "MONTHS:7.2019", "MONTHS:8.2019", "MONTHS:9.2019", "MONTHS:10.2019", "MONTHS:11.2019"], "ParReg": "45",
    "order": {"type": "1", "fieldName": "dat"}, "reg": "45268592", "ind": "1", "st": "1", "en": "16"}
req_data["en"] = str(100)
print(req_data)

# чтобы сформировать собственный json для запроса, используйте функцию json.dumps(), которая превращает словарь,
# содержащий ваши параметры, в строку
# некоторые ресурсы (stat.gibdd.ru в их числе) требуют, чтобы данные были переданы в так называемой "компактной записи",
# т.е. не содержали ни одного лишнего пробела
# к сожалению, json.loads автоматически вставляет пробелы. убирайте их функцией str.replace(" ", "")
payload2["data"] = json.dumps(req_data).replace(" ", "")
# payload2["data"] = json.dumps(req_data)
print(f"payload2:\n{payload2}\npayload:\n{payload}")

try:
    # если вы передаете данные вместе с url запроса, используйте метод POST вместо GET
    # в данном случае формат передаваемых данных будет json
    # (а не, например, data, который вы используете для авторизации на сайте через форму логина-пароля)
    r = requests.post(url, json=payload2)
    print(r.status_code)
    if r.status_code == 200:
        # в ответ на ваш запрос сайт также возвращает данные в формате json.
        # преобразуйте их в словарь методом json.loads()
        json_data = json.loads(r.text)
        print(f'Тип данных: {type(json_data)}, тип значения: {type(json_data["data"])}')
        json_cards = json.loads(json_data["data"])
        print(f'Тип данных: {type(json_cards)}, количество карточек: {len(json_cards["tab"])}')
except Exception as e:
    print(e)
