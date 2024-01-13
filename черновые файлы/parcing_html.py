from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui

from bs4 import BeautifulSoup
import pandas as pd
import itertools


def download_links(tree_BS4):
    # поиск тегов <a> с определенным классом по дереву
    Nodes = tree_BS4.find_all("a", class_="catalog-product__name")
    List_link = list()
    for i in range(len(Nodes)):
        List_link.append(Nodes[i]['href'])
        # print(f"{len(temp[i].attrs):>50}  \t=>\t {temp[i].attrs},\n\n")
    return List_link


def collections_title_value(tree_BS4, current_DataBase: pd.DataFrame, path: str):
    names_classes = {'title': 'product-characteristics__spec-title',
                     'value': 'product-characteristics__spec-value'}
    # TR = Translator(from_lang="ru", to_lang="en")
    stringe = str()
    Nodes = tree_BS4.find_all("div", class_="product-characteristics__group")  # поиск объекта с группами характеристик
    example_type = type(tree_BS4.find('div'))  # для проверки типа "Tag" и наличия метода attrs
    current_columns = current_DataBase.columns  # столбцы текущей БД, которую передали как параметр
    unused_names_columns = current_DataBase.columns
    list_unused_names_columns = list(unused_names_columns)
    # буферная однострочная БД для склеивания с текущей,
    # создается на основе столбцов текущей БД
    buffer_DataBase = pd.DataFrame(columns=current_columns)

    """Сбор характеристик по DOM-дереву конкретного телефона"""
    # по каждой группе с харатеристиками
    for i in range(len(Nodes)):
        List_child = Nodes[i].descendants

        flag_title = False
        flag_value = False
        name_title = str()
        value_title = str()

        # Прямой дочерний элемент - это дочерний элемент,
        # который находится непосредственно под родительским
        # элементом с точки зрения иерархии. То есть не внук или правнук.

        # по каждому полю в группе
        TITLE_None = 0
        for child in List_child:
            # Проверка на то, что это тэг и у него будет метод attrs
            if type(child) is example_type:
                if 'class' in child.attrs:
                    if names_classes['title'] in child['class']:  # a in b, a-строка, b-список
                        if child.string is None:
                            # создание среза из генератора дочерних элементов, для перехода к следующему
                            list_name_title = list(
                                itertools.islice(Nodes[i].descendants, TITLE_None + 1, TITLE_None + 2))
                            name_title = list_name_title[0]
                            flag_title = True

                            # t1 = Class_Timer.Timer()
                            # t1.start()
                            # res = TR.translate(name_title)
                            # t1.stop()
                            # print("title: ", name_title)
                            # stringe = " ".join([stringe,name_title])
                            # print(stringe)
                        else:
                            name_title = child.string

                            flag_title = True
                    elif names_classes['value'] in child['class']:
                        value_title = child.string
                        flag_value = True

                    if flag_title and flag_value:
                        if value_title is None:
                            value_title = 'Перечисление'
                        temp = value_title.encode('utf-8').decode('utf-8')

                        if (name_title in list_unused_names_columns):  # Удаление использованных имен столбцов
                            list_unused_names_columns.remove(name_title)
                        buffer_DataBase[name_title] = [temp.replace(" ", "")]  # удаление пробелов
                        flag_title = False
                        flag_value = False

            TITLE_None += 1

    """Подсчет кол-во новых столбцов"""
    old_and_new_columns = buffer_DataBase.columns
    count_current_columns = len(current_columns)
    count_old_and_new_columns = len(old_and_new_columns)
    #count_new_columns = count_old_and_new_columns - count_current_columns  # нашел число новых столбцов

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

    Series_new_columns = pd.Series(old_and_new_columns)  # формирую Series на основе имеющихся столбцов из буферной БД

    # Беру срез из Series, начиная с последнего столбца текущей БД +1
    # Вытаскиваю индексы "новых" столбцов и формирую из них список
    index_new_columns = list(Series_new_columns[count_current_columns:].index)
    names_new_columns = list()
    for i in index_new_columns:
        names_new_columns.append(Series_new_columns[i])

    """Добавление новых столбцов к текущей БД и заполнение для старых телефонов каждой ячейки нового столбца затычкой"""
    # кол-во ячеек в столбцах
    temp = list(current_DataBase.index)
    if len(temp):
        count_box = temp[-1] + 1  # индекс последней строки в текущей БД
    else:
        count_box = 0
    list_empty = [""] * count_box

    # добавление пустых столбцов к текущей БД
    for name_column in names_new_columns:
        current_DataBase[name_column] = list_empty

    # Конкатенация буферной БД и текущей
    current_DataBase = pd.concat([current_DataBase, buffer_DataBase], ignore_index=True)

    flag_print = False
    keys = current_DataBase.columns
    if flag_print:
        for key in keys:
            print(f"{current_DataBase[key]}\n")
    # t1 = Class_Timer.Timer()
    # t1.start()
    # res = TR.translate(stringe)
    # t1.stop()
    # print(res)

    return current_DataBase


