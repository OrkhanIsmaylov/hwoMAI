import csv
import sys

# ====================
# Функции
# ====================
# функция - это часть кода, которую можно оформить отдельно, дать ей имя и вызывать в нужный момент
# функции обычно возникают, когда какую-то последовательность команд требуется вызывать несколько раз. тогда выгоднее оформить их в функцию
# функция:
# 1) обозначается ключевым словом def, объявление функции завершается символом ":", тело функции пишется с отступом, например:
# 2) функция может принимать параметры. параметры записываются в круглых скобках через запятую
# 3) функция может возвращать результат - одно значение или больше. если больше - возвращается кортеж!
# пример:
# def test_function(param1, param2):
# 	your code
# 	return result1, result2

# ====================
# Часть 1: Функция с жестко заданными параметрами
# ====================
# читаем информацию о квартирах в список. в этот раз - в список словарей, а не список списков
# для этого предназначен объект csv.DictReader. Он воспринимает первую строку файла output.csv как набор ключей, а каждую следующую строку - как набор данных
# получаются пары [('ID', '156605497'), ('Количество комнат', '2'), ('Новостройка/вторичка', 'новостройка'), ('Метро', 'м.Черкизовская'), ('Время до метро', '10') ... ('Лифт', 'да'), ('Ссылка на объявление', ''), (None, ['https://www.cian.ru/sale/flat/156605497'])]
flats_list = list()
with open('output.csv', encoding="utf-8") as csvfile:
    flats_dictreader = csv.DictReader(csvfile, delimiter=';')
    flats_list = list(flats_dictreader)

user_budget = 3000000
user_flat_type = "новостройка"
print(f"Мы задаем бюджет пользователя в user_budget: {user_budget}")

# будем подбирать квартиры по совокупности параметров: стоимости, этажу + наличию лифта, новостройка/вторичка
# это функция с жестко заданными параметрами. их количество не может меняться, все они обязательно должны быть заданы при вызове функции
def filterFlats(budget, flat_type):
	flats = list()
	for flat in flats_list:
		if budget >= int(flat["Цена (руб)"]) and flat["Новостройка/вторичка"] == flat_type:
			flats.append(flat)
			print(f'Квартира {flat["ID"]} нам подходит, потому что ее цена {flat["Цена (руб)"]} и ее тип {flat["Новостройка/вторичка"]}')
	return len(flats), flats

flats_count, flats_choosen = filterFlats(user_budget, "вторичка")
print(f"Мы отобрали {flats_count} квартир, вот они:\n {flats_choosen}")

# ====================
# Часть 2: Функция с не известным заранее числом параметров
# ====================
# мы можем передать в функцию переменное количество параметров. Это удобно, если нам нужно производить вычисления над не известным заранее количеством данных
# в этом случае параметры передаются как *args. Звездочка означает переменное количество параметров. Тип args - кортеж
# параметры должны идти в заранее определенном порядке!

# пример: передаем те же параметры для отбора квартир - бюджет и тип квартиры (новостройка или вторичка), но в формате *args
def filterFlats_args(*args):
	print(f"Тип параметров *args: {type(args)}, параметры выглядят вот так: {args}")
	budget = 0
	flat_type = ""
	for i, arg in enumerate(args):
		if i == 0:
			budget = int(arg)
		elif i == 1:
			flat_type = arg

	flats = list()
	for flat in flats_list:
		if budget >= int(flat["Цена (руб)"]) and flat["Новостройка/вторичка"] == flat_type:
			flats.append(flat)
			print(f'Квартира {flat["ID"]} нам подходит, потому что ее цена {flat["Цена (руб)"]} и ее тип {flat["Новостройка/вторичка"]}')
	return len(flats), flats

flats_count, flats_choosen = filterFlats_args(user_budget, "вторичка")
print(f"Мы отобрали {flats_count} квартир, вот они:\n {flats_choosen}")

# ====================
# Часть 3: Функция с не известным заранее числом ИМЕНОВАННЫХ параметров
# ====================
# мы можем передать в функцию переменное количество параметров, каждый из которых будет иметь собственное имя. Это удобно, если мы не только не знаем заранее количество параметров, но не знаем и порядок их следования
# в этом случае параметры передаются как **kwargs. Две звезды означает переменное количество именованных параметров. Тип kwargs - словарь, в котором ключ - имя параметра, которое мы передаем в функцию

