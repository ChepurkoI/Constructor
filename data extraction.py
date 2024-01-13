import itertools

from bs4 import BeautifulSoup
#, SoupStrainer
#import requests, json
#import translate
from translate import Translator
import Class_Timer
import pandas as pd
import pprint


#/media/igor/USB DISK/Файлы HTML/dns.html
# home/igor/PycharmProjects/parsing_and_analysys/analysis/Файлы HTML

def download_links(tree_BS4):
    # поиск тегов <a> с определенным классом по дереву
    Nodes = tree_BS4.find_all("a", class_="")
    with open("product_links.txt", "a", encoding='utf-8') as file:
        for i in range(len(Nodes)):
            file.write(Nodes[i]['href'] + "\n")
    
    """ПОЛИНЕ ДЛЯ ЧТЕНИЯ ССЫЛОК ИЗ ФАЙЛА"""
    with open("product_links.txt", "r", encoding='utf-8') as file:
        for line in file:
            print(line, end="")
    
            
    

def collections_title_value(tree_BS4, current_DataBase: pd.DataFrame, path : str):
    TR = Translator(from_lang="ru", to_lang="en")
    stringe = str()
    Nodes = tree_BS4.find_all("div", class_="product-characteristics__group") # поиск объекта с группами характеристик
    example_type = type(tree_BS4.find('div')) # для проверки типа "Tag" и наличия метода attrs
    current_columns = current_DataBase.columns # столбцы текущей БД, которую передали как параметр
    unused_names_columns = current_DataBase.columns
    #print(type(unused_names_columns))
    print(current_columns)
    list_unused_names_columns = list(unused_names_columns)
    # буферная однострочная БД для склеивания с текущей,
    # создается на основе столбцов текущей БД
    buffer_DataBase = pd.DataFrame(columns=current_columns)

    """Сбор характеристик по DOM-дереву конкретного телефона"""
    # по каждой группе с харатеристиками
    for i in range(len(Nodes)):
        #print(f"{Nodes[i].text:>50} ,\n")
        #print(Nodes[i].prettify())
        #print(Nodes[i].prettify())
        List_child = Nodes[i].descendants
        #print("List_child: ", len(list(List_child)))
        count = 0

        flag_title = False
        flag_value = False
        name_title = str()
        value_title = str()

        # Прямой дочерний элемент - это дочерний элемент,
        # который находится непосредственно под родительским
        # элементом с точки зрения иерархии. То есть не внук или правнук.
        #print(f"{Nodes[i].text:>50} ,\n")
        # по каждому полю в группе

        TITLE_None = 0 # используется для взятия зн-я заголовка
        for child in List_child:
            #print(count, end=" ")
            #count += 1
            #print("\t ", type(child), ": ", child, "\n")

            # Проверка на то, что это тэг и у него будет метод attrs
            if type(child) is example_type:
                if 'class' in child.attrs:
                    #print(child.attrs)
                    # print(names_classes['title'] in child['class'])
                    if names_classes['title'] in child['class']:  # a in b, a-строка, b-список
                        # print(child.string)
                        if child.string is None:
                            # создание среза из генератора дочерних элементов, для перехода к следующему
                            list_name_title = list(
                                itertools.islice(Nodes[i].descendants, TITLE_None + 1, TITLE_None + 2))
                            name_title = list_name_title[0]
                            flag_title=True
                            
                            # в качестве параметра можно указать глубину нахождения текстовой информации, а так же указание, несколько их или нет
							


                            #t1 = Class_Timer.Timer()
                            #t1.start()
                            #res = TR.translate(name_title)
                            #t1.stop()
                            #print("title: ", name_title)
                            #stringe = " ".join([stringe,name_title])
                            #print(stringe)
                        else:
                            # name_title = child.string # не работает, так как берет None, вместо строки
                            name_title = child.string

                            #stringe = " ".join([stringe,name_title])
                            flag_title = True
                            #print("title", name_title)
                            #print(stringe)
                    elif names_classes['value'] in child['class']:
                        value_title = child.string
                        flag_value = True
                        #print("value: ", value_title) # .encode('utf-8'))

                    if flag_title and flag_value:
                        if value_title is None:
                            value_title = 'Перечисление'
                        temp = value_title.encode('utf-8').decode('utf-8')

                        if (name_title in list_unused_names_columns): # Удаление использованных имен столбцов
                            list_unused_names_columns.remove(name_title)
                        # удаление концевых пробелов
                        temp = temp.lstrip() # левый
                        temp = temp.rstrip() # правый
                        buffer_DataBase[name_title] = [temp] # .replace(" ","")
                        flag_title = False
                        flag_value = False


            #print("child.string = ", child.string, end="\n\n")
            # print("\n\n")
            TITLE_None += 1
        #print("\n\n")

    """Подсчет кол-во новых столбцов"""
    old_and_new_columns = buffer_DataBase.columns
    count_current_columns = len(current_columns)
    count_old_and_new_columns = len(old_and_new_columns)
    count_new_columns = count_old_and_new_columns - count_current_columns # нашел число новых столбцов

    """Извлечение имен новых столбцов"""
    # Чтобы достать названия новых столбцов, мне необходимо закинуть старые и новые столбцы в структуру Series,
    # далее при помощи числовых индексов и знания кол-ва "старых"(текущих) стобцов вытащить их имена

    # Пример:
    # текущая БД -> 75 столбцов, ,буферная БД -> 77 столбцов
    # Число новых столбцов = 77 - 75 = 2
    # index_new_columns = list(Series_new_columns[count_current_columns:].index) -> [76,77]
    # Из Series с пронумерованными названиями столбцов буферной БД извлекаю названия под номерами 76 и 77
    # Добавляю новые столбцы к текущей БД с пустыми ячейками заданной длины(длина = последний индекс в текущей БД)
    #
    # а

    Series_new_columns = pd.Series(old_and_new_columns) # формирую Series на основе имеющихся столбцов из буферной БД

    # Беру срез из Series, начиная с последнего столбца текущей БД +1
    # Вытаскиваю индексы "новых" столбцов и формирую из них список
    index_new_columns = list(Series_new_columns[count_current_columns:].index)
    names_new_columns = list()
    for i in index_new_columns:
        names_new_columns.append(Series_new_columns[i])
    # if len(names_new_columns) == count_new_columns:
    #     print("Названия новых столбцов достаются в нужном кол-ве")
    # else:
    #     print("Не совпадает кол-во имен столбцов и кол-во новых столбцов")


    """Добавление новых столбцов к текущей БД и заполнение для старых телефонов каждой ячейки нового столбца затычкой"""
    # кол-во ячеек в столбцах
    temp = list(current_DataBase.index)
    if len(temp):
        count_box = temp[-1] + 1 # индекс последней строки в текущей БД
    else:
        count_box = 0
    list_empty = [""] * count_box

    # добавление пустых столбцов к текущей БД
    for name_column in names_new_columns:
        current_DataBase[name_column] = list_empty

    # Конкатенация буферной БД и текущей
    #print("Текущая БД: ", current_DataBase)
    #print("Буферная БД: ",buffer_DataBase)
    current_DataBase = pd.concat([current_DataBase,buffer_DataBase], ignore_index=True)

    flag_print = False
    keys = current_DataBase.columns
    if flag_print:
        for key in keys:
            print(f"{current_DataBase[key]}\n")
    #t1 = Class_Timer.Timer()
    #t1.start()
    #res = TR.translate(stringe)
    #t1.stop()
    #print(res)

    # if len(unused_names_columns): # если остались неиспользованные имена столбцов
    #     last_index = current_DataBase.index[-1]
    #     for name_column in unused_names_columns: # для каждого имени вставляем затычку
    #         current_DataBase[name_column, last_index] = ""
    #print("Новая текущая БД, отработала по одной из ссылок \n",current_DataBase,"\n\n\n")
    print("Неиспользованные столбцы: ",list_unused_names_columns)

    return current_DataBase




