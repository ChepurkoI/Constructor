import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

#print(requests.Response.apparent_encoding('https://www.eldorado.ru/c/smartfony/'))
# url = 'https://www.eldorado.ru/c/smartfony/'
# r = requests.get(url)
# code = r.headers 
# print(code['Content-Type'])

path_el = '/home/igor/PycharmProjects/HTML/1.html'
path = '/home/igor/PycharmProjects/HTML/eldo.html'
                  
#
# with open(path, 'r' , encoding="utf-8" ) as html_file:
#     BS4_Tree = BeautifulSoup(html_file, "lxml")
#     #products_list = BS4_Tree
#     temp = BS4_Tree.prettify()
#     print(temp)
#     #print(BS4_Tree)
#
#     Nodes = BS4_Tree.find_all('tbody')
#     print(len(Nodes))
#     for node in Nodes:
#         print(node)
#         print("AA")
#

A = "https://www.eldorado.ru/c/smartfony/"

https = "https://"
print(f"Полная ссылка: {A}")
A1 = A[len(https):]
A2 = A1[:A1.find("/")]
print(f"Ссылка на сайт: {https + A2}")


# res = requests.get("https://www.eldorado.ru/c/smartfony/")
# print(res.encoding)

DB=pd.read_feather('DataBase.feather')
dict_for_post_request = dict()
dict_for_post_request['site'] = 'dns'
dict_for_post_request['type_product'] = "Смартфон"

temp_dict = dict()

for key in DB.columns:
    temp_dict[key] =  list(DB[key].values)
    #print(DB[key].values)
dict_for_post_request["data"] = temp_dict

url = "https://35a4-89-179-47-36.eu.ngrok.io/api/information/"
dict_for_post_request = json.dumps(dict_for_post_request)
r = requests.post(url, data=dict_for_post_request, headers = {'Content-Type': 'application/json'})
print(r)
