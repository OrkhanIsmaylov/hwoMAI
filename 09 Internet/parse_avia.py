# ====================
# Работа с интернет-источниками
# ====================
# работа с интернет-источниками через библиотеку requests (самый простой способ)
# requests http://docs.python-requests.org/en/latest/index.html
# примеры для requests https://habr.com/ru/post/126262/
# мы будем изучать воздушный флот двух авиакомпаний: "Россия" и "S7"

import requests  # импортируем библиотеку. предварительно необходимо установить ее в python: pip install requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
# для парсинга веб-страниц понадобится библиотека BeautifulSoup. устанвока: pip install bs4

# веб-адрес страницы S7, с которой мы будем получать информацию
url = r"https://www.s7.ru/ru/about/ourfleet.dot"

# в работе с интернет-источниками участвуют два объекта: request (объект запроса) и response (объект ответа),
# в которых содержится как служебная информация запроса, так и дополнительные настройки и данные, которые можете туда
# встроить вы сами

# при подключении к интернет-источнику (серверу) сервер "видит", что к нему в качестве клиента обращается
# робот-парсер на питоне. поэтому представимся как браузер, заколнив заголовки запроса:
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/78.0.3904.97 Safari/537.36"}

# # есть два спосооба отправить запрос к серверу: GET (запрос на получение данных), POST (тоже на получение данных,
# # но вместе с запросом можно передать дополнительные даннные. например, когда вам нужно авторизоваться на сайте)
# try:
#     # отправляем запрос на получение html страницы с сервера.
#     в качестве параметра передаем данные о клиенте (браузере)
#     r = requests.get(url, headers=headers)
#
#     # при получении данных необходимо проверить, было ли оно успешным, через r.status_code
#     print(r.status_code)  # отображаем код ответа HTTP. 200 - ОК, 404 - ресурс не найден, 500* - различные коды
#     # ошибок сервера. подробно:
#
#     # другие полезные свойства объекта response:
#     print(r.url)  # отображаем url источника, который нам вернулся. он может отличаться от исходного!
#     print(r.headers)  # отображаем заголовок ответа сервера
#     # содержимое страницы можно получить в виде текста либо в бинарном виде:
#     print(r.text)  # получаем обычный html-код страницы
#     print(r.content)  # получаем html-код страницы как двоичный объект
#
#     # создаем парсер. в качестве параметра передаем название движка, который может парсить html-страницы - lxml если
#     # у вас не установлен lxml: pip install lxml. этот параметр можно опустить. рабоать будет, но появится
#     # предупреждение
#     bs = BeautifulSoup(r.text, 'html.parser')
#     # после анализа кода страницы находим html-тег, внутри которого содержится нужная дла нас информация о воздушном
#     # флоте авиакомпании find_all() находит все теги, find() берет только первый по списку и останавливает поиск для
#     # уточнения поиска (т.к. тегов div очень много) используются атрибуты, сопровождающие этот тег ("div",
#     # attrs={"class":"company-main-cont"}) соответствует коду html ...........
#     div_bs = bs.find_all("div", attrs={"class": "company-main-cont"})
#     rows_bs = div_bs[0].findChildren("div", attrs={"class": "row"}, recursive=False)
#     # print(len(rows_bs))
#     # результат поиска - список объектов-тегов. работаем с ними как с обычным списком:
#     for row in rows_bs:
#         print(row.find("h3").text)
#         cols_bs = row.find_all("div", attrs={"class": "col-md-11"})
#         for col in cols_bs:
#             print(col.text)
#         print()
#         # атрибуты - это словарь, поэтому значение атрибута получается аналогично
#         # например, в строке ниже получаем ссылку на изображение самолета, которая находится в теге src
#         img = row.find("img")["src"]
#         # обратите внимание на параметр allow_redirects=True. некоторые html-страницы при запросе на один url
#         # перенаправляют на другой url и именно по нему вы получаете нужные данные. True разрешает редиректы
#         rfile = requests.get(url, allow_redirects=True)
#         # сохраняем полученное изображение в файл. открываем его в режиме "запись+двоичный" wb, т.к.
#         # изображение - это файл в двоичном формате
#         open(row.find("h3").text + ".png", 'wb').write(rfile.content)
#     # print(r.status_code)
# except Exception as e:
#     print(e)

# веб-адрес страницы АК "Россия", с которой мы будем получать информацию
url_rossiya = r"https://www.rossiya-airlines.com/about/about_us/fleet/aircraft/"
try:
    r = requests.get(url_rossiya, headers=headers)
    bs = BeautifulSoup(r.text, 'html.parser')
    table_bs = bs.find_all("tbody")[1]
    imgs_bs = table_bs.find_all("img")
    for i, image in enumerate(imgs_bs):
        pict_url = "https://www.rossiya-airlines.com{}".format(image["src"])
        print(pict_url)
        rimg = requests.get(pict_url, allow_redirects=True)
        open("aircraft_{}.png".format(i+1), 'wb').write(rimg.content)
    pdfs_bs = table_bs.find_all("a")
    for pdf in pdfs_bs:
        pdf_url = "https://www.rossiya-airlines.com{}".format(pdf["href"])
        if ".pdf" in pdf_url:
            rpdf = requests.get(pdf_url, allow_redirects=True)
            path = pdf["href"].split("/")
            open(path[-1], 'wb').write(rpdf.content)
except Exception as e:
    print(e)
