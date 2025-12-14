from modules.rab_s_tablicami.db_create import create_db 
from modules.rab_s_tablicami.clear_table import clear_table 
from modules.rab_s_tablicami.drop_table import drop_table 
from modules.rab_s_tablicami.load_excel_to_db import load_excel_to_db

from modules.rascheti_oz.proda_i_vozvrati import proda_i_vozvrati_main
from modules.rascheti_oz.viruchka import viruchka_main
from modules.rascheti_oz.programmi_partnerov import programmi_partnerov_main
from modules.rascheti_oz.balli_za_skidki import balli_za_skidki_main
from modules.rascheti_oz.voznagr_ozon import voznagr_ozon_main
from modules.rascheti_oz.uslugi_dostavki import uslugi_dostavki_main
from modules.rascheti_oz.uslugi_fbo import uslugi_fbo_main
from modules.rascheti_oz.prod_i_reklama import prod_i_reklama_main
from modules.rascheti_oz.uslugi_agentov import uslugi_agentov_main
from modules.rascheti_oz.drugie_uslugi import drugie_uslugi_main
from modules.rascheti_oz.prochie_nachisleniya import prochie_nachisleniya_main
from modules.rascheti_oz.vozvrati import vozvrati_main
from modules.rascheti_oz.nachisleniya import nachisleniya_main
import importlib
import inspect
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()

# Проверяем наличие переменных окружения
# Список нужных переменных
required_vars = ["TABLE_NAME", "DB_NAME", "DB_NAME_CREATE" , "TABLE_NAME_CREATE", "EXCEL_FILE"]
# Проверяем их наличие
missing_vars = [var for var in required_vars if os.getenv(var) is None]
missing_vars = [var for var in required_vars if os.getenv(var) is None]

if missing_vars:
    print(f"ВНИМАНИЕ! Не найдены переменные окружения: {missing_vars}")
    exit(1)

# Название рабочей таблицы которая уже есть в базе 
table_name = os.getenv("TABLE_NAME")
# имя рабочей базы данных
db_name = os.getenv("DB_NAME")
# при создании db имя файла базы данных
db_name_create = os.getenv("DB_NAME_CREATE")
# При создании новой таблицы в базу данных
table_name_create = os.getenv("TABLE_NAME_CREATE")
excel_file = os.getenv('EXCEL_FILE')
# print(f"Все переменные = {table_name}, {db_name}, {db_name_create}, {table_name_create}, {excel_file} ок")

def zapusk_otcheta():
    # Продажи и возвраты
    proda_i_vozvrati_main()
    # Выручка
    viruchka_main()
    # Программы партнёров
    programmi_partnerov_main()
    # Баллы за скидки
    balli_za_skidki_main()
    # Вознаграждения OZON
    voznagr_ozon_main()
    # Услуги доставки
    uslugi_dostavki_main()
    # Услуги FBO
    uslugi_fbo_main()
    # Услуги агентов
    uslugi_agentov_main()
    # Продвижение и реклама
    prod_i_reklama_main()
    # Другие услуги
    drugie_uslugi_main()
    # Прочие начисления
    prochie_nachisleniya_main()
    # Возвраты
    vozvrati_main()
    # Начисления
    nachisleniya_main()

def main():
    # заглушка
    # pass
    # запуск отчета
    # zapusk_otcheta()
    #____________________________________________________м
    # print("Загружаю данные из Excel в базу.")
    # load_excel_to_db(db_name, excel_file, table_name)
    # print("Данные успешно загружены.")
    #____________________________________________________
    # запуск отчета
    zapusk_otcheta()
    # ________________________________________________________
    # print("Создаю базу данных.")
    # create_db(db_name_create) 
    # print("Успешное создание базы.")
    # ________________________________________________________
    # Очистка таблицы
    # clear_table(db_name, table_name)
    # print("Данные очищены.")
    # ________________________________________________________
    # Удаление таблицы
    # drop_table(db_name, table_name)
    # ________________________________________________________
    # По умолчанию разметка таблицы для фин отчета озон
    # print("Создаю таблицу.")
    # create_table(db_name,table_name_create)
    # print("Таблица успешно создана.")
    # ________________________________________________________

if __name__ == "__main__":
    main()