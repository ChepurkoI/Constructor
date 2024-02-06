import time

import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
from tabulate import tabulate
import collections
from urllib3.util import SKIP_HEADER

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class Proxy():

    def __init__(self):
        r = requests.get("https://www.ipaddress.com/proxy-list/")
        request_content = html.fromstring(r.content)

def parsing_tables(tables):
    """
    Фукнция, которая забирает значения из таблиц, которые были найдены и переданы в виде параметра tables

    table: структура bs4, в которой уже найдены таблицы
    return: спискок таблиц
    """

    list_tables = []
    for iterator_table in range(len(tables)):
            table = []
            for row in tables[iterator_table].find_all('tr'):
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                if cols:
                    table.append([cols[0] , cols[1]]) # Собираю данные по парам 
            list_tables.append(table)
    
    return list_tables

def primer_table():
    
    table_metrics = {"Класс": ['CD (нарушение проводимости)','HYP (гипертрофия)','MI (Ишемические нарушения)','NORM (нормальная ЭКГ)','STTC (изменения ST/T)'],
                 "precision": [0.69782, 0.62766, 0.71498, 0.80851, 0.67354],
                 "recall": [0.60705, 0.40972, 0.60163, 0.93333, 0.68531],
                 "f1-score": [0.64928, 0.49580, 0.65342, 0.86645, 0.67938],
                 "support": [269, 144, 246, 855, 286]
                 }
    print(tabulate(table_metrics, headers="keys",tablefmt='psql', stralign='right', numalign="center"))
    

def create_nice_table(table, name_table):
    """
        Функция для вывода заголовков на экран в наглядном виде.
        На вход подаются данные: таблица, ее название, названия столбцов

        table: DataFrame, в котором сохранены заголовки различных конфигураций заголовков
        name_table: str, имя таблицы
                
    """
    names_columns = table.keys().tolist() # Извлекаем названия столбцов
    nice_table = {str(name_table): table.index.tolist()} # формируем первый столбец таблицы, в котором указаны названия строк
    
    for name_column in names_columns: # Добавляем по одной колонке к таблице
        nice_table[str(name_column)] = table[name_column].values.tolist()
    
    print(tabulate(nice_table, headers="keys",tablefmt='psql', stralign='right', numalign="center"))