def Save_html(name):
    time.sleep(5)
    # "Сохранить как..."
    pyautogui.keyDown('ctrl')  # hold ctrl key
    pyautogui.press('s')  # press s key
    pyautogui.keyUp('ctrl')  # release ctrl key
    # print("Not found")
    time.sleep(3)
    FILE_NAME = name  # имя, под которым сохранится HTML-файл: 'dns3.html'
    pyautogui.typewrite(FILE_NAME)  # ввести заданное имя в окно в браузере
    pyautogui.press(['tab', 'down', 'up', 'up', 'enter'])
    pyautogui.press('enter')
    time.sleep(5)



def download_pages(url):
    s = Service('C:\\Users\\79182\\chromedriver_win32\\chromedriver.exe')
    driver = webdriver.Chrome(service=s)  # запустить браузер
    driver.implicitly_wait(1)
    driver.maximize_window()  # открыть окно браузера на весь экран
    # перейти по ссылке URL
    driver.get(url)

    num_page_old = 1
    name = 'dns' + str(num_page_old - 1) + '.html'
    Save_html(name)

    while (True):
        name = 'dns' + str(num_page_old - 1) + '.html'
        with open('C:\\Users\\79182\\Downloads\\' + name, 'r', encoding="utf-8") as name_html:
            soup = BeautifulSoup(name_html, 'lxml')
            res = soup.find_all("a", class_="pagination-widget__page-link")
            for i in range(len(res) - 1, 0, -1):
                # print(f"{res[i].text:>10}", "\n")
                num_page_new = res[i].text
                print(num_page_new)
                if (len(num_page_new) != 0):
                    break
                # print(res[i].prettify())
            print('num_page_new = ', num_page_new)
            print('num_page_old = ', num_page_old)
        if (num_page_old < int(num_page_new)):
            for i in range(num_page_old, int(num_page_new)):
                try:
                    time.sleep(3)
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[text()="Показать ещё" and not(@disabled)]')))
                    time.sleep(5)
                    # перейти на следующую страницу
                    driver.find_element(By.XPATH, '//button[text()="Показать ещё" and not(@disabled)]').click()
                    # driver.find_element(By.CLASS_NAME, 'pagination-widget__page-link pagination-widget__page-link_next').click()
                except:
                    print("Not click", i)
                    num_page_old = i
                    break
                name = 'dns' + str(i) + '.html'
                Save_html(name)
                num_page_old = i + 1  # int(num_page_new)
                print("num_page_old: i+1 =", num_page_old)
        else:
            break
    return num_page_old



def download_unic_pages(unic_url):
    s = Service('C:\\Users\\79182\\chromedriver_win32\\chromedriver.exe')
    driver = webdriver.Chrome(service=s)  # запустить браузер
    driver.implicitly_wait(1)
    driver.maximize_window()  # открыть окно браузера на весь экран
    for i in range(0, len(unic_url)):
        # перейти по ссылке URL
        driver.get(unic_url[i])
        try:
            time.sleep(3)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Развернуть все" and not(@disabled)]')))
            time.sleep(3)
            # перейти на следующую страницу
            driver.find_element(By.XPATH, '//button[text()="Развернуть все" and not(@disabled)]').click()
            # driver.find_element(By.CLASS_NAME, 'pagination-widget__page-link pagination-widget__page-link_next').click()
        except:
            print("Not click")
            break
        else:
            name = 'dns_unic_' + str(i) + '.html'
            Save_html(name)


# _______________________________________________________________________________________
path = 'C:\\Users\\79182\\Downloads\\'
url = "https://www.dns-shop.ru/search/?q=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%D1%8B+xiaomi+poco&category=17a8a01d16404e77"

num_page_old = download_pages(url) # кол-во скачанных страниц, из к-х нужно доставать ссылки
print("download_pages - good")

unic_url = list()
for i in range(0, num_page_old):
    name = 'dns' + str(i) + '.html'
    with open(path + name, 'r', encoding="utf-8") as html_file:
        tree = BeautifulSoup(html_file, "lxml")
        buffer = download_links(tree_BS4=tree)
        for i in range(len(buffer)):
            print(buffer[i], sep=", ")
        for i in range(len(buffer)):
            unic_url.append("https:/www.dns-shop.ru" + buffer[i])
download_unic_pages(unic_url)

print("download_unic_pages - good")

# _______________________________________________________________________________________
