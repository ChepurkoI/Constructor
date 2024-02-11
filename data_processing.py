import pandas as pd
import string


def number_conversion(data: str):
    return int(data) if data.isdigit() else data


database = pd.read_feather('DataBase_305.feather')
print(database.keys())

# 'Объявление', 'Цена (руб.)', 'Город', 'Дата и номер объявления',
#        'Количество просмотров', 'Мнение о цене от Drom', 'Двигатель',
#        'Мощность (л.с.)', 'Цвет', 'Поколение', 'Комплектация', 'Пробег (км)',
#        'Характеристики и ПТС', 'Записи о регистрации', 'Информация о розыске',
#        'Информация об ограничениях', 'Марка модель по ПТС',
#        'Год выпуска по ПТС', 'Рабочий объем по ПТС (см3)',
#        'Мощность по ПТС (л.с.)', 'Цвет по ПТС', 'Фотографии', 'Источник'

for index in database.index:
    piece_delete = len(database.loc[index, "Цена (руб.)"]) - len('₽')
    database.loc[index, "Цена (руб.)"] = number_conversion(database.loc[index, "Цена (руб.)"][:piece_delete].replace(" ", ""))

    database.loc[index, "Город"] = database.loc[index, "Город"][len('Город: '):]

    database.loc[index, "Количество просмотров"] = number_conversion(database.loc[index, "Количество просмотров"])

    piece_delete = len(database.loc[index, "Мощность (л.с.)"]) - len(' л.с., налог')
    database.loc[index, "Мощность (л.с.)"] = number_conversion(database.loc[index, "Мощность (л.с.)"][:piece_delete])

    # piece_delete = len(database.loc[index, "Поколение"]) - len(' поколение')
    # database.loc[index, "Поколение"] = number_conversion(database.loc[index, "Поколение"][:piece_delete])

    piece_delete = len(database.loc[index, "Пробег (км)"]) - len('км')
    database.loc[index, "Пробег (км)"] = number_conversion(database.loc[index, "Пробег (км)"][:piece_delete].replace(" ", ""))

    database.loc[index, 'Записи о регистрации'] = database.loc[index, 'Записи о регистрации'].replace("с ", "\nс ")

    database.loc[index, "Марка модель по ПТС"] = database.loc[index, "Марка модель по ПТС"][len('Марка модель: '):]

    database.loc[index, "Год выпуска по ПТС"] = number_conversion(database.loc[index, "Год выпуска по ПТС"][len('Год выпуска: '):])

    database.loc[index, "Рабочий объем по ПТС (см3)"] = number_conversion(database.loc[index, "Рабочий объем по ПТС (см3)"][len('Рабочий объем (см3): '):])

    database.loc[index, "Мощность по ПТС (л.с.)"] = number_conversion(database.loc[index, "Мощность по ПТС (л.с.)"][len('Мощность (л.с.): '):])

    database.loc[index, "Цвет по ПТС"] = database.loc[index, "Цвет по ПТС"][len('Цвет: '):]

    database.loc[index, 'Фотографии'] = len(database.loc[index, 'Фотографии'])
    print(database.iloc[index], "\n\n")
    pass


database.to_csv("csv_data.xlsx", index=False)