def humanisation_check(url="https://bot.sannysoft.com/"):
    """
    В три захода извлекаются данные из сайта проверки.
    1) С сохраненного файла извлекаются результаты анализа сайтом при обычном посещении сайта
    2) Делается обычный запрос без изменений и извлекаются результаты анализа, который сделал сайт
    3) Меняются заголовки запроса и отправляется скорректированный запрос

    После извлечения собираются в DataFrame для сравнения и корректировки заголовков
    """
    
    
    print("START")
    
    # Сайт, который проверяет всеми способами посетителей на наличие WebDriver, неправильных заголовков и выдает статистику
    url = "https://bot.sannysoft.com/" 

    # Загружаю html документ, в котором собраны данные при обычном посещении сайта
    with open("C:\\Users\\Ingvar\\PycharmProjects\\Aggregator\\Info_my_PC.txt",'r',encoding="utf-8") as html_file:
        DOM_My_PC = BeautifulSoup(html_file, "lxml")
        
        all_table = DOM_My_PC.find_all('table')    # Ищем все таблицы, которые есть в документе
        my_PC = parsing_tables(tables=all_table)   # Собираем все таблицы в одном месте

    # Формируем DataFrame с извлеченными данными для дальнейшей конкатенации с другими вариациями запроса
    table_1 = pd.DataFrame(my_PC[0], columns=['Name_Test', 'my_PC_info'])
    table_1 = table_1.set_index('Name_Test')

    table_2 = pd.DataFrame(my_PC[1], columns=['Fingerprint_Scanner', 'my_PC_info'])
    table_2 = table_2.set_index('Fingerprint_Scanner')

    table_3 = pd.DataFrame(my_PC[2], columns=['Some_details', 'my_PC_info'])
    table_3 = table_3.set_index('Some_details')


    # Работа requests без вмешательства в заголовки
    r_default = requests.get(url)
    
    if r_default.status_code == 200:
        #print(r_default.request.headers, "\n") # Заголовки, которые отправлены браузеру
        DOM = BeautifulSoup(r_default.text, "lxml")
        tables_for_request = DOM.find_all('table')
        request_info_table = parsing_tables(tables=tables_for_request)


        df_request_info_table_1 = pd.DataFrame(request_info_table[0], columns=['Name_Test', 'Request_info'])
        df_request_info_table_1 = df_request_info_table_1.set_index('Name_Test')
        
        df_request_info_table_2 = pd.DataFrame(request_info_table[1], columns=['Fingerprint_Scanner', 'Request_info'])
        df_request_info_table_2 = df_request_info_table_2.set_index('Fingerprint_Scanner')

        df_request_info_table_3 = pd.DataFrame(request_info_table[2], columns=['Some_details', 'Request_info'])
        df_request_info_table_3 = df_request_info_table_3.set_index('Some_details')

        # df_request_info_table = df_request_info_table.set_index('Name_Test')
        #print(df_request_info_table["Request_info"])
        table_1 = pd.concat([table_1, df_request_info_table_1],axis=1)
        # print(f"\n\n\t1:\n\n{table_1}")
        
        table_2 = pd.concat([table_2, df_request_info_table_2],axis=1)
        # print(f"\n\n\t2:\n\n{table_2}")

        table_3 = pd.concat([table_3, df_request_info_table_3],axis=1)
        # print(f"\n\n\t3:\n\n{table_3}")

    else:
        print(r_default.status_code)



    # Работа requests при добавлении заголовков
    with requests.Session() as session:
        my_headers = collections.OrderedDict([("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"),
                    ("Accept-Language", "en-us,en;q=0.5"),
                    ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36")])

        headers_for_SANNYSOFT = collections.OrderedDict({
                    'Accept': SKIP_HEADER,
                    'Accept-Encoding':SKIP_HEADER,
                    'Accept-Language':SKIP_HEADER,
                    'Cache-Control':SKIP_HEADER,
                    'Cookie':SKIP_HEADER,
                    'Downlink':SKIP_HEADER,
                    'Ect':SKIP_HEADER,
                    'Pragma':SKIP_HEADER,
                    'Rtt':SKIP_HEADER,
                    'Sec-Ch-Ua':SKIP_HEADER,
                    'Sec-Ch-Ua-Mobile':SKIP_HEADER,
                    'Sec-Ch-Ua-Platform':SKIP_HEADER,
                    'Sec-Fetch-Dest':SKIP_HEADER,
                    'Sec-Fetch-Mode':SKIP_HEADER,
                    'Sec-Fetch-Site':SKIP_HEADER,
                    'Sec-Fetch-User':SKIP_HEADER,
                    'Upgrade-Insecure-Requests':SKIP_HEADER,
                    'User-Agent': SKIP_HEADER
        })

        headers_for_SANNYSOFT.update(collections.OrderedDict([
                    ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
                    ('Accept-Encoding','gzip, deflate, br'),
                    ('Accept-Language','ru,en;q=0.9'),
                    ('Cache-Control','no-cache'),
                    ('Cookie','_ym_uid=1706461737721473179; _ym_d=1706461737; _ym_isad=2'),
                    ('Downlink','10'),
                    ('Ect','4g'),
                    ('Pragma','no-cache'),
                    ('Rtt','50'),
                    ('Sec-Ch-Ua','"Chromium";v="118", "YaBrowser";v="23.11", "Not=A?Brand";v="99", "Yowser";v="2.5"'),
                    ('Sec-Ch-Ua-Mobile','?0'),
                    ('Sec-Ch-Ua-Platform','"Windows"'),
                    ('Sec-Fetch-Dest','document'),
                    ('Sec-Fetch-Mode','navigate'),
                    ('Sec-Fetch-Site','none'),
                    ('Sec-Fetch-User','?1'),
                    ('Upgrade-Insecure-Requests','1'),
                    ('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36')
        ]))
        
        session.headers = {}
        # session.headers.update(headers_for_SANNYSOFT)
        # session.auth = ('user', 'pass')
        r_with_headers = session.get(url, headers=headers_for_SANNYSOFT)
        if r_with_headers.status_code == 200:
            print(f"Cookies: {r_with_headers.cookies}")
            print(f"Скорректированые заголовки, отправленные при запросе{r_with_headers.request.headers}") # Заголовки, которые отправлены браузеру
            DOM = BeautifulSoup(r_with_headers.text, "lxml")
            tables_for_request = DOM.find_all('table')
            request_info_table = parsing_tables(tables=tables_for_request)
            df_request_info_table_1 = pd.DataFrame(request_info_table[0], columns=['Name_Test', 'Request_with_headers_info'])
            df_request_info_table_1 = df_request_info_table_1.set_index('Name_Test')
            
            df_request_info_table_2 = pd.DataFrame(request_info_table[1], columns=['Fingerprint_Scanner', 'Request_with_headers_info'])
            df_request_info_table_2 = df_request_info_table_2.set_index('Fingerprint_Scanner')

            df_request_info_table_3 = pd.DataFrame(request_info_table[2], columns=['Some_details', 'Request_with_headers_info'])
            df_request_info_table_3 = df_request_info_table_3.set_index('Some_details')

            # df_request_info_table = df_request_info_table.set_index('Name_Test')
            #print(df_request_info_table["Request_info"])
            table_1 = pd.concat([table_1, df_request_info_table_1],axis=1)
            # print(f"\n\n\t1:\n\n{table_1}")
            
            table_2 = pd.concat([table_2, df_request_info_table_2],axis=1)
            # print(f"\n\n\t2:\n\n{table_2}")

            table_3 = pd.concat([table_3, df_request_info_table_3],axis=1)
            # print(f"\n\n\t3:\n\n{table_3}")

        else:
            print(r_with_headers.status_code)
    
    create_nice_table(table=table_1, name_table="Таблица 1")
    create_nice_table(table=table_2, name_table="Таблица 2")
    create_nice_table(table=table_3, name_table="Таблица 3")
    print("FINISH")


def func_check_cloudfare_Selenium():
    s = Service("C:\\Users\\Ingvar\\PycharmProjects\\Aggregator\\parsing_constructor\\chromedriver_win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    # навигация по сайту
    driver.get()
    time.sleep(5)
    actions = ActionChains(driver)
    try:
        time.sleep(5)
        cloudfare = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, "#challenge-stage > div > label > input[type=checkbox]"))
        print("cloudfare элемент найден")
        #выполняем цепочку действий
        actions\
            .move_to_element(cloudfare)\
            .click()\
            .perform()
        time.sleep(5)
    except:
        print("Что-то пошло не так")

    finally:
        time.sleep(3)
        driver.quit()
        print("Завершено")


def delete_this_example():
        web_driver = "C:\\Users\\Ingvar\\PycharmProjects\\parsing_constructor\\chromedriver_win64\\chromedriver.exe"
        s = Service(web_driver)
        driver = webdriver.Chrome(service=s)
        
        #навигация по сайту

        driver.get("https://auto.drom.ru/lada/2110/") # 
        time.sleep(12)
        driver.quit()

def check_working_FREE_proxy():
    with requests.Session() as session:
        list_proxy = ['51.79.229.202:3128',
                        '47.89.184.18:3128',
                        '125.94.219.96:9091',
                        '183.100.14.134:8000',
                        '122.116.150.2:9000',
                        '187.1.57.206:20183',
                        '85.26.146.169:80',
                        '195.23.57.78:80',
                        '213.33.2.28:80',
                        '203.243.63.16:80',
                        '8.219.97.248:80',
                        '41.230.216.70:80',
                        '103.130.130.179:8080',
                        '50.228.83.226:80',
                        '209.126.119.176:80',
                        '51.15.242.202:8888',
                        '183.230.162.122:9091',
                        '51.75.122.80:80',
                        '36.6.145.95:8089',
                        '103.152.112.145:80',
                        '185.118.153.110:8080',
                        '12.186.205.120:80',
                        '58.246.58.150:9002',
                        '60.210.40.190:9091',
                        '121.128.194.154:80',
                        '114.156.77.107:8080',
                        '154.85.58.149:80',
                        '117.160.250.163:81',
                        '103.165.126.66:8080',
                        '47.74.152.29:8888',
                        '116.203.28.43:80',
                        '164.132.170.100:80',
                        '50.218.57.67:80',
                        '103.49.202.252:80',
                        '24.52.33.75:8080',
                        '159.203.3.234:80',
                        '50.221.166.2:80',
                        '158.255.212.55:10434',
                        '20.223.202.65:80',
                        '152.32.68.171:65535',
                        '196.203.83.249:9090',
                        '68.185.57.66:80',
                        '188.166.56.246:80',
                        '123.138.214.150:9002',
                        '51.159.159.73:80',
                        '68.188.59.198:80',
                        '50.171.32.226:80',
                        '183.215.23.242:9091',
                        '222.124.202.144:8080',
                        '50.218.57.70:80'
                    ]
        count = 0
        for current_proxy in list_proxy:
            count += 1
            print(f"{count}) Прокси: {current_proxy}",end=" ")
            proxies = {
                'http': current_proxy,
                'https': current_proxy
            }
            try:
                url_yandex = "https://yandex.ru/internet"
                url_simple = "http://ident.me/"
                IP_selector = {"http://ident.me/": "body", "https://yandex.ru/internet": "#mount > div.layout > div.layout__top-wrapper > div.layout__top > section:nth-child(1) > ul > li:nth-child(1) > div:nth-child(2)"}
                
                response = session.get(url_simple, proxies=proxies, timeout=(3,7))
                print(" - работает") # 158.255.212.55:10434
                print(f"Статус ответа: {response.status_code}\n")
                site_html = BeautifulSoup(response.text, 'lxml')
                result = site_html.select(IP_selector['http://ident.me/'])
                print(f"{result}\n\n")
            except:
                print(" - не работает")
                continue

url_with_check_cloudfare = "https://digitology.tech/docs/requests/user/advanced.html" # На этом сайте используется проверка Cloudfare перед доступом к данным
url_proxy = "https://www.ipaddress.com/proxy-list/"
url = "https://bot.sannysoft.com/"



# сброс заголовков по умолчанию
# headers = collections.OrderedDict({
# "Host": SKIP_HEADER,
# "User-Agent": SKIP_HEADER,
# "Accept-Encoding": SKIP_HEADER,
# "Accept": None,
# "Connection": None
# })
test_requests = False
if test_requests:
    with requests.Session() as session:

        headers_for_DROM = collections.OrderedDict({   
        "Accept":SKIP_HEADER,
        "Accept-Encoding":SKIP_HEADER,
        "Accept-Language": SKIP_HEADER,
        "Cache-Control": SKIP_HEADER,
        'Connection':SKIP_HEADER,
        "Cookie": SKIP_HEADER,
        'Host':SKIP_HEADER,
        "Pragma":SKIP_HEADER,
        "Referer":SKIP_HEADER,
        'Sec-Ch-Ua':SKIP_HEADER,
        "Sec-Ch-Ua-Mobile":SKIP_HEADER,
        'Sec-Ch-Ua-Platform':SKIP_HEADER,
        'Sec-Fetch-Dest':SKIP_HEADER,
        'Sec-Fetch-Mode':SKIP_HEADER,
        "Sec-Fetch-Site":SKIP_HEADER,
        "Sec-Fetch-User":SKIP_HEADER,
        "Upgrade-Insecure-Requests":SKIP_HEADER,
        "User-Agent":SKIP_HEADER})

        headers_for_DROM.update = collections.OrderedDict({
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'ru,en;q=0.9',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Cookie':'ring=97b583aj4FiBeoFzWcZCAFYJAY6DA0ad; cookie_cityid=1; cookie_regionid=77; _ga=GA1.1.687903372.1706174070; _ym_uid=1706174071106200016; _ym_d=1706174071; my_geo=77; segSession=IjAxY2EzMTYzZDlkMTcyMjFkZDllZDUzMjEzYzZmN2Njbm90QXV0aDk3YjU4M2FqNEZpQmVvRnpXY1pDQUZZSkFZNkRBMGFkIl9mZDBjMDBkMmFjODYzZTIyNjcyYzQ1ZjUwYjJiNDgyZQ; _ym_isad=2; dr_df=1; ndyr=1706788830; drom_search_web=2; _ga_1G91VLKB2K=GS1.1.1706788717.7.1.1706788835.36.0.0',
            'Host':'auto.drom.ru',
            'Pragma':'no-cache',
            'Referer':'https://auto.drom.ru/lada/',
            'Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36' })
        
        MVideo_headers = collections.OrderedDict(
            {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'ru,en;q=0.9',
                'Cache-Control':'no-cache',
                'Cookie':'MVID_FILTER_CODES=true; MVID_FLOCKTORY_ON=true; MVID_NEW_LK_OTP_TIMER=true; MVID_SERVICE_AVLB=true; MVID_TIMEZONE_OFFSET=3; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; mindboxDeviceUUID=b1ff883e-3610-4170-a060-cba08604b23f; directCrm-session=%7B%22deviceGuid%22%3A%22b1ff883e-3610-4170-a060-cba08604b23f%22%7D; _ym_uid=1703663846815879955; _ym_d=1703663846; _ga=GA1.1.556226783.1703663846; tmr_lvid=6116ebdcf8d7c82ca169f34b63a83b60; tmr_lvidTS=1703663849414; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=e2e92416-dfda-4faa-bc95-611d325eb535; uxs_uid=958ca2f0-a48d-11ee-979e-3f4fcf782be7; flocktory-uuid=5bc7c461-c287-4cd0-a8a0-60b71fe9a00a-3; afUserId=6e955af6-5640-4412-b5ae-bc6ca73ae399-p; adrcid=Aw8g1yGYe0-8aA5GONmNFGg; adid=170366385066589; _gpVisits={"isFirstVisitDomain":true,"idContainer":"100025D5"}; MVID_CITY_ID=CityCZ_2128; MVID_GEOLOCATION_NEEDED=false; MVID_REGION_ID=11; MVID_REGION_SHOP=S911; MVID_KLADR_ID=2300000100000; MVID_GUEST_ID=23376458899; wurfl_device_id=generic_web_browser; searchType2=1; MVID_NEW_OLD=eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9; MVID_OLD_NEW=eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==; deviceType=desktop; utm_term=%D0%BC%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%20%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80; MVID_COMPARE_LIST=400227948/30059681/400081515; __lhash_=4000d40d6c2a9434e1f53e91c15c3f26; MVID_AB_PERSONAL_RECOMMENDS=true; MVID_AB_UPSALE=true; MVID_ACCESSORIES_PDP_BY_RANK=true; MVID_ALFA_PODELI_NEW=true; MVID_CASCADE_CMN=true; MVID_CREDIT_DIGITAL=true; MVID_CREDIT_SERVICES=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_DISPLAY_ACCRUED_BR=true; MVID_EMPLOYEE_DISCOUNT=true; MVID_FILTER_TOOLTIP=1; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_LAYOUT_TYPE=1; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PODELI_PDP=true; MVID_PROMO_PAGES_ON_2=true; MVID_SERVICES=111; MVID_SINGLE_CHECKOUT=true; MVID_SP=true; __SourceTracker=yandex.ru__organic; admitad_deduplication_cookie=yandex.ru__organic; advcake_track_id=280d228d-079d-86f7-99ed-0b65d7782e16; advcake_session_id=6f732fbc-0d8f-db95-cd80-025d78ec8617; AF_SYNC=1706616246742; MVID_VIEWED_PRODUCTS=; MVID_CALC_BONUS_RUBLES_PROFIT=false; NEED_REQUIRE_APPLY_DISCOUNT=true; MVID_CART_MULTI_DELETE=false; MVID_YANDEX_WIDGET=true; MVID_CHECKOUT_REGISTRATION_AB_TEST=2; PROMOLISTING_WITHOUT_STOCK_AB_TEST=2; MVID_GET_LOCATION_BY_DADATA=DaData; PRESELECT_COURIER_DELIVERY_FOR_KBT=true; HINTS_FIO_COOKIE_NAME=2; COMPARISON_INDICATOR=false; CACHE_INDICATOR=false; MVID_GTM_ENABLED=011; _ym_isad=2; __hash_=f49d39daa0863201176e2ba7d31c4dd2; MVID_CHAT_VERSION=6.6.0; MVID_ENVCLOUD=prod2; _sp_ses.d61c=*; _ym_visorc=w; SMSError=; authError=; _gp100025D5={"hits":2,"vc":1,"ac":1,"a6":1}; _ga_CFMZTSS5FM=GS1.1.1706783885.10.1.1706783893.0.0.0; _ga_BNX5WPP3YK=GS1.1.1706783885.10.1.1706783893.52.0.0; tmr_detect=0%7C1706783893677; gsscgib-w-mvideo=xyUUK+bzhPIAp06L1Womu6yEBEaHADBo5hDtgQn0ld10/Nf5s5LaQ+cp6zsss5hOzizjdRL+0aPeWbOnu2ObMXZk8j42Y5a3l7udTjRY1Tx7Kd/DrvpA0tTfRpRwiB/Sb0rQU7AcW8TGIA26ow3R4msLIN5lD5icbs/gJ7mraKv+bAEUngDTeeNP+DO+wVvW4mNmg1GyzOJr4XC8rpDefrMJQkHVK4yP0qYO9ZIiD3xg1ZJBJhATcAzz4o8XIw==; cfidsgib-w-mvideo=XbPZz5t5ChZN7c0gKQ78kYUy0RnffjFxz4QFLrGwRoqZL/55Wi7kQkv6I82KBnWK/d7Wq+JlZNHyjWWytz1NUo4OqgDiFuDVLesWKow3HhRWlNxnDOX4QV0CwkEb51d5MA6yNzLnOKpLTC1hAsVdy6AvSSPFXx+rKv67QoI=; gsscgib-w-mvideo=xyUUK+bzhPIAp06L1Womu6yEBEaHADBo5hDtgQn0ld10/Nf5s5LaQ+cp6zsss5hOzizjdRL+0aPeWbOnu2ObMXZk8j42Y5a3l7udTjRY1Tx7Kd/DrvpA0tTfRpRwiB/Sb0rQU7AcW8TGIA26ow3R4msLIN5lD5icbs/gJ7mraKv+bAEUngDTeeNP+DO+wVvW4mNmg1GyzOJr4XC8rpDefrMJQkHVK4yP0qYO9ZIiD3xg1ZJBJhATcAzz4o8XIw==; gsscgib-w-mvideo=xyUUK+bzhPIAp06L1Womu6yEBEaHADBo5hDtgQn0ld10/Nf5s5LaQ+cp6zsss5hOzizjdRL+0aPeWbOnu2ObMXZk8j42Y5a3l7udTjRY1Tx7Kd/DrvpA0tTfRpRwiB/Sb0rQU7AcW8TGIA26ow3R4msLIN5lD5icbs/gJ7mraKv+bAEUngDTeeNP+DO+wVvW4mNmg1GyzOJr4XC8rpDefrMJQkHVK4yP0qYO9ZIiD3xg1ZJBJhATcAzz4o8XIw==; _sp_id.d61c=2b683eaa-ea80-4551-a1d0-1a27a7441a70.1703663846.8.1706784136.1706715980.fcf8f34c-c58d-40c3-8a63-3a318e6a472c.729a081d-e288-4530-ab4e-762c8aba3349.ec5f7213-626d-4011-ba1b-cf9f5c7a5961.1706783885449.28; fgsscgib-w-mvideo=JwUE8b1bccc9f781ea03433e6257ec6b78dddc90; fgsscgib-w-mvideo=JwUE8b1bccc9f781ea03433e6257ec6b78dddc90',
                'Pragma':'no-cache',
                'Referer':'https://www.yandex.ru/',
                'Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
                'Sec-Ch-Ua-Mobile':'?0',
                'Sec-Ch-Ua-Platform':'"Windows"',
                'Sec-Fetch-Dest':'document',
                'Sec-Fetch-Mode':'navigate',
                'Sec-Fetch-Site':'same-origin',
                'Sec-Fetch-User':'?1',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
            })
        
        DNS_headers = collections.OrderedDict([
                        ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
                        ('Accept-Encoding','gzip, deflate, br'),
                        ('Accept-Language','ru,en;q=0.9'),
                        ('Cache-Control','no-cache'),
                        ('Pragma','no-cache'),
                        ('Referer','https://yandex.ru/'),
                        ('Sec-Ch-Ua','"Chromium";v="118", "YaBrowser";v="23.11", "Not=A?Brand";v="99", "Yowser";v="2.5"'),
                        ('Sec-Ch-Ua-Mobile','?0'),
                        ('Sec-Ch-Ua-Platform','"Windows"'),
                        ('Sec-Fetch-Dest','document'),
                        ('Sec-Fetch-Mode','navigate'),
                        ('Sec-Fetch-Site','none'),
                        ('Sec-Fetch-User','?1'),
                        ('Upgrade-Insecure-Requests','1'),
                        ('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36')])

        DROM_headers = collections.OrderedDict({
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'ru,en;q=0.9',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Cookie':'ring=97b583aj4FiBeoFzWcZCAFYJAY6DA0ad; cookie_cityid=1; cookie_regionid=77; _ga=GA1.1.687903372.1706174070; _ym_uid=1706174071106200016; _ym_d=1706174071; my_geo=77; segSession=IjAxY2EzMTYzZDlkMTcyMjFkZDllZDUzMjEzYzZmN2Njbm90QXV0aDk3YjU4M2FqNEZpQmVvRnpXY1pDQUZZSkFZNkRBMGFkIl9mZDBjMDBkMmFjODYzZTIyNjcyYzQ1ZjUwYjJiNDgyZQ; _ym_isad=2; dr_df=1; ndyr=1706788830; drom_search_web=2; _ga_1G91VLKB2K=GS1.1.1706788717.7.1.1706788835.36.0.0',
            'Host':'auto.drom.ru',
            'Pragma':'no-cache',
            'Referer':'https://auto.drom.ru/lada/',
            'Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
        })

        session.headers={}

        response = session.get(url="https://auto.drom.ru/lada/2110/", headers=DROM_headers)
        print(f"ОТвет: {response.status_code}\n")
        print(f"Куки: {response.cookies}\n")
        print(f"Заголовки запроса: {response.request.headers}\n") # Заголовки, которые отправлены браузеру
        print(f"Заголовки ответа: {response.headers}\n\n")
        # print(f"Заголовки ответа: {response.text}\n")
    
if False:
    with requests.Session() as session:
        Headers = collections.OrderedDict({
            'Accept': '',
            'Accept-Encoding': SKIP_HEADER,
            'Connection': '',
            'User-Agent': SKIP_HEADER})
        print(Headers)

        Headers = collections.OrderedDict({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'})
        
        print(Headers)
        session.headers = {}
        response = session.get("https://www.dns-shop.ru/search/?q=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%D1%8B+xiaomi+poco&category=17a8a01d16404e77",
                            headers=Headers)
        print(f"Статус ответа: {response.status_code}\n")
        print(f"Заголовки запроса:{response.request.headers}\n")
        print(f"Заголовки ответа: {response.headers}\n")
        # print(f"Текст: {response.text}\n")


# Заголовки запроса для сайта с бесплатными прокси: https://www.ipaddress.com/proxy-list/
proxy_headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'ru,en;q=0.9',
'Cache-Control':'no-cache',
'Content-Length':'16396',
'Content-Type':'application/x-www-form-urlencoded',
'Cookie':'ezux_lpl_280870=1706615862278|9eb4ee5e-2dc7-4125-4836-d82b82a98e2a|true; ezosuibasgeneris-1=8adfe6fc-885e-4ed8-5e6c-4dd44b329387; _ga=GA1.1.491813669.1706454310; __qca=P0-1924934795-1706454345988; ezux_ifep_280870=true; cf_clearance=fym7htfyAj3rbk4jfsMwxwjMbKJZzgmZwmg1O9miqUQ-1706615810-1-AVyfZKJPpwUfMmjipwboUApxugP8pOeVWZfmxij13Tsc0u0GDE0dwHYSah0zx4Rv+249gyEKMzyof2V/YdnrrEk=; ezovuuidtime_280870=1706615821; ezds=ffid%3D1%2Cw%3D1280%2Ch%3D720; ezohw=w%3D459%2Ch%3D725; _ga_3GT2CLN45N=GS1.1.1706615811.4.1.1706615822.0.0.0; ezux_et_280870=107; ezux_tos_280870=85385; cf_chl_3=b58cdfe377c8a48',
'Origin':'https://www.ipaddress.com',
'Pragma':'no-cache',
'Referer':'https://www.ipaddress.com/proxy-list/?__cf_chl_tk=FAnjnHFqsrHo6JqOKxF_kr8MfWewMPDnqZzYmL_E5t0-1706624063-0-gaNycGzNPns',
"Sec-Ch-Ua":'"Chromium";v="118", "YaBrowser";v="23.11", "Not=A?Brand";v="99", "Yowser";v="2.5"',
'Sec-Ch-Ua-Arch':'"x86"',
'Sec-Ch-Ua-Bitness':'"64"',
'Sec-Ch-Ua-Full-Version':'"23.11.3.966"',
'Sec-Ch-Ua-Full-Version-List':'"Chromium";v="118.0.5993.159", "YaBrowser";v="23.11.3.966", "Not=A?Brand";v="99.0.0.0", "Yowser";v="2.5"',
'Sec-Ch-Ua-Mobile':'?0',
'Sec-Ch-Ua-Model':'""',
'Sec-Ch-Ua-Platform':'"Windows"',
'Sec-Ch-Ua-Platform-Version':'"10.0.0"',
'Sec-Fetch-Dest':'document',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-Site':'same-origin',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36'
}



# humanisation_check()
some = dict()
some['a'] = 'a'
print(some['a'])

dict_rules = {"designer": 
    {
        'one': {'site':'', 
                 'type_product':'',
                 'url':'',
                 'teg_name_url':'',
                 'class_name_url':'',
                 'teg_name_number':'',
                 'class_name_number':''
                },

        'button': [   {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'ПТС'},
                                        {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'о регистрации'},
                                        {'teg_name': 'button', 'class_name': 'ezmft1z0 css-xst070 e104a11t0', 'button_text': 'фото'},
                                        {'teg_name': 'button', 'class_name': 'css-18zgczx e3cb8x01', 'button_text': 'контакты'}],

        'many': [] 
    }

}

# общие сведения
dict_rules['designer']['one']['site'] = 'drom'
dict_rules['designer']['one']['type_product'] = 'лада'
dict_rules['designer']['one']['url'] = '"https://novorossiysk.drom.ru/lada/2110/?unsold=1&distance=100",  # 2 страницы 38 объявлений'

dict_rules['designer']['one']['teg_name_url'] = 'a' # тег ссылки на машину в общем списке ссылок
dict_rules['designer']['one']['class_name_url'] = 'css-1oas0dk e1huvdhj1' # класс ссылки на машину в общем списке ссылок

# сведения для скачивания страниц
dict_rules['designer']['one']['teg_name_number'] = 'a'   # self.tag_link_next_page
dict_rules['designer']['one']['class_name_number'] = 'css-4gbnjj e24vrp30' # self.class_link_next_page


# сведения для поиска и нажатия кнопок при скачивании страниц
dict_rules['designer']['buttons'] = [   {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'ПТС'},
                                        {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'о регистрации'},
                                        {'teg_name': 'button', 'class_name': 'ezmft1z0 css-xst070 e104a11t0', 'button_text': 'фото'},
                                        {'teg_name': 'button', 'class_name': 'css-18zgczx e3cb8x01', 'button_text': 'контакты'}] 


# сведения для скачивания характеристик
dict_rules['designer']['many'] = [] # список из словарей, ключами являются название хар-ки, тег и аттрибуты

print(dict_rules)