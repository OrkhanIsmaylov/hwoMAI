# ДЗ по теме "Работа с интернет-источниками"
# ваша задача - получить данные о воздушном флоте перечисленных ниже авиакомпаний (2 компании),
# аналогично тому, как это было на лекции
# 1) NordWind https://nordwindairlines.ru/ru/fleet
# 2) ЮТэйр https://www.utair.ru/about/aircrafts/

# TODO1: разработайте структуру данных, в которой вы сможете сохранить данные по воздушному флоту каждой из авиакомпаний
# например, это может быть словарь с ключами - названиями авиакомпаний и значениями - данными по воздушному флоту
# в любом случае, у вас получится сложная структура

# TODO2: напишите код парсеров данных о воздушном флоте для каждой из перечисленных авиакомпаний

# TODO3: сохраните полученные данные в структуру данных об авиакомпаниях Не забудьте добавить туда S7 и АК "Россия"
# если вас будет банить S7 так же, как на лекции, тогда добавьте только АК "Россия", без S7

import requests  # импортируем библиотеку. предварительно необходимо установить ее в python: pip install requests
from bs4 import BeautifulSoup

airplanes_dict = {}
url = r"https://nordwindairlines.ru/ru/fleet"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/78.0.3904.97 Safari/537.36"}
try:
    print("NordWind")
    r = requests.get(url, headers=headers)
    print(r.status_code)
    bs = BeautifulSoup(r.text, 'html.parser')
    div_bs = bs.find_all("div", attrs={"class": "page__container"})
    rows_bs = div_bs[0].findChildren("ul", attrs={"class": "fleet__list"}, recursive=True)
    ul_bs = rows_bs[0].findChildren("li", attrs={"class": "fleet__item"}, recursive=True)
    for ul in ul_bs:
        name = ul.find("h3").text.replace("\n", "")
        print(name)
        airplanes_dict.setdefault(name, {})
        p_bs = ul.findChildren("p", attrs={"class": "fleet__item-parameter"}, recursive=True)
        for p in p_bs:
            span_bs_name = p.findChildren("span", attrs={"class": "fleet__item-parameter-name"}, recursive=True)
            span_bs_name = span_bs_name[0].text.replace(":", "")
            span_bs_value = p.findChildren("span", attrs={"class": "fleet__item-parameter-value"}, recursive=True)
            value = span_bs_value[0].text.replace("\n", "")
            value = value.replace(" ", "")
            index_a = 0
            for char in range(0, len(value)-1):
                if value[char].isdigit() and value[char+1].isalpha():
                    value = value[:index_a+1] + " " + value[index_a+1:]
                    break
                index_a += 1
            airplanes_dict[name].setdefault(span_bs_name, value)
            print(f"{span_bs_name}  {value}")
        print(""*2)
    print(""*2)
    print("Ютэйр")
    url = r"https://www.utair.ru/about/aircrafts/"
    r = requests.get(url, headers=headers)
    print(r.status_code)
    bs = BeautifulSoup(r.text, 'html.parser')
    div_bs = bs.find_all("div", attrs={"class": "wrapper-content"}, recursive=True)
    div_bs = div_bs[0].find_all("div", attrs={"class": "airship-blocks"}, recursive=True)
    content_bs = div_bs[0].findChildren("div", attrs={"class": "airship-block"}, recursive=True)
    for item in content_bs:
        print(item.find("a").text)
        name = item.find("a").text.replace("\n", "")
        airplanes_dict.setdefault(name, {})
        p_bs = item.findChildren("p")
        for p in range(1, len(p_bs)):
            text = p_bs[p].text.split(":")
            airplanes_dict[name].setdefault(text[0], text[1].lstrip())
            print(f"{text[0]} {text[1]}")
        print("" * 2)
    print("АК Россия")
    url = r"https://www.rossiya-airlines.com/about/about_us/fleet/aircraft/"
    r = requests.get(url, headers=headers)
    print(r.status_code)
    bs = BeautifulSoup(r.text, 'html.parser')
    table_bs = bs.find_all("tbody")[1]
    tr_bs = table_bs.find_all("tr")
    for tr in tr_bs:
        name = tr.find("h2").text.replace("\n", "")
        print(name)
        airplanes_dict.setdefault(name, {})
        span_bs = tr.find_all("span")
        for i in range(2, len(span_bs)-2):
            value = span_bs[i].text.replace("\r", "")
            value = value.replace("\n", "")
            value = value.replace("\t", "")
            value = value.replace("\xa0", "")
            index = 0
            for char in value:
                if char.isdigit():
                    index = index
                    break
                index += 1
            index_a = 0
            for char in range(0, len(value)-1):
                if value[char].isdigit() and value[char+1].isalpha():
                    value = value[:index_a+1] + " " + value[index_a+1:]
                    break
                index_a += 1
            airplanes_dict[name].setdefault(value[:index].rstrip(), value[index:])
            print(f"{value[:index].rstrip()} {value[index:]}")
        print(""*2)
except Exception as e:
    print(e)
