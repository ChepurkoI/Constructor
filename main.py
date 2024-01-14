from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta

import time
# from time import sleep
import pyautogui
import os
import requests
import json

import pprint

from bs4 import BeautifulSoup
import pandas as pd
import itertools




class constructor():

    def __init__(self,
                 name_website="dns",  # имя сайта на английском
                 name_product="Смартфон",  # наименование продукта
                 url_product="",  # url первой страницы поиска
                 encoding="",
                 name_tag="",
                 name_class="",

                 name_tag_title="",
                 name_class_title="",

                 name_tag_value="",
                 name_class_value="",
                 name_characteristics="",

                 web_driver="",  # расположение chromedriver.exe
                 path_downloads="", # путь до папки "Загрузки"
                 separator_for_path='',

                 name_teg_last_page="a",  # тег номера последней страницы, отображ-ся на сайте
                 name_attribute_last_page="class",  # по какому атрибуту искать номер последней страницы (class/role)
                 name_class_last_page="pagination-widget__page-link",
                 # имя класса номера последней страницы, отображ-ся на сайте
                 button_text_new_page="Показать ещё",  # текст на кнопке, которая переводит на след. страницу поиска
                 button_characteristics="Развернуть все"  # текст на кнопке, которая открывает хар-ки
                 ):

        # сведения для скачивания страниц

        # Переданные параметры для chromedriver и папки Загрузки
        self.web_driver = web_driver
        self.path_downloads = path_downloads
        self.separator_for_path = separator_for_path

        # местоположение chromedriver
        if web_driver == "": # если параметр не задан
            if platform == "linux" or platform == "linux2":
                self.web_driver = "/home/ingvar/PycharmProjects/parser/parsing_constructor/chromedriver_linux64/chromedriver"
            elif platform == "win32":
                self.web_driver = "C:\\Users\\Ingvar\\PycharmProjects\\\\chromedriver_win64\\chromedriver.exe"

        # путь до папки "Загрузки"
        if path_downloads == "":  # если параметр не задан
            if platform == "linux" or platform == "linux2":
                self.path_downloads = "/home/ingvar/Загрузки"
            elif platform == "win32":
                self.path_downloads = "C:\\Users\\Ingvar\\Downloads"

        # разделитель для указания пути к файлам\папкам
        if separator_for_path == "":  # если параметр не задан
            if platform == "linux" or platform == "linux2":
                self.separator_for_path = "/"
            elif platform == "win32":
                self.separator_for_path = "\\"

        # общие сведения
        self.name_website = name_website  # имя сайта, с которым работаем,
        self.name_product = name_product  # имя товара, например: телефон, пылесос
        self.url_product = url_product  # ссылка на раздел исследуемого товара
        self.encoding = encoding  # кодировка страницы товара
        self.name_tag = name_tag
        self.name_class = name_class

        # сведения по заголовку хар-ки
        self.name_tag_title = name_tag_title  # имя тега заголовка хар-ки, по которому ищем
        self.name_class_title = name_class_title  # имя класса, по которому ищем

        # сведения по зн-ю хар-ки
        self.name_tag_value = name_tag_value  # имя тега зн-я хар-ки, по которому ищем
        self.name_class_value = name_class_value  # имя класса, по которому ищем
        self.name_characteristics = name_characteristics  # имя характеристики


        self.name_teg_last_page = name_teg_last_page  # тег номера последней страницы, отображ-ся на сайте
        self.name_attribute_last_page = name_attribute_last_page  # по какому атрибуту искать номер последней страницы (class/role)
        self.name_class_last_page = name_class_last_page  # имя класса номера последней страницы, отображ-ся на сайте
        self.button_text_new_page = button_text_new_page  # текст на кнопке, которая переводит на след. страницу поиска
        self.button_characteristics = button_characteristics  # текст на кнопке, которая открывает хар-ки

        self._url_server = "https://35a4-89-179-47-36.eu.ngrok.io/api/information/"
        self._tree_dom_bs4 = None
        self._list_rules = []


    def get_request(self):
        # 'https://a2da-89-179-47-18.eu.ngrok.io/api/information/'

        if "api/information" in self._url_server:
            get_result = requests.get(self._url_server)
            #print(get_result.text)
            dict_result = dict(get_result.json())
        else:
            print("В названии ссылки на сервер отсутствует в конце api/information")

        """Единожды / one"""
        # общие сведения
        self.name_website = dict_result['designer']['one']['site']
        self.name_product = dict_result['designer']['one']['type_product']
        self.url_product = dict_result['designer']['one']['url']

        self.name_tag = dict_result['designer']['one']['teg_name_url']
        self.name_class = dict_result['designer']['one']['class_name_url']

        # сведения для скачивания страниц
        self.name_teg_last_page = dict_result['designer']['one']['teg_name_number']
        self.name_attribute_last_page = dict_result['designer']['one']['role_name_url']
        self.name_class_last_page = dict_result['designer']['one']['class_name_number']
        self.button_text_new_page = dict_result['designer']['one']['name_button']

        #???self.button_characteristics = dict_result['designer']

        """Многократно / many"""

        temp = dict_result['designer']['many']
        print(f"Число правил для товара: {len(temp)}")
        for dict_param in temp:
            print(f"{dict_param['title']} : {len(dict_param['title'])}")
            print(f"{dict_param['teg_name']}: {len(dict_param['teg_name'])}")
            print(f"{dict_param['class_name']} : {len(dict_param['class_name'])}")


        # сведения по заголовку хар-ки

        self._list_rules = dict_result['designer']['many'] # список из словарей, ключами являются название хар-ки, тег и аттрибуты
        # self.name_tag_title = dict_result['designer']
        # self.name_class_title = dict_result['designer']

        # # сведения по зн-ю хар-ки
        #self.name_tag_value = dict_result['designer']
        # self.name_class_value = dict_result['designer']
        # self.name_characteristics = dict_result['designer']


    def download_links(self):
        """
            Метод для вытаскивания ссылок из страниц товаров
            Для работы метода необходимо, чтобы были переданы параметры

        """
        type_value = "href"

        files = os.listdir(self.path_downloads + self.separator_for_path + self.name_website)
        count_sait = list(filter(lambda x: x.endswith('.html'), files))
        # print("count_sait", count_sait)
        num_page_old = len(count_sait)  # кол-во скачанных страниц, из к-х нужно доставать ссылки
        # print(num_page_old)
        num_page_old -= num_page_old-1

        for i in range(0, num_page_old):
            name_file = self.name_website + str(i) + '.html'

            with open(self.path_downloads + self.separator_for_path + self.name_website + self.separator_for_path + name_file,
                      "r",
                      encoding='utf-8') as html_file:
                self._tree_dom_bs4 = BeautifulSoup(html_file, 'lxml')


            # поиск тегов  с определенным классом по дереву
            if self.name_tag != "" and self.name_class != "":
                Nodes = self._tree_dom_bs4.find_all(self.name_tag, class_=self.name_class)
            elif self.name_tag != "" and self.name_class == "":
                Nodes = self._tree_dom_bs4.find_all(self.name_tag)
            print(f"Количество возможных ссылок: {len(Nodes)}")
            print(f"{self.name_tag}, {self.name_class}")
            with open(self.path_downloads + self.separator_for_path + self.name_website + self.separator_for_path + "product_links.txt", "a",
                      encoding='utf-8') as file:
                for i in range(len(Nodes)):
                    # print(Nodes[i].prettify())
                    #print(f"Модель: {Nodes[i].text}")
                    if self.name_product + " " in Nodes[i].text:

                        if 'href' in Nodes[i].attrs:
                            #print(f"Ссылка: {Nodes[i][type_value]}\n\n")
                            temp_link = Nodes[i][type_value]
                            main_piece_url = ""

                            # Проверка, что ссылка полная
                            if "https://" in temp_link:
                                if self.name_website in temp_link:
                                    pass
                            elif "http://" in temp_link:
                                if self.name_website in temp_link:
                                    pass
                            else:
                                http_or_s = 0
                                if "https://" in self.url_product:
                                    http_or_s = len("https://")
                                elif "http://" in self.url_product:
                                    http_or_s = len("http://")
                                index_end = self.url_product[http_or_s:].find("/")
                                # print()
                                main_piece_url = self.url_product[:http_or_s + index_end]

                            file.write(main_piece_url + temp_link + "\n")


    def download_links_old(self, path, name, tree_BS4=""):
        with open(path + name, 'r', encoding='utf-8') as html_file:
            tree_BS4 = BeautifulSoup(html_file, 'lxml')
            # поиск тегов <a> с определенным классом по дереву
            Nodes = tree_BS4.find_all("a", class_="catalog-product__name")
            with open(path + "product_links.txt", "w", encoding='utf-8') as file:
                for i in range(len(Nodes)):
                    file.write(Nodes[i]['href'] + "\n")


    """
    def collections_title_value(tree_BS4, current_DataBase: pd.DataFrame, path: str):
        names_classes = {'title': 'product-characteristics__spec-title',
                         'value': 'product-characteristics__spec-value'}
        # TR = Translator(from_lang="ru", to_lang="en")
        stringe = str()
        Nodes = tree_BS4.find_all("div",
                                  class_="product-characteristics__group")  # поиск объекта с группами характеристик
        example_type = type(tree_BS4.find('div'))  # для проверки типа "Tag" и наличия метода attrs
        current_columns = current_DataBase.columns  # столбцы текущей БД, которую передали как параметр
        unused_names_columns = current_DataBase.columns
        # print(type(unused_names_columns))
        list_unused_names_columns = list(unused_names_columns)

        # буферная однострочная БД для склеивания с текущей,
        # создается на основе столбцов текущей БД
        buffer_DataBase = pd.DataFrame(columns=current_columns)

        #Сбор характеристик по DOM-дереву конкретного телефона
        # по каждой группе с харатеристиками
        for i in range(len(Nodes)):
            # print(f"{Nodes[i].text:>50} ,\n")
            # print(Nodes[i].prettify())
            # print(Nodes[i].prettify())
            List_child = Nodes[i].descendants
            # print("List_child: ", len(list(List_child)))
            count = 0

            flag_title = False
            flag_value = False
            name_title = str()
            value_title = str()

            # Прямой дочерний элемент - это дочерний элемент,
            # который находится непосредственно под родительским
            # элементом с точки зрения иерархии. То есть не внук или правнук.
            # print(f"{Nodes[i].text:>50} ,\n")
            # по каждому полю в группе
            TITLE_None = 0
            for child in List_child:
                # print(count, end=" ")
                # count += 1
                # print("\t ", type(child), ": ", child, "\n")

                # Проверка на то, что это тэг и у него будет метод attrs
                if type(child) is example_type:
                    if 'class' in child.attrs:
                        # print(child.attrs)
                        # print(names_classes['title'] in child['class'])
                        if names_classes['title'] in child['class']:  # a in b, a-строка, b-список
                            # print(child.string)
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
                                # name_title = child.string # не работает, так как берет None, вместо строки
                                name_title = child.string

                                # stringe = " ".join([stringe,name_title])
                                flag_title = True
                                # print("title", name_title)
                                # print(stringe)
                        elif names_classes['value'] in child['class']:
                            value_title = child.string
                            flag_value = True
                            # print("value: ", value_title) # .encode('utf-8'))

                        if flag_title and flag_value:
                            if value_title is None:
                                value_title = 'Перечисление'
                            temp_value = value_title.encode('utf-8').decode('utf-8')

                            if (name_title in list_unused_names_columns):  # Удаление использованных имен столбцов
                                list_unused_names_columns.remove(name_title)

                            # удаление пробелов
                            temp_value = temp_value.lstrip()
                            temp_value = temp_value.rstrip()
                            temp_name = name_title
                            temp_name = temp_name.lstrip()
                            temp_name = temp_name.rstrip()
                            buffer_DataBase[temp_name] = [temp_value]  # .replace(" ", "")
                            flag_title = False
                            flag_value = False

                # print("child.string = ", child.string, end="\n\n")
                # print("\n\n")
                TITLE_None += 1
            # print("\n\n")

        # Подсчет кол-во новых столбцов
        old_and_new_columns = buffer_DataBase.columns
        count_current_columns = len(current_columns)
        count_old_and_new_columns = len(old_and_new_columns)
        count_new_columns = count_old_and_new_columns - count_current_columns  # нашел число новых столбцов

        # Извлечение имен новых столбцов
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

        Series_new_columns = pd.Series(
            old_and_new_columns)  # формирую Series на основе имеющихся столбцов из буферной БД

        # Беру срез из Series, начиная с последнего столбца текущей БД +1
        # Вытаскиваю индексы "новых" столбцов и формирую из них список
        index_new_columns = list(Series_new_columns[count_current_columns:].index)
        names_new_columns = list()
        for i in index_new_columns:
            names_new_columns.append(Series_new_columns[i])

        # Добавление новых столбцов к текущей БД и заполнение для старых телефонов каждой ячейки нового столбца затычкой
        # кол-во ячеек в столбцах
        temp = list(current_DataBase.index)
        if len(temp):
            count_box = temp[-1] + 1  # индекс последней строки в текущей БД
        else:
            count_box = 0
        list_empty = [""] * count_box

        DF_list_empty = pd.DataFrame(list_empty, columns=[name])

        # добавление пустых столбцов к текущей БД
        for name_column in names_new_columns:
            DF_list_empty = pd.DataFrame(list_empty, columns=[name_column])
            current_DataBase = pd.concat([current_DataBase, DF_list_empty], axis=1)
            # current_DataBase[name_column] = list_empty

        # Конкатенация буферной БД и текущей
        # print("Текущая БД: ", current_DataBase)
        # print("Буферная БД: ",buffer_DataBase)
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

        # if len(unused_names_columns): # если остались неиспользованные имена столбцов
        #     last_index = current_DataBase.index[-1]
        #     for name_column in unused_names_columns: # для каждого имени вставляем затычку
        #         current_DataBase[name_column, last_index] = ""
        return current_DataBase
    """


    def Save_html(self, name):
        """name - имя, под которым сохранится файл"""
        time.sleep(6)
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
        # Проверяем, как только получится открыть файл, значит он сохранился, можно переходить к следующему действию

        wait_end_time = datetime.now() + timedelta(seconds=15)

        while datetime.now() < wait_end_time:
            try:
                f = open(self.path_downloads + self.separator_for_path + name)
                f.close()
                break
            except:
                # print(5, end = '')
                time.sleep(.1)
        else:
            raise Exception('Save error')
        # time.sleep(5)


    def my_wait(driver, min_wait=0.0, max_wait=60.0):
        wait_end_time = datetime.now() + timedelta(seconds=max_wait)

        while datetime.now() < wait_end_time:
            if driver.execute_script('return document.readyState != "complete";'):
                time.sleep(min_wait)
            else:
                break
        else:
            raise Exception('timeout error')


    def download_pages(self):


        # Создание/переименовывание папки, в которой будут лежать скачанные страницы
        if not os.path.isdir(self.path_downloads + self.separator_for_path + self.name_website):
            os.mkdir(self.path_downloads + self.separator_for_path + self.name_website)
        else:
            os.rename(self.path_downloads + self.separator_for_path + self.name_website,
                      self.path_downloads + self.separator_for_path + self.name_website + str(datetime.now().date()) +
                      '_' + str(datetime.now().microsecond))
            os.mkdir(self.path_downloads + self.separator_for_path + self.name_website)

        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)  # запустить браузер

        driver.implicitly_wait(1)
        driver.maximize_window()  # открыть окно браузера на весь экран

        try:
            driver.get(self.url_product)  # перейти по ссылке URL
            # my_wait(driver, 0.1, 30)
            num_page_old = 1
            name = self.name_website + str(num_page_old - 1) + '.html' # Имя страницы

            # извлечение и сохранение данных страницы в папку в файл
            page = driver.find_element(By.XPATH, "//body").get_attribute("outerHTML")
            with open(self.path_downloads + self.separator_for_path + self.name_website + "\\" + name, "w", encoding="utf-8") as file:
                file.write(page)
            time.sleep(5)
            """
            self.Save_html(name)
            os.replace(self.path_downloads + self.separator_for_path + name,
                       self.path_downloads + self.separator_for_path + self.name_website + "\\" + name)
            # print("pered while")
            """
            flag_not_click = 0
            while (True):

                # Поиск количества страниц в скачанном файле
                name = self.name_website + str(num_page_old - 1) + '.html'
                with open(self.path_downloads + self.separator_for_path + self.name_website + self.separator_for_path + name,
                          'r', encoding="utf-8") as name_html:
                    soup = BeautifulSoup(name_html, 'lxml')
                    if (self.name_attribute_last_page == 'class'):
                        res = soup.find_all(self.name_teg_last_page, class_=self.name_class_last_page)
                    elif (self.name_attribute_last_page == 'role'):
                        res = soup.find_all(self.name_teg_last_page, role=self.name_class_last_page)

                    print(res)

                    list_last_page = list()
                    for i in range(len(res)):
                        temp_num = res[i].text
                        if temp_num.isdigit():
                            list_last_page.append(int(temp_num))
                            # print(f"Атрибуты: {res[i].attrs}\n\n")
                        else:
                            continue
                    print("Список обнаруженных страниц: ", len(list_last_page))
                    num_page_new = max(list_last_page)
                    # print(f"Номер последней страницы: {max(list_last_page)}")
                    """
                    for i in range(len(res) - 1, 0, -1):
                        # print(f"{res[i].text:>10}", "\n")
                        num_page_new = res[i].text
                        print(num_page_new)
                        if (len(num_page_new) != 0):
                            break
                        # print(res[i].prettify())
                    """
                    print('num_page_new = ', num_page_new)
                    print('num_page_old = ', num_page_old)


                if (num_page_old < int(num_page_new)):
                    for i in range(num_page_old, int(num_page_new)):
                        try:
                            time.sleep(3)
                            print("------------------")
                            # WebDriverWait(driver, 10).until(
                            #   EC.element_to_be_clickable(
                            #        (By.XPATH, '//button[text()="' + self.button_text_new_page +
                            #         '" and not(@disabled)]')))
                            time.sleep(2)
                            # my_wait(driver, 0.1, 30)
                            # driver.implicitly_wait(10)
                            # print("Тип найденного элемента:")

                            # print("Тип найденного элемента: ", type(driver.find_element(By.XPATH, '//button[text()="' + self.button_text_new_page + '"]')))
                            driver.find_element(By.XPATH, '//button[text()="' + self.button_text_new_page + '"]').click()
                            # '" and not(@disabled)]').click()
                            # для dns
                            # driver.find_element(By.CLASS_NAME, 'pagination-widget__page-link pagination-widget__page-link_next').click()
                            # для citilink
                            # print(driver.find_element(By.CLASS_NAME, 'e4uhfkv0 app-catalog-1ls3bkl e4mggex0'))
                            # driver.find_element(By.XPATH, "//button[@class='e4uhfkv0 app-catalog-1ls3bkl e4mggex0']").click()
                            # driver.find_element(By.CLASS_NAME, 'e4uhfkv0').click()
                            # my_wait(driver, 0.1, 30)
                        except:
                            print("Not click", i)
                            flag_not_click += 1
                            num_page_old = i
                            break
                        name = self.name_website + str(i) + '.html'
                        # my_wait(driver, 0.1, 30)
                        page = driver.find_element(By.XPATH, "//body").get_attribute("outerHTML")

                        with open(self.path_downloads + self.separator_for_path + self.name_website + "\\" + name, "w",
                                  encoding="utf-8") as file:
                            file.write(page)
                        time.sleep(1)
                        """
                        self.Save_html(name)
                        os.replace(self.path_downloads + self.separator_for_path + name,
                                   self.path_downloads + self.separator_for_path + self.name_website + "\\" + name)
                        """

                        num_page_old = i + 1  # int(num_page_new)
                        print("num_page_old: i+1 =", num_page_old)
                    if (flag_not_click > 0): break
                else:
                    break
        except Exception as ex:
            print(ex)
            driver.quit()


    def download_pages_old(self):
        if not os.path.isdir(self.path_downloads + '\\' + self.name_website):
            os.mkdir(self.path_downloads + '\\' + self.name_website)
        else:
            os.rename(self.path_downloads + '\\' + self.name_website,
                      self.path_downloads + '\\' + self.name_website + str(datetime.now().date()) +
                      '_' + str(datetime.now().microsecond))
            os.mkdir(self.path_downloads + '\\' + self.name_website)
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)  # запустить браузер
        driver.implicitly_wait(1)
        driver.maximize_window()  # открыть окно браузера на весь экран

        try:
            # перейти по ссылке URL
            driver.get(self.url_product)
            # my_wait(driver, 0.1, 30)
            num_page_old = 1
            name = self.name_website + str(num_page_old - 1) + '.html'
            self.Save_html(name)
            os.replace(self.path_downloads + '\\' + name,
                       self.path_downloads + '\\' + self.name_website + "\\" + name)
            print("pered while")
            flag_not_click = 0
            while (True):
                name = self.name_website + str(num_page_old - 1) + '.html'
                with open(self.path_downloads + '\\' + self.name_website + '\\' + name,
                          'r', encoding="utf-8") as name_html:
                    soup = BeautifulSoup(name_html, 'lxml')
                    if (self.name_attribute_last_page == 'class'):
                        res = soup.find_all(self.name_teg_last_page, class_=self.name_class_last_page)
                    elif (self.name_attribute_last_page == 'role'):
                        res = soup.find_all(self.name_teg_last_page, role=self.name_class_last_page)
                    list_last_page = list()
                    for i in range(len(res)):
                        temp_num = res[i].text
                        if temp_num.isdigit():
                            list_last_page.append(int(temp_num))
                            # print(f"Атрибуты: {res[i].attrs}\n\n")
                    num_page_new = max(list_last_page)
                    # print(f"Номер последней страницы: {max(list_last_page)}")
                    """
                    for i in range(len(res) - 1, 0, -1):
                        # print(f"{res[i].text:>10}", "\n")
                        num_page_new = res[i].text
                        print(num_page_new)
                        if (len(num_page_new) != 0):
                            break
                        # print(res[i].prettify())
                    """
                    print('num_page_new = ', num_page_new)
                    print('num_page_old = ', num_page_old)
                if (num_page_old < int(num_page_new)):
                    for i in range(num_page_old, int(num_page_new)):
                        try:
                            time.sleep(3)
                            WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//button[text()="' + self.button_text_new_page +
                                     '" and not(@disabled)]')))
                            time.sleep(2)
                            # my_wait(driver, 0.1, 30)
                            # driver.implicitly_wait(10)
                            # перейти на следующую страницу
                            driver.find_element(By.XPATH, '//button[text()="' + self.button_text_new_page +
                                                '" and not(@disabled)]').click()
                            # driver.find_element(By.CLASS_NAME, 'pagination-widget__page-link pagination-widget__page-link_next').click()
                            # my_wait(driver, 0.1, 30)
                        except:
                            print("Not click", i)
                            flag_not_click += 1
                            num_page_old = i
                            break
                        name = self.name_website + str(i) + '.html'
                        # my_wait(driver, 0.1, 30)
                        self.Save_html(name)
                        os.replace(self.path_downloads + '\\' + name,
                                   self.path_downloads + '\\' + self.name_website + "\\" + name)
                        num_page_old = i + 1  # int(num_page_new)
                        print("num_page_old: i+1 =", num_page_old)
                    if (flag_not_click > 0): break
                else:
                    break
        except Exception as ex:
            print(ex)
            driver.quit()


    def download_unic_pages(self):


        if not os.path.isdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic'):
            os.mkdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic')
        else:
            os.rename(self.path_downloads + self.separator_for_path + self.name_website + '_unic',
                      self.path_downloads + self.separator_for_path + self.name_website + '_unic' + str(datetime.now().date()) +
                      '_' + str(datetime.now().microsecond))
            os.mkdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic')
        unic_url = list()
        with open(self.path_downloads + self.separator_for_path + self.name_website + self.separator_for_path + "product_links.txt", "r",
                  encoding='utf-8') as file:
            for line in file:
                # unic_url.append(self.head_url + line)
                unic_url.append(line)
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)  # запустить браузер
        driver.implicitly_wait(1)
        driver.maximize_window()  # открыть окно браузера на весь экран
        for i in range(0, len(unic_url)):
            # перейти по ссылке URL
            driver.get(unic_url[i])
            try:
                time.sleep(2)
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="' + self.button_characteristics +
                                                '" and not(@disabled)]')))
                time.sleep(2)
                driver.find_element(By.XPATH, '//button[text()="' + self.button_characteristics +
                                    '" and not(@disabled)]').click()

                # driver.find_element(By.CLASS_NAME, 'pagination-widget__page-link pagination-widget__page-link_next').click()
            except:
                print("Not click")
                continue
            else:
                try:
                    time.sleep(2)
                    name = self.name_website + '_unic_' + str(i) + '.html'
                    page = driver.find_element(By.XPATH, "//*").get_attribute("outerHTML")
                    with open(self.path_downloads + self.separator_for_path + self.name_website + '_unic' + self.separator_for_path + name, "w",
                              encoding="utf-8") as file:
                        file.write(page)
                    time.sleep(1)
                    """
                    self.Save_html(name)
                    os.replace(self.path_downloads + self.separator_for_path + name,
                               self.path_downloads + self.separator_for_path + self.name_website + '_unic' + self.separator_for_path + name)
                    """
                except Exception as ex:
                    print(ex)
                    driver.quit()


    def download_unic_pages_old(self):
        if not os.path.isdir(self.path_downloads + '\\' + self.name_website + '_unic'):
            os.mkdir(self.path_downloads + '\\' + self.name_website + '_unic')
        else:
            os.rename(self.path_downloads + '\\' + self.name_website + '_unic',
                      self.path_downloads + '\\' + self.name_website + '_unic' + str(datetime.now().date()) +
                      '_' + str(datetime.now().microsecond))
            os.mkdir(self.path_downloads + '\\' + self.name_website + '_unic')
        unic_url = list()
        with open(self.path_downloads + '\\' + self.name_website + '\\' + "product_links.txt", "r",
                  encoding='utf-8') as file:
            for line in file:
                unic_url.append(self.head_url + line)
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)  # запустить браузер
        driver.implicitly_wait(1)
        driver.maximize_window()  # открыть окно браузера на весь экран
        for i in range(0, len(unic_url)):
            # перейти по ссылке URL
            driver.get(unic_url[i])
            try:
                time.sleep(2)
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="' + self.button_characteristics +
                                                '" and not(@disabled)]')))
                time.sleep(2)
                # перейти на следующую страницу
                driver.find_element(By.XPATH, '//button[text()=" ' + self.button_characteristics +
                                    '" and not(@disabled)]').click()
                # driver.find_element(By.CLASS_NAME, 'pagination-widget__page-link pagination-widget__page-link_next').click()
            except:
                print("Not click")
                break
            else:
                try:
                    name = self.name_website + '_unic_' + str(i) + '.html'
                    self.Save_html(name)
                    os.replace(self.path_downloads + '\\' + name,
                               self.path_downloads + '\\' + self.name_website + '_unic' + '\\' + name)
                except Exception as ex:
                    print(ex)
                    driver.quit()


    def extraction_data(self):



        files = os.listdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic')
        list_files = list(filter(lambda x: x.endswith('.html'), files))
        print(f"Кол-во скачанных страниц товара: \n{len(list_files)}")
        temp_dict = dict()
        dict_for_post_request = dict()
        dict_for_post_request['site'] = self.name_website
        dict_for_post_request['type_product'] = self.name_product
        for rule in self._list_rules:
            temp_dict[rule['title']] = list()

        # По всем скачанным файлам товара
        for name_file in list_files:
            #name = self.name_website + '_unic_' + str(i) + '.html'
            with open(self.path_downloads + self.separator_for_path + self.name_website + '_unic' + self.separator_for_path + name_file,
                      'r',encoding="utf-8") as html_file:
                self._tree_dom_bs4 = BeautifulSoup(html_file, "lxml")

            list_unused_name = list(temp_dict.keys())
            # По всем полученным правилам
            for rule in self._list_rules:

                str_title = rule['title']
                str_all = str()
                Nodes_all = self._tree_dom_bs4.find_all(rule['teg_name'], class_=rule['class_name'])
                #print(len(Nodes_all))
                for i in range(len(Nodes_all)):
                    temp_str = Nodes_all[i].text

                    if rule['title'] in temp_str:
                        list_unused_name.remove(rule['title'])
                        str_all = str(temp_str).replace("  ", " ")
                        str_all = " ".join(str_all.split())
                        break
                size_title = len(str_title)

                temp_dict[str_title].append(str_all[size_title:])
                #print(f"{str_title}:{str_all[size_title:]}")

            # По всем неиспользованным именам хар-тик из правил
            for unused_name in list_unused_name:
                temp_dict[unused_name].append("") # вставить заглушки

        dict_for_post_request['data'] = temp_dict

        #url = "https://35a4-89-179-47-36.eu.ngrok.io/api/information/"
        dict_for_post_request = json.dumps(dict_for_post_request)
        r = requests.post(self._url_server, data=dict_for_post_request, headers={'Content-Type': 'application/json'})
        print(r)

        # print("Кол-во тел-ов ",(len(temp_dict['Модель'])))
        # for i in range(len(temp_dict['Модель'])):
        #     print(f"{temp_dict['Модель'][i]}, {temp_dict['Разрешение экрана'][i]}, {temp_dict['Версия ОС'][i]}")
            #print(temp_dict['Разрешение экрана'])
            #print(temp_dict['Версия ОС'])
        # Модель
        # Разрешение экрана
        # Версия ОС


    def parsing_process(self):

        # Запрос на получение данных, их запись в атрибуты класса
        self.get_request()

        # Скачивание страниц с товаром
        self.download_pages()

        # Изъятие ссылок и запись их в файл
        self.download_links()

        # Скачивание страниц товара
        self.download_unic_pages()

        # Изъятие характеристик из скачанных страниц товара
        self.extraction_data()