My_link = ['/home/igor/PycharmProjects/parsing_and_analysys/analysis/1.html',
           '/home/igor/PycharmProjects/parsing_and_analysys/analysis/2.html',
           '/home/igor/PycharmProjects/parsing_and_analysys/analysis/3.html',
           '/home/igor/PycharmProjects/parsing_and_analysys/analysis/4.html',
           '/home/igor/PycharmProjects/parsing_and_analysys/analysis/5.html']

Url = 'https://www.dns-shop.ru/product/d2b3866d6a793332/667-smartfon-xiaomi-redmi-note-10-pro-128-gb-seryj/'

names_classes = {'title': 'product-characteristics__spec-title',
                 'value': 'product-characteristics__spec-value'}

DB = pd.DataFrame()
t1 = Class_Timer.Timer()


# path = "/home/igor/PycharmProjects/parsing_and_analysys/analysis/Файлы HTML/dns.html"
# with open(path, 'r', encoding="utf-8") as html_file:
#     soup = BeautifulSoup(html_file, "lxml")
#     res = download_links(tree_BS4=soup)
#     for i in range(len(res)):
#         print(i, res[i])

# """Пример запуска скачивания характеристик"""
# for path in My_link:
#     with open(path, 'r' ,encoding="utf-8" ) as html_file:
#         #products_list = SoupStrainer("a",class_="ui-link_black")
#         #print(products_list)
#         #page = requests.get(Url)
#         #print(page.status_code)
#
#         soup = BeautifulSoup(html_file, "lxml")
#         t1.start()
#         DB = collections_title_value(tree_BS4=soup, current_DataBase=DB, path="")
#         t1.stop()
#
#
# t1.start()
# DB.to_feather('DataBase.feather')
# t1.stop()
#
#
# t1.start()
# DB.to_csv("DataBase.csv")
# t1.stop()
#
# read_DB = pd.read_feather("DataBase.feather")
#
# print(read_DB.columns)
# print(read_DB.index)


