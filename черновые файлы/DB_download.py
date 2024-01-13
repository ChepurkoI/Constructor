import pandas as pd
import json
import requests
import Class_Timer


def post_request_create():
    DB=pd.read_feather('DataBase.feather')
    columns = DB.columns
    
    list_columns = list(columns)
    payload = dict()
    method = "create"
    product_name = "smartfon_dns"
    payload['list_name'] = list_columns
    payload['method'] = method 
    payload['product_name'] = product_name
    url = 'https://88f3-89-179-41-1.eu.ngrok.io/api/information'
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.text)

def post_request():
    """
        Программа формирует словарь с одним элементом - списком, состоящим из словарей.
        Каждый из словарей содержит все характеристики для одного телефона. {"Название хар-ки" : "Зн-е хар-ки"}
        В конце отправляется запрос.

        Новая задача:
        Реализовать у себя конкатенацию этих словарей в датафрейм, из которого я создал эту поебень.

    """
    DB=pd.read_feather('DataBase.feather')

    # генерируются последовательности для перебора
    columns = DB.columns
    indexes = DB.index
    
    url = "https://88f3-89-179-41-1.eu.ngrok.io/api/information/"
    product_name = "smartfon_dns"
    headers = {'Content-type': 'application/json'}

    list_columns = list(columns)


    
    list_table = list()
    # Внешний цикл идет по телефонам
    for index in indexes:
        
        temp_dict = dict()
        for name_column in columns:
            temp_dict[name_column] = DB[name_column][index]
        list_table.append(temp_dict)
    
    dict_request = {'list_table': list_table, 'list_name' : list_columns}
    dict_request['method'] = 'create'
    dict_request['product_name'] = product_name
        
    r = requests.post(url, data=json.dumps(dict_request), headers=headers)
    print(r.text)

    return list_columns,list_table
        
def list_of_dictionary_to_frame(list_names : list, list_table : list, current_DB : pd.DataFrame):
    """
        :param list_names : list - список названий хар-тик
        :param list_table : list - список словарей, где лежат пары {"назв-е хар-ки" : "зн-е хар-ки"} 
        :param current_DB : pd.DataFrame - текущий фрейм БД, уже содержащий названия столбцов
    """
    # кол-во продуктов в списке
    count_product = len(list_table)

    for num_product in range(count_product):
        #product = list_table[num_product].copy() # копируем словарь

        # создание временного фрейма БД из одного продукта, указывая 
        # названия столбцов: list_table[num_product].keys()      
        #      зн-я хар-тик: list_table[num_product].values() 
        buffer_DB = pd.DataFrame([list_table[num_product].values()], columns = list_names)
        

        # Конкатенация буферной БД и текущей
        current_DB = pd.concat([current_DB,buffer_DB], ignore_index=True)
    return current_DB


DB=pd.read_feather('DataBase.feather')
list_len_col = list()
columns = DB.columns
for column in columns:
    list_len_col.append(len(column))
print("Максимальная длина: ", max(list_len_col))
    


t3 = Class_Timer.Timer(text="Время работы склейки: {:0.5f} с")
t2 = Class_Timer.Timer(text="Время работы запроса: {:0.5f} с")
t2.start()
#columns_names, list_dict_table = post_request()
t2.stop()
#current_DB = pd.DataFrame(columns=columns_names)



t3.start()
#current_DB = list_of_dictionary_to_frame(columns_names,list_dict_table, current_DB)
t3.stop()
#print(current_DB.columns())
#print(current_DB.index())

#print(list_dict_table[0].keys())
#print(list_dict_table[0].values())

# # генерируются последовательности для перебора
# columns = DB.columns
# indexes = DB.index

# list_columns = list(columns)

# method = "create"
# payload['list_name'] = list_columns
# payload['method'] = method 
# url = 'http://127.0.0.1:8000/api/information/'
# headers = {'Content-type': 'application/json'}
# r = requests.post(url, data=json.dumps(payload), headers=headers)

# # Внешний цикл идет по телефонам
# for index in indexes:
#     payload = dict()
#     payload['list_name'] = list_columns
#     payload['method'] = 'addition'

#     for name_column in columns:
#         payload[name_column] = DB[name_column][index]
#     r = requests.post(url, data=json.dumps(payload), headers=headers)

# unical_val = list(set(DB[' Цвет задней панели ']))
# for i in range(len(unical_val)):
#     print(unical_val[i], "\n")

# DB.to_csv('DataBase_NEW.csv')

