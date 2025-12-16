import sqlite3
from pathlib import Path
import os
from dotenv import load_dotenv
# Загружаем переменные окружения из .env
load_dotenv()

period = os.getenv("PERIOD")
db_name = os.getenv("DB_NAME")
table_name = os.getenv("TABLE_NAME")

start, end = period.split("-")
start_date = f"{start[6:]}-{start[3:5]}-{start[:2]}"  # 2025-11-01
end_date   = f"{end[6:]}-{end[3:5]}-{end[:2]}"        # 2025-11-30

# --- ДРУГИЕ УСЛУГИ ---
def get_obr_oper_oh_prod():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Другие услуги' AND TRIM(accrual_type)='Обработка операционных ошибок продавца: отгрузка в нерекомендованный слот'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_util_tovara():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Другие услуги' AND TRIM(accrual_type)='Утилизация товара: Автоутилизация со стока'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result
# Сумируем все другие услуги
def drugie_uslugi_itog_main():
    return (
        get_obr_oper_oh_prod()
        + get_util_tovara()
    )
# ЗАПУСК ФУНКЦИИ
def drugie_uslugi_main(silent=False):
    obr_oper_oh_prod = get_obr_oper_oh_prod()
    util_tovara = get_util_tovara()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = (
        obr_oper_oh_prod
        + util_tovara
    )
    if not silent:
        print("\n================= ДРУГИЕ УСЛУГИ =================")
        print("Сумма:", itog, "\n")
        print("Другие услуги:", "Обработка операционных ошибок продавца: отгрузка в нерекомендованный слот", obr_oper_oh_prod)
        print("Другие услуги:", "Утилизация товара: Автоутилизация со стока", util_tovara)
    