def print_Nodes(Nodes):
    print("print_Nodes")
    for i in range(len(Nodes)):
        num = 43
        if i < num:
            pass
        elif i == num:
            pass
        elif i > num:
            pass
        print(f"\n\n\n{i}) хар-ка")
        print(f"Весь извлекаемый текст эл-та:\n {Nodes[i].text:>50}\n\n")
        # print("children", list(Nodes[i].children))
        # print("descendants", list(Nodes[i].descendants))
        #print(f"DOM структура элемента: \n{Nodes[i].prettify()}\n\n")

        
        for childs in Nodes[i].descendants:
            if childs.name is None:
                continue
            List_child = childs.descendants
            print(f"Кол-во всех дочерних элементов: {len(list(List_child))}\n\n")
            count = 0
            for child in childs.descendants:
                print(count, end=" ")
                count += 1
                print(f"\tтег: {child.name}  {type(child)} {child} \n")
                if child.name is not None:
                    print(f"\t Атрибуты: {child.attrs}\n")
        print("_"*100)

path = '/home/igor/PycharmProjects/HTML/test_mvideo.html' # test_mvideo
with open(path, 'r' ,encoding="utf-8" ) as html_file:
    dom_tree = BeautifulSoup(html_file, "lxml")
    #print(dom_tree.prettify())
    print(dom_tree.prettify())
    Body = dom_tree.find_all(name="body")
    
    element = Body[0].contents[0] # дочерний элемент, который и передал пользователь
    tag = element.name
    attributes = element.attrs


    print(f"\n\nСледующий после body: {tag}")
    print(f"\n\nСледующий после body: {attributes}")
    if 'class' in attributes:
        Node = dom_tree.find_all(name = str(tag), attrs=attributes['class'][0])
        print(f"\n\n\n\nТекст: {Node[0].text}")
    #print(f"\n{len(tag.text)}")
    Nodes_all = dom_tree.find_all("a") # class_ = 'catalog-product__name'
    #print_Nodes(Nodes_all)
    list_A = list()
    for i in range(len(Nodes_all)):
        if "Смартфон " in Nodes_all[i].text:
            if 'href' in Nodes_all[i].attrs:
                print(f"{i}) {Nodes_all[i].text}")
                print(f"Атрибуты: {Nodes_all[i].attrs}")
                print(f"Ссылка: {Nodes_all[i]['href']}\n")
                list_A.append(Nodes_all[i]['href'])
    print(len(list_A))



    #nodes = dom_tree.find_all("body")


# у ДНС utf-8
# у Эльдорадо windows-1251
#with open(path, 'r' ,encoding="windows-1251" ) as html_file:
    #products_list = SoupStrainer("a",class_="ui-link_black")
    #print(products_list)
    #page = requests.get(Url)
    #print(page.status_code)


    #soup = BeautifulSoup(html_file, "lxml") возился с Эльдорадо


    #Nodes = soup.find_all("td",class_="popupDeliveryPriceTable__name")
    #print(soup.prettify())
    #print_Nodes(Nodes)

    #print(DB)
    #keys = MyDB.columns
    #indexs = MyDB.index
    #print("индексы ",indexs[-1])
    #for key in keys:
    #    print(key,": " ,MyDB[key] )
