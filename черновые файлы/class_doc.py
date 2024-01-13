from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
from datetime import datetime, timedelta
import os


from bs4 import BeautifulSoup
import pandas as pd
import itertools
import requests


class constructor():

    def __init__(self,
                 name_website="",
                 name_product="",
                 url_product="",
                 encoding = 'utf-8',

                 name_tag = "",
                 name_class = "",

                 name_tag_title="",
                 name_class_title="",
                 
                 name_tag_value="",
                 name_class_value="",
                 
                 name_characteristics="",

                 web_driver="C:/Users/79182/chromedriver_win32/chromedriver.exe",   # расположение chromedriver.exe
                 path_downloads='C:/Users/79182/Downloads',   # /home/igor/Загрузки/
                 name_teg_last_page="a",
                 name_attribute_last_page="class",
                 name_class_last_page="pagination-widget__page-link",
                 button_text_new_page="Показать ещё",
                 button_characteristics="Развернуть все"
                ):

               # общие сведения      
        self.name_website = name_website                    # имя сайта, с которым работаем,
        self.name_product = name_product                    # имя товара, например: телефон, пылесос
        self.url_product = url_product                      # ссылка на раздел исследуемого товара
        self.encoding = encoding                            # кодировка страницы товара
       
        self.name_tag = name_tag
        self.name_class = name_class
 
 
        # сведения по заголовку хар-ки
        self.name_tag_title = name_tag_title                      # имя тега заголовка хар-ки, по которому ищем
        self.name_class_title = name_class_title                  # имя класса, по которому ищем
 
 
       
        # сведения по зн-ю хар-ки    
        self.name_tag_value = name_tag_value                      # имя тега зн-я хар-ки, по которому ищем
        self.name_class_value = name_class_value                  # имя класса, по которому ищем
        self.name_characteristics = name_characteristics          # имя характеристики
       
        # сведения для скачивания страниц
        self.web_driver=web_driver                                # расположение chromedriver.exe
        self.path_downloads=path_downloads                        # путь до папки "Загрузки"
 
 
        self.name_teg_last_page=name_teg_last_page                # тег номера последней страницы, отображ-ся на сайте
        self.name_attribute_last_page=name_attribute_last_page    # по какому атрибуту искать номер последней страницы (class/role)
        self.name_class_last_page=name_class_last_page            # имя класса номера последней страницы, отображ-ся на сайте
        self.button_text_new_page=button_text_new_page            # текст на кнопке, которая переводит на след. страницу поиска
        self.button_characteristics=button_characteristics        # текст на кнопке, которая открывает хар-ки
       
        self._path_save_url_product = "/home/igor/PycharmProjects/HTML/test_sitilink.html"  # путь сохраненного файла html test_mvideo

        if self.url_product != "":
            self.encoding = requests.get(self.url_product).encoding
            
        if self._path_save_url_product != "":
            with open(self._path_save_url_product, 'r', encoding=self.encoding) as html_file:
                self._tree_dom_bs4 = BeautifulSoup(html_file, "lxml")
        else:
            self._tree_dom_bs4 = None  # DOM структура скачанного файла html


    def get_request(self,link):
        # 'https://a2da-89-179-47-18.eu.ngrok.io/api/information/'
        get_result = requests.get(link)
        dict_result = dict(get_result.json)
        
        # общие сведения
        self.name_website = dict_result['designer']                    # имя сайта, с которым работаем, 
        self.name_product = dict_result['designer']                    # имя товара, например: телефон, пылесос
        self.url_product = dict_result['designer']                      # ссылка на раздел исследуемого товара
        self.encoding = dict_result['designer']                            # кодировка страницы товара
        self.link_or_str = dict_result['designer']                   # что пробуем достать, ссылка или строка

        self.name_tag = dict_result['designer']
        self.name_class = dict_result['designer']

        # сведения по заголовку хар-ки
        self.name_tag_title = dict_result['designer']                 # имя тега заголовка хар-ки, по которому ищем
        self.name_class_title = dict_result['designer']             # имя класса, по которому ищем
        self.num_places_title = dict_result['designer']             # кол-во мест, в которых лежит название хар-ки
        
        # сведения по зн-ю хар-ки     
        self.name_tag_value = dict_result['designer']           # имя тега зн-я хар-ки, по которому ищем
        self.name_class_value = dict_result['designer']             # имя класса, по которому ищем
        self.num_places_value = dict_result['designer']           # кол-во мест, в которых лежит зн-е хар-ки
        self.name_characteristics = dict_result['designer']          # имя характеристики
        
        # сведения для скачивания страниц
        self.web_driver=web_driver                                # расположение chromedriver.exe
        self.path_downloads=path_downloads                        # путь до папки "Загрузки"
        self.head_url=dict_result['designer']                                    # начало ссылок на каждый телефон
        self.name_teg_last_page=dict_result['designer']                # тег номера последней страницы, отображ-ся на сайте
        self.name_attribute_last_page=dict_result['designer']    # по какому атрибуту искать номер последней страницы (class/role)
        self.name_class_last_page=dict_result['designer']     # имя класса номера последней страницы, отображ-ся на сайте
        self.button_text_new_page=dict_result['designer']         # текст на кнопке, которая переводит на след. страницу поиска
        self.button_characteristics=dict_result['designer']        # текст на кнопке, которая открывает хар-ки


    def Save_html(self, name):
        """name - имя, под которым сохранится файл"""
        time.sleep(3)
        # "Сохранить как..."
        pyautogui.keyDown('ctrl')  # hold ctrl key
        pyautogui.press('s')  # press s key
        pyautogui.keyUp('ctrl')  # release ctrl key
        # print("Not found")
        time.sleep(1)
        FILE_NAME = name  # имя, под которым сохранится HTML-файл: 'dns3.html'
        pyautogui.typewrite(FILE_NAME)  # ввести заданное имя в окно в браузере
        pyautogui.press(['tab', 'down', 'up', 'up', 'enter'])
        pyautogui.press('enter')
        # Проверяем, как только получится открыть файл, значит он сохранился, можно переходить к следующему действию
        """
        while True:
            try:
                f = open(self.path_downloads + "/" + name)
                f.close()
                break
            except:
                # print(5, end = '')
                time.sleep(.1)
        """
        wait_end_time = datetime.now() + timedelta(seconds=15)

        while datetime.now() < wait_end_time:
            try:
                f = open(self.path_downloads + "/" + name)
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
        if not os.path.isdir(self.path_downloads + '/' + self.name_website):
            os.mkdir(self.path_downloads + '/' + self.name_website)
        else:
            os.rename(self.path_downloads + '/' + self.name_website,
                      self.path_downloads + '/' + self.name_website + str(datetime.now().date()) +
                      '_' + str(datetime.now().microsecond))
            os.mkdir(self.path_downloads + '/' + self.name_website)
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
            os.replace(self.path_downloads + '/' + name,
                       self.path_downloads + '/' + self.name_website + "/" + name)
            print("pered while")
            flag_not_click = 0
            while (True):
                name = self.name_website + str(num_page_old - 1) + '.html'
                with open(self.path_downloads + '/' + self.name_website + '/' + name,
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
                        os.replace(self.path_downloads + '/' + name,
                                   self.path_downloads + '/' + self.name_website + "/" + name)
                        num_page_old = i + 1  # int(num_page_new)
                        print("num_page_old: i+1 =", num_page_old)
                    if (flag_not_click > 0): break
                else:
                    break
        except Exception as ex:
            print(ex)
            driver.quit()


    def download_unic_pages(self):
        if not os.path.isdir(self.path_downloads + '/' + self.name_website + '_unic'):
            os.mkdir(self.path_downloads + '/' + self.name_website + '_unic')
        else:
            os.rename(self.path_downloads + '/' + self.name_website + '_unic',
                      self.path_downloads + '/' + self.name_website + '_unic' + str(datetime.now().date()) +
                      '_' + str(datetime.now().microsecond))
            os.mkdir(self.path_downloads + '/' + self.name_website + '_unic')
        unic_url = list()
        with open(self.path_downloads + '/' + self.name_website + '/' + "product_links.txt", "r",
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
                    os.replace(self.path_downloads + '/' + name,
                               self.path_downloads + '/' + self.name_website + '_unic' + '/' + name)
                except Exception as ex:
                    print(ex)
                    driver.quit()


    def download_links(self, name_tag="", name_class="", type_value="href"):
        """
            Метод для вытаскивания ссылок из страниц товаров
            Для работы метода необходимо, чтобы были переданы параметры
            
            param: self 
            param: name_tag имя тега
            param: name_class имя класса
            param: type_value тип значения (по умолчанию href)
        """

        self.name_tag = name_tag
        self.name_class = name_class
        self.link_or_str = type_value # "href" 
        # поиск тегов  с определенным классом по дереву
        if self.name_tag != "" and self.name_class != "":
            Nodes = self._tree_dom_bs4.find_all(self.name_tag, class_=self.name_class)
        elif self.name_tag != "" and self.name_class == "":
            Nodes = self._tree_dom_bs4.find_all(self.name_tag)

        with open("product_links.txt", "a", encoding='utf-8') as file:
            print(len(Nodes))
            for i in range(len(Nodes)):
                #print(Nodes[i].prettify())
                if self.name_product + " " in Nodes[i].text:
                    if 'href' in Nodes[i].attrs:
                        #print(Nodes[i][self.link_or_str])
                        file.write(Nodes[i][self.link_or_str] + "\n")
            

    #def collections_title_value(tree_BS4, current_DataBase: pd.DataFrame, path: str):
    """
    def extraction_data(self, 
                        name_tag_title, 
                        name_class_title, 
                        name_title, 
                        name_tag_value, 
                        name_class_value):

        self.name_tag_title = name_tag_title
        self.name_class_title = name_class_title
        self.name_characteristics = name_title

        self.name_tag_value = name_tag_value
        self.name_class_value = name_class_value

        str_title = str()
        str_value = str()
        num = 0
        if self._tree_dom_bs4 is not None:
            Nodes_title = self._tree_dom_bs4.find_all(self.name_tag_title, class_ = self.name_class_title)
            Nodes_value = self._tree_dom_bs4.find_all(self.name_tag_value, class_ = self.name_class_value)
        else:
            return
        
        for i in range(len(Nodes_title)):
            temp_str = Nodes_title[i].text
            if self.name_characteristics in temp_str:
                str_title = str(temp_str)
                num = i
                str_value = Nodes_value[i].text
                break
        print(f"{str_title}: {str_value}")
    """    
    
    
    def extraction_data(self, 
                        name_title, 
                        name_tag_all, 
                        name_class_all):

        self.name_characteristics = name_title

        self.name_tag_value = name_tag_all
        self.name_class_value = name_class_all

        str_title = self.name_characteristics
        str_all = str()
        if self._tree_dom_bs4 is not None:
            Nodes_all = self._tree_dom_bs4.find_all(self.name_tag_value, class_ = self.name_class_value)

        else:
            return
        
        print(len(Nodes_all))
        for i in range(len(Nodes_all)):
            temp_str = Nodes_all[i].text
            if self.name_characteristics in temp_str:
                str_all = str(temp_str)
                print(f"Текстовое поле: {str_all}")
                break
        size_title = len(str_title)
        print(f"{str_title}: {str_all[size_title:]}")


    def collections_title_value(self, tree_BS4, current_DataBase: pd.DataFrame, path: str):

        names_classes = {'title': 'product-characteristics__spec-title',
                        'value': 'product-characteristics__spec-value'}
        # TR = Translator(from_lang="ru", to_lang="en")
        stringe = str()
        Nodes = tree_BS4.find_all("div", class_="product-characteristics__group") # поиск объекта с группами характеристик
        example_type = type(tree_BS4.find('div')) # для проверки типа "Tag" и наличия метода attrs
        current_columns = current_DataBase.columns # столбцы текущей БД, которую передали как параметр
        unused_names_columns = current_DataBase.columns
        #print(type(unused_names_columns))
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
                        if self.name_class_title in child['class']:  # a in b, a-строка, b-список
                            # print(child.string)
                            if child.string is None:
                                # создание среза из генератора дочерних элементов, для перехода к следующему
                                list_name_title = list(
                                    itertools.islice(Nodes[i].descendants, TITLE_None + 1, TITLE_None + 2))
                                name_title = list_name_title[0]
                                flag_title=True

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
                        elif self.name_class_value in child['class']:
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

    def parsing_process(self):
        
        # Запрашиваются данные с сервера
        
        # По первому основному правилу устанавливаются параметры и создается экземляр класса: 
        # * домен товара
        # * ссылка на 1ую страницу сайта с интересующим товаром
        # * кодировка сайта через запрос
        
        # Происходит скачивание доступных на сайте страниц с товаром
        # Результат фиксируется в предопределнной папке

        # Из первого основного правила достаются параметры для вытаскивания ссылок
        # Происходит извлечение ссылок из скачанных страниц
        # Результат фиксируется в файле в предопределенной папке

        # Происходит скачивание записанных в файл ссылок в другую предопределенную папку

        # В одну структуру собираются все правила для характеристик.
        # В цикле перебираются скачанные страницы с товаром и к каждой применяется вся сводка правил 


        pass
A = constructor(name_product="Смартфон")

A.extraction_data(name_title='Операционная система',name_tag_all='div',name_class_all='app-catalog-xc0ceg')

# Эльдорадо
# A.extraction_data(name_title='Операционная система',name_tag_all='tr',name_class_all=' grey')

# МВидео
# A.extraction_data(name_title='Операционная система',name_tag_all='div',name_class_all='item-with-dots')
 
#A.download_links(name_tag='a', name_class='catalog-product__name' )