# xiaomi-redmi-note-11-4gb-64gb-twilight-blue-30062792
# xiaomi-redmi-note-11-4gb-64gb-star-blue-30062764
# xiaomi-redmi-9a-32gb-granite-gray-30051224
# xiaomi-redmi-9a-32gb-glacial-blue-30063682
# xiaomi-redmi-a1-32gb-black-30065370
# xiaomi-redmi-9c-nfc-3gb-64gb-green-30063443
# xiaomi-redmi-note-11s-6gb-128b-graphite-gray-30062385
# xiaomi-redmi-9a-32gb-aurora-green-30063291


# _______________________________________________________________________________________
path = 'C:\\Users\\Ingvar\\Downloads\\'
sait = 'dns'
sait_eld = 'eldorado'
sait_citi = 'citilink'
# path = 'C:\\Users\\Ingvar\\Desktop\\Documents\\WEB\\dns'
# url = "https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?order=6"
url = "https://www.dns-shop.ru/search/?q=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%D1%8B+xiaomi+poco&category=17a8a01d16404e77"
url_eld = "https://www.eldorado.ru/search/catalog.php?q=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%20xiaomi%20redmi%20note&utf"
url_citi = "https://www.citilink.ru/catalog/smartfony/?text="
url_mvideo = "https://www.mvideo.ru/product-list-page?q=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%D1%8B+xiaomi&category=smartfony-205"
url_dns_unic = "https://www.dns-shop.ru/product/3c9695dde2d5ed20/667-smartfon-poco-f4-256-gb-seryj/"

