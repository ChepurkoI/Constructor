from sys import platform
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Для автоматической установки и указания пути к WebDriver
# from webdriver_manager.chrome import ChromeDriverManager
# https://automated-testing.info/t/python-webdriver-manager-dlya-avtomatizaczii-upravleniya-drajverami/12101

from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Для расширенного функционала по настройке proxy, заголовков, cookies и прочего
# Есть проблемы, чего-то не хватает для полного функционирования
# import seleniumwire.undetected_chromedriver as uc

# _______________________________________________________________________

# Import согласно scrapeOps
# импорт нашего веб-драйвера
# from selenium import webdriver дубликат
# импорт ActionChains
from selenium.webdriver import ActionChains
# импорт By
# from selenium.webdriver.common.by import By дубликат
# импорт ScrollOrigin
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
# импортируем возможность сна
# from time import sleep # дубликат для import time

# _______________________________________________________________________


from datetime import datetime, timedelta

import time
# from time import sleep
import pyautogui
import os
import requests
import json

import pprint

from bs4 import BeautifulSoup
# import pandas as pd
import numpy as np

class constructor_():
    def __init__(
        self,
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
                self.web_driver = "C:\\Users\\Ingvar\\PycharmProjects\\parsing_constructor\\chromedriver_win64\\chromedriver.exe"

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

    def first_start(self):
        # create a bool to know when we're running
        running = True

        # open the Chrome browser
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)

        while running:
        #navigate to the scrapeops website
            driver.get("https://scrapeops.io/")
            #wait a couple seconds
            time.sleep(2)
            #save the page's footer as a variable
            footer = driver.find_element(By.TAG_NAME, "footer")
            #scroll to the footer
            ActionChains(driver).scroll_to_element(footer).perform()
            #wait a couple more seconds
            time.sleep(2)
            #exit the loop
            running = False

            #после прокрутки мы находим все ссылки на странице
            links = driver.find_elements(By.TAG_NAME, "a")

            #перебираем все ссылки
            for link in links:
                print(link.text)

                #Найти "Получить бесплатный аккаунт"
                if link.text == "Get Free Account":

                    #сохраняем эту ссылку в качестве цели
                    target = link

                    #прервать цикл
                    break

            #прокрутка до нужной нам ссылки
            ActionChains(driver)\
                .scroll_to_element(target)\
                .perform()
            time.sleep(2)
            target.click()
            
            #выход из цикла
            running = False

        #закрыть браузер
        driver.quit()

    def Example_with_wait(self):
        #Открываем Chrome
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)
        
        #навигация по сайту
        driver.get("https://www.drom.ru/") # 
        
        #id-селектор для кнопки меню
        selector = "body > div:nth-child(3) > div.css-1s4zmmw.exbslet0 > div > div.css-1x129lu.e79n5oy0 > div" #"#global-nav-mobile-trigger"
        
        #создаем объект ActionChains
        actions = ActionChains(driver)
        
        #Ждем появления кнопки меню
        open_menu = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, selector))
        )

        #выполняем цепочку действий
        actions\
            .move_to_element(open_menu)\
            .click()\
            .perform()
        
        #id селектор для отображаемого меню
        menu_selector = "body > div:nth-child(3) > div.css-1s4zmmw.exbslet0 > div > div.css-1x129lu.e79n5oy0 > div > div.css-1xrw13i.e700zrq0" #"#global-nav-mobile"
        
        #Ждем, пока появится меню
        menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, menu_selector
            ))
        )
        
        # выводим содержимое меню
        print(menu.text)
        
        # закрываем браузер
        driver.quit()

    def Example_without_wait(self):
        
        #Открываем Chrome
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)
        
        #навигация по сайту
        driver.get("https://www.drom.ru/") # 
        
        #id-селектор для кнопки меню
        selector = "body > div:nth-child(3) > div.css-1s4zmmw.exbslet0 > div > div.css-1x129lu.e79n5oy0 > div" #"#global-nav-mobile-trigger"
        
        #создаем объект ActionChains
        actions = ActionChains(driver)
        
        #Ждем появления кнопки меню
        print("Не ждем появления кнопки меню")
        open_menu = driver.find_element(By.CSS_SELECTOR, selector)
        
        
        #выполняем цепочку действий
        actions\
            .move_to_element(open_menu)\
            .click()\
            .perform()
        
        #id селектор для отображаемого меню
        menu_selector = "body > div:nth-child(3) > div.css-1s4zmmw.exbslet0 > div > div.css-1x129lu.e79n5oy0 > div > div.css-1xrw13i.e700zrq0" #"#global-nav-mobile"
        
        #Ждем, пока появится меню
        print("Не ждем появления меню")
        menu = driver.find_element(By.CSS_SELECTOR, menu_selector)
        
        # выводим содержимое меню
        print(menu.text)
        
        # закрываем браузер
        driver.quit()
    
    def Example_work_seleniumwire(self):
        """
        
        """
        # email = "some_address@emailprovider.com"
        # API_KEY = "my_super_special_api_key"

        # # форматированная строка, которая вставляет наш email и API_KEY в url прокси-сервера.
        # proxy_url = f"http://{email}.headless_browser_mode=true:{API_KEY}@proxy.scrapeops.io:5353"

        # # альтернатива объекту Options
        # chrome_options = uc.ChromeOptions() 
        # chrome_options.headless=False #  чтобы видеть работу внутри браузера

        # proxy_options = {
        #     "proxy": {
        #         "http" : proxy_url,
        #         "https" : proxy_url,
        #         "no_proxy" : "127.0.0.1"
        #     }
        # }
        
        # # создаем объект undetected_chromedriver. Это альтернативный драйвер по сравнению с chromedriver
        # driver = uc.Chrome(options=chrome_options, seleniumwire_options=proxy_options)

        # driver.get("http://quotes.toscrape.com/")
        # time.sleep(10)

        # driver.quit()

    def wait_until_an_element_is_present(self):
        """
        Пример не рабочий, так как на сайте ESPN изменили конфигурацию 
        и меню в виде бургера есть только в мобильной версии сайта.

        В этом разделе мы будем ждать, пока элемент не появится, а затем найдем его. 
        В примере ниже мы находим на экране кнопку меню, а затем щелкаем по ней.
        """

        #open Chrome
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)
        driver.implicitly_wait
        #navigate to the site
        driver.get("https://espn.com")

        #id selector for the menu button
        selector = "#global-nav-mobile-trigger"

        #create an ActionChains object
        actions = ActionChains(driver)

        #wait until the menu button appears
        open_menu = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, selector))
        )

        #perform a chain of actions
        actions\
            .move_to_element(open_menu)\
            .click()\
            .perform()

        #close the browser
        driver.quit()

    def wait_until_an_element_is_visible(self):
        """
        Пример не рабочий, так как на сайте ESPN изменили конфигурацию 
        и меню в виде бургера есть только в мобильной версии сайта.

        Этот код основан на предыдущем примере wait_until_an_element_is_present 
        и позволяет найти меню после того, как мы щелкнули на нем и оно стало видимым.
        """

        # open Chrome
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)
        
        #переход на сайт
        driver.get("https://espn.com")
        
        #id селектор для кнопки меню
        selector = "#global-nav-mobile-trigger"
        
        #создаем объект ActionChains
        actions = ActionChains(driver)
        
        #дождитесь появления кнопки меню
        open_menu = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, selector))
        )
        
        #выполнить цепочку действий
        actions\
            .move_to_element(open_menu)\
            .click()\
            .perform()
        
        #id селектор для появляющегося меню
        menu_selector = "#global-nav-mobile"
        
        #дождитесь появления меню
        menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, menu_selector
            ))
        )
        
        #вывести содержимое меню
        print(menu.text)
        
        #закрыть браузер
        driver.quit()

    def XPath_variability(self):
        """
       
        """
        #откройте экран Chrome
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)
        
        #переход на веб-страницу
        driver.get("https://quotes.toscrape.com")
        
        #найти элемент h1
        h1 = driver.find_element(By.XPATH, "//h1")
        print(f"h1: {h1.text}\n\n")
        
        #найти первый элемент в body
        first_element = driver.find_element(By.XPATH, "/html/body[1]")
        print(f"Первый элемент: {first_element.text}\n\n")
        
        #найти все элементы class "quote" 
        all_quotes = driver.find_elements(By.XPATH, "//*[@class='quote']")
        print("Все цитаты:")
        for quote in all_quotes:
            print(quote.text)
        
        #найти все элементы, содержащие слово "by"
        authors = driver.find_elements(By.XPATH, "//*[contains(text(), 'by')]")
        print("\n\nАвторы:")
        for author in authors:
            print(author.text)
        
        #задав диапазон чисел, находим все теги, восходящие к цитате Эйнштейна
        tag_string = "/html/body/div/div[2]/div[1]/div[1]/div/a"
        print(f"\n\nТеги Эйнштейна:")
        for tagnumber in range(1,5):
            tag = driver.find_element(By.XPATH, f"{tag_string}[{tagnumber}]")
            print(tag.text)
        
        #найти элементы, происходящие от "//html/body/div/div[2]"
        all_div_2_stuff = driver.find_element(By.XPATH, "//html/body/div/div[2]")
        print("\n\nВсе div[2] вещи:")
        print(all_div_2_stuff.text)
        
        #найти ссылку для входа в систему
        login = driver.find_element(By.XPATH, "//*[@href='/login']")
        
        #щелкните по этой ссылке, чтобы перейти на страницу входа в систему
        login.click()
        
        #найдите поле ввода с идентификатором 'username' и сохраните его как переменную
        username = driver.find_element(By.XPATH, "//input[@id='username']")
        
        #найдите поле ввода с идентификатором 'password' и сохраните его как переменную
        password = driver.find_element(By.XPATH, "//input[@id='password']")
        
        #ввод имени пользователя
        username.send_keys("new_user")
        
        #ввод пароля
        password.send_keys("mysupersecretpassword")
        
        #спит в течение 3 секунд, чтобы вы могли видеть, как заполняются поля ввода
        time.sleep(3)
        
        #найдите элемент, следующий за 'username', и выведите его местоположение
        element_after_body = driver.find_element(By.XPATH, "//following-sibling::input[@id='username']")
        print(f'\n\n{element_after_body.location}\n\n')
        
        #найдите элемент, предшествующий имени пользователя, и выведите его местоположение
        element_before_username = driver.find_element(By.XPATH, "//preceding-sibling::input[@id='username']")
        print("Элемент перед телом")
        print(element_before_username.location)
        
        #закрыть браузер
        driver.quit()

    def Cookies_solver_Implicit_Waits(self):

        #open Chrome
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)
        #set implicit wait
        driver.implicitly_wait(10)

        #navigate to the url
        driver.get("https://www.hubspot.com")

        #find the "accept" button
        modal = driver.find_element(By.ID, "hs-eu-confirmation-button")

        #click the button
        modal.click()

        #pause so we can see whats happening
        time.sleep(2)
        driver.quit()

    def Cookies_solver_Explicit_Waits(self):
        #open Chrome
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)

        #navigate to the url
        driver.get("https://www.hubspot.com")
        
        #find the "accept" button
        modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "hs-eu-confirmation-button")))
        
        #click the button
        modal.click()
        
        #pause so we can see whats happening
        time.sleep(2)
        
        driver.quit()

    def Scroll_with_keys(self):
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)


        driver.get('https://books.toscrape.com/')
        driver.maximize_window()

        body = driver.find_element(By.TAG_NAME, 'body')  
        body.send_keys(Keys.PAGE_DOWN)  # Scroll down
        time.sleep(5)

        body.send_keys(Keys.PAGE_UP)    # Scroll up
        time.sleep(5)

        driver.quit()

    def smooth_scroll(self):
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)

        # Переход на веб-страницу с бесконечной прокруткой
        driver.get('https://www.shipspotting.com/')
        
        # Получение элемента body для выполнения действий
        driver.find_element(By.TAG_NAME, 'body')

        # Определите количество прокруток (настройте по необходимости)
        scroll_iterations = 5
        for _ in range(scroll_iterations):

            # Прокрутка вниз с помощью клавиши END для запуска бесконечной прокрутки
            ActionChains(driver).send_keys(Keys.END).perform()
            
            # Подождите некоторое время, чтобы контент успел загрузиться
            time.sleep(5)

        # Захват и печать содержимого после прокрутки
        captured_images = driver.find_elements(By.TAG_NAME, 'img')
        for image in captured_images:
            print(image.get_attribute('src'))

        # Закрыть окно браузера
        driver.quit()

    def use_stealth(self):
        PROXY = '50.228.83.226:80'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s, options=chrome_options)
        
        stealth(driver,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36",
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        
        driver.get("https://yandex.ru/internet")
        driver.maximize_window()
        time.sleep(15)
        driver.quit()
ScrapeOps = constructor_()


# ScrapeOps.Example_without_wait() # Работают одинаково на примере Дрома
# ScrapeOps.Example_with_wait() # Как первый так и второй загружают и выводят текст меню "Ещё"

# ________________________________________________________________________________________________________________________________________________
# ________________________________________________________________________________________________________________________________________________
# ________________________________________________________________________________________________________________________________________________
# ________________________________________________________________________________________________________________________________________________

s = Service("C:\\Users\\Ingvar\\PycharmProjects\\parsing_constructor\\chromedriver_win64\\chromedriver.exe")
driver = webdriver.Chrome(service=s)  # запустить браузер

stealth(driver,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36",
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
driver.maximize_window()
driver.get("file:///C:/Users/Ingvar/Downloads/one_car.html")
time.sleep(3)

# Выкладываю данные про кнопки с общего массива данных
buttons = [{'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'ПТС'},
           {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'о регистрации'},
           {'teg_name': 'button', 'class_name': 'ezmft1z0 css-xst070 e104a11t0', 'button_text': 'фото'},
           {'teg_name': 'button', 'class_name': 'css-18zgczx e3cb8x01', 'button_text': 'контакты'}] 

try: # для каждой страницы нажимаем группу кнопок (массив словарей с данными)
    for button_data in buttons: # идем по списку кнопок
        try: # пробуем поочередно нажать на кнопки
            print(f"Кнопка: {button_data}")
            time.sleep(2)
            Xpath_button = '//' + button_data["teg_name"] + '[@class="'+ button_data["class_name"] + '" and not(@disabled)]'
            #Xpath_button_with_text = '//'+ button_data['teg_name'] + '[text()="' + button_data["button_text"] + '" and not(@disabled)]'
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Xpath_button)))
            time.sleep(2)
            candidates_buttons = driver.find_elements(By.XPATH, Xpath_button)
            for i in range(len(candidates_buttons)):
                if button_data["button_text"] in candidates_buttons[i].text:
                    candidates_buttons[i].click
                    print(f"Нажата клавиша {candidates_buttons[i].text}")
                    print("\n\n")
        
        except: # если не получилось нажать на кнопку
            continue
        
except:
    print("Not click Не получилось нажать кнопку развертывания характеристик или фото")
    # continue