# пример
def filterFlats_kwargs(**kwargs):
	print(f"Тип параметров **kwargs: {type(kwargs)}, параметры выглядят вот так: {kwargs}")
	# Работать с параметрами kwargs можно точно так же, как с обычным словарем:
	for k, v in kwargs.items():
		print(k, v, type(v))

	# безопасное получение значения словаря через dictionary.get()
	budget = kwargs.get("budget")
	if budget is None:
		print("Нет данных по бюджету, не с чем сравнивать, поэтому выходим из функции")
		return

	# безопасное получение значения словаря через dictionary.get()
	flat_type = kwargs.get("flat_type")
	if flat_type is None:
		print("Нет данных по типу квартиры, не с чем сравнивать, поэтому выходим из функции")
		return

	flats = list()
	for flat in flats_list:
		if budget >= int(flat["Цена (руб)"]) and flat["Новостройка/вторичка"] == flat_type:
			flats.append(flat)
			print(
				f'Квартира {flat["ID"]} нам подходит, потому что ее цена {flat["Цена (руб)"]} и ее тип {flat["Новостройка/вторичка"]}')

	return len(flats), flats

# теперь порядок передачи параметров в функцию не имеет значения
flats_count, flats_choosen = filterFlats_kwargs(flat_type="вторичка", budget=3000000)
# получим тот же самый результат, даже если поменяем параметры местами
# flats_count, flats_choosen = filterFlats_kwargs(budget=3000000, flat_type="вторичка")
print(f"Мы отобрали {flats_count} квартир, вот они:\n {flats_choosen}")

# ====================
# Часть 4: Комбинирование параметров в функции
# ====================
# мы можем комбинировать различные типы параметров, но с обязательным соблюдением правила следования: обязательные, *args, **kwargs
# можно опускать любой из типов параметров. Например, написать так: обязательные, **kwargs
# но ни в коем случае не так! **kwargs, обязательные

# пример:
def filterFlats_flexible(subway, *args, **kwargs):
    # проверяем список параметров
    floor = 0
    is_elevator = False
    print(f"subway={subway}, *args = {args}, **kwargs = {kwargs}")

    if args is not None:
        if len(args) < 2:
            print("Необходимо задать и этаж, и наличие лифта")
            return
        else:
            floor = int(args[0])
            is_elevator = bool(args[1])

    budget = kwargs.get("budget")
    if budget is None:
        print("Нет данных по бюджету, не с чем сравнивать, поэтому выходим из функции")
        return

    flat_type = kwargs.get("flat_type")
    if flat_type is None:
        print("Нет данных по типу квартиры, не с чем сравнивать, поэтому выходим из функции")
        return
    print(f"Значение бюджета: {budget}, значение типа квартиры: {flat_type}")

    for flat in flats_list:
        if budget >= int(flat["Цена (руб)"]) and flat["Новостройка/вторичка"] == flat_type:
            is_flat_elevator = False
            if flat["Лифт"].lower() == "нет" or len(flat["Лифт"]) == 0:
                is_flat_elevator = False
            elif flat["Лифт"].lower() == "да":
                is_flat_elevator = True

            print(f'Квартира {flat["ID"]} нам подходит, потому что ее цена {flat["Цена (руб)"]} и ее тип {flat["Новостройка/вторичка"]}')
            if int(flat["Этаж"]) == floor or is_elevator == is_flat_elevator:
                print(f'А также рекомендуем для пенсионеров, инвалидов или мамочек с колясками (и еще лентяев), потому что она либо на первом этаже (проверяем: {flat["Этаж"]}) либо с лифтом (проверяем: {is_flat_elevator}), либо и то, и другое')
            else:
                print(f'Похоже, это квартира для спортсменов! {flat["Этаж"]}, {is_flat_elevator}')

filterFlats_flexible("Черкизовская", 2, 1, flat_type="новостройка", budget=3000000)
# ====================
# Часть 4: Глобальные переменные
# ====================
# если внутри функции мы переопределим переменную с ключевым словом global, то изменится значение этой переменной даже за пределами функции
# пример
budget = 3000000
budget2 = 3000000
print(f"Мы задали значения бюджетов в основном коде: budget={budget}, budget2 = {budget2}")
def filterFlats():
	global budget
	budget = 6000000
	budget2 = 6000000
	print(f"Мы переопределили budget модификатором global и пока находимся в функции. Сейчас budget={budget}, budget2 = {budget2}")

filterFlats()
print(f"Мы вышли из функции. Теперь budget={budget}, budget2 = {budget2}")