"""
with open("C:\\Users\\Ingvar\\Downloads\\eldo.html",'r', encoding='utf-8') as name_html:
    soup = BeautifulSoup(name_html, 'lxml')
    res = soup.find_all('a', role="button")
    list_last_page = list()
    for i in range(len(res)):
        temp_num = res[i].text
        if temp_num.isdigit():
            list_last_page.append(int(temp_num))
            #print(f"Атрибуты: {res[i].attrs}\n\n")
    print(f"Номер последней страницы: {max(list_last_page)}")
"""


# test_mvideo = constructor(name_website="mvideo",
#                           name_product="Смартфон",
#                           encoding="utf-8",
#                           name_tag="a",
#                           name_class="product-title__text",)

# test_mvideo.download_links()

# url_Danil = 'https://a2da-89-179-47-18.eu.ngrok.io/api/information/'
# r_full = requests.get(url_Danil)
# r = dict(r_full.json())
#
# obj = constructor(name_website=r['designer']['one']['site'],
#                   name_product=r['designer']['one']['type_product'],
#                   url_product=r['designer']['one']['url'],
#                   name_teg_last_page=r['designer']['one']['teg_name_number'],
#                   name_attribute_last_page=r['designer']['one']['role_name_url'],
#                   name_class_last_page=r['designer']['one']['class_name_number'],
#                   button_text_new_page=r['designer']['one']['name_button'])