"""
    # поиск сгруппированной информации
    Nodes = soup.find_all("div",class_="product-characteristics__group")
    print(len(Nodes))
    #ldJson = soup.find("script", type="application/ld+json")

    #для проверки типа и наличия метода attrs
    example_type = type(soup.find('div'))

    # по каждой группе с харктеристиками
    for i in range(len(Nodes)):
        print(f"{Nodes[i].text:>50} ,\n")
        #print("children", list(Nodes[i].children))
        #print("descendants", list(Nodes[i].descendants))
        print(Nodes[i].prettify())
        List_child = Nodes[i].descendants
        print("List_child: ",len(list(List_child)))
        count = 0

        # Прямой дочерний элемент - это дочерний элемент,
        # который находится непосредственно под родительским
        # элементом с точки зрения иерархии. То есть не внук или правнук.

        # по каждому полю в группе
        TITLE_None = 0
        for child in Nodes[i].descendants:
            print(count, end=" ")
            count+=1
            print("\t ", type(child),": ",child,"\n")

            # Проверка на то, что это тэг и у него будет метод attrs
            if type(child) is example_type:
                if 'class' in child.attrs:
                    #print(names_classes['title'] in child['class'])
                    if names_classes['title'] in child['class']: # a in b, a-строка, b-список
                        #print(child.string)
                        if child.string is None:
                            list_name_title = list(itertools.islice(Nodes[i].descendants, TITLE_None+1, TITLE_None+2))
                            name_row = list_name_title[0]
                            print("title: ", name_row)
                        else:
                            #name_row = child.string # не работает, так как берет None, вместо строки
                            name_row = child.string
                            print("title", name_row)
                    elif names_classes['value'] in child['class']:
                        value_row = child.string
                        print("value: ", value_row, " ", type(value_row))

            print("child.string = ",child.string, end="\n\n")
            #print("\n\n")
            TITLE_None+=1
        print("\n\n")
"""

def pesochnica():
    new_row = "AAA"
    new_value = "A"
    a1 = ['Somu', 'Kiku', 'Amol', 'Lini']
    a2 = [68, 74, 77, 78]
    a3 = [84, 56, 73, 69]
    a4 = [78, 88, 82, 87]
    grand = [a1,a2,a3,a4]

    dann = [a1,a2,a3,a4]
    data = pd.DataFrame(columns=[' name','physics ', ' chemistry ', '  algebra'])
    data_orig = pd.DataFrame(columns=[' name','physics ', ' chemistry ', 'algebra'])
    count = 0
    for key in data.columns:
        data[key] = dann[count]
        data_orig[key] = dann[count]
        count+=1
    print("\n\n")
    print(data.index)
    print(list(data.index))
    print("получаемый последний индекс ", data.index[-1])
    print("получаемый последний индекс(из списка) ", list(data.index)[-1])
    if not(new_row in data.columns): # если столбец не найден в таблице
        empty_list = [""] * (data.index[-1])
        empty_list.append(new_value)
        print(empty_list)
        list_S = pd.DataFrame(empty_list, columns=[new_row])
        #data[new_row] = list_S
        data = pd.concat([data,list_S], axis=1)
        print(data)

        #data_index = data.index[-1]
        #data[new_row][data_index] = new_value
        #print(data[new_row])

    #print(data_orig.concat(data))


    #print(data)
    #print(data.loc[3])

    list_col = list(data.columns)
    print(list_col)
    for i in range(len(list_col)):
        #list_col[i] = "".join(list_col[i].split()) # удаляет все виды пробелов, перенос строки, знаки табуляции и т.п.
        list_col[i] = list_col[i].replace(" ","") # удаляет только пробелы внутри строки, оставляя \n, \t
    print(list_col)


#print(len(list(soup.children))) # дочерние элементы
#print(len(list(soup.descendants))) # потомки

#print(list(soup.descendants))
#print(len(list(soup.contents)))
#print(soup.contents[2])
# позволяет перебирать все дочерние элементы (у тега дочерний элемент строка) тега рекурсивно:
# его непосредственные дочерние элементы, дочерние элементы
# дочерних элементов и так далее.

#print(list(soup.children)) # дочерние элементы
#print(soup.find_all('div'))
#for sibling in soup.find_all("data-result-container").previous_siblings:
#    print(repr(sibling))


# a = "Типы поддерживаемых карт памяти microSD, microSDHC, microSDXC"
# b = "Типы поддерживаемых карт памяти"
# size_b = len(b)
# c = a[size_b:]
# print(c)