obj = constructor(name_website="dns", name_product="Смартфон", url_product=url, name_teg_last_page="a",
                  name_attribute_last_page="class", name_class_last_page="pagination-widget__page-link",
                  button_text_new_page="Показать ещё")
obj.download_pages()

#obj.download_unic_pages()
#

# obj_citi = constructor(name_website="citilink", name_product="Смартфон", url_product=url_citi, name_teg_last_page='div',
#                         name_attribute_last_page="class", name_class_last_page="app-catalog-h5nagc ero1s990",
#                         button_text_new_page="Показать ещё")

# obj_mvideo = constructor(name_website="mvideo", name_product="Смартфон", url_product=url_mvideo, name_teg_last_page='a',
#                          name_attribute_last_page="class", name_class_last_page="page-link",
#                          button_text_new_page="Показать ещё")
# obj_mvideo.download_pages()
# obj_citi.download_pages()
#
print("download_pages - good")


# s = Service("C:\\Users\\Ingvar\\chromedriver_win32\\chromedriver.exe")
# driver = webdriver.Chrome(service=s)  # запустить браузер
# driver.implicitly_wait(1)
# driver.maximize_window()
# driver.get(url_citi)
# time.sleep(5)
# WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//button[text()="Показать ещё" and not(@disabled)]')))
#
# time.sleep(2)
# driver.find_element(By.XPATH, '//button[text()="Показать ещё" and not(@disabled)]').click()
# # driver.find_element(By.XPATH, '//button[@class="e4uhfkv0 app-catalog-1ls3bkl e4mggex0"]').click()
# # driver.find_element(By.CLASS_NAME, 'button-ui button-ui_white button-ui_icon wishlist-btn').click()
# time.sleep(5)
# driver.quit()
# page = driver.find_element(By.XPATH, "//*").get_attribute("outerHTML")
# print(type(page))


# with open("page.html", "w", encoding="utf-8") as file:
#   file.write(page)
# time.sleep(1)


"""

files = os.listdir(path + sait_citi)
count_sait = list(filter(lambda x: x.endswith('.html'), files))
print("count_sait", count_sait)
num_page_old = len(count_sait)  # кол-во скачанных страниц, из к-х нужно доставать ссылки
print(num_page_old)
# num_page_old = 75


#for i in range(0, num_page_old):
#    name = sait + str(i) + '.html'
#    obj.download_links(name_file=name, name_tag='a', name_class='catalog-product__name')

for i in range(0, num_page_old):
    name = sait_citi + str(i) + '.html'
    obj_citi.download_links(name_file=name, name_tag='a', name_class='XD')

# print(len(unic_url))
# obj.download_unic_pages()
print("download_unic_pages - good")

import Class_Timer

# if (num_page_old==163783):
t1 = Class_Timer.Timer()
# DataBase = pd.DataFrame()

t1.start()
# files = os.listdir(path + sait + '_unic')
# count_sait_unic = list(filter(lambda x: x.endswith('.html'), files))

# for i in range(0, len(count_sait_unic)):
"""
"""
for i in range(0, 1350):
    name = 'dns_unic_' + str(i) + '.html'
    with open('C:\\Users\\Ingvar\\Desktop\\Documents\\WEB\\dns_unic\\' + name, 'r', encoding="utf-8") as html_file:
        tree_phone_charact = BeautifulSoup(html_file, "lxml")
        DataBase = collections_title_value(tree_phone_charact, DataBase, "")
print("Kol-vo phone", len(DataBase.index))
DataBase.to_feather("DataBase.feather")
t1.stop()
"""
# _______________________________________________________________________________________
