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

# --- ЛОГИСТИКА ---
def get_logistika():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги доставки' AND TRIM(accrual_type)='Логистика'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]

    conn.close()
    return result

def get_obrab_vozvratov():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги доставки' AND TRIM(accrual_type)='Обработка возвратов Ozon'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]

    conn.close()
    return result

def get_obr_otmen():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги доставки' AND TRIM(accrual_type)='Обработка отменённых и невостребованных товаров'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]

    conn.close()
    return result

def get_obrat_logistika():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги доставки' AND TRIM(accrual_type)='Обратная логистика'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]

    conn.close()
    return result

def get_drop_off():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги доставки' AND TRIM(accrual_type)='Обработка отправления Drop-off (ПВЗ)'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]

    conn.close()
    return result

# Сумируем все другие услуги
def uslugi_dostavki_itog_main():
    return (
        get_logistika()
        + get_obrab_vozvratov()
        + get_obr_otmen()
        + get_obrat_logistika()
        + get_drop_off()
    )

def uslugi_dostavki_main(silent=False):
    logistika = get_logistika()
    obrab_vozvratov = get_obrab_vozvratov()
    obr_otmen = get_obr_otmen()
    obr_ligistika = get_obrat_logistika()
    drop_off = get_drop_off()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    total_sales = logistika + obrab_vozvratov + obr_otmen + obr_ligistika + drop_off
    # Итого по возвратам
    itog = total_sales
    if not silent:
        print("\n================= УСЛУГИ ДОСТАВКИ =================")
        print("Сумма:", itog, "\n")
        print( "", "Услуги доставки:", "Логистика", logistika, "\n", 
              "Услуги доставки:", "Обработка возвратов Ozon", obrab_vozvratov, "\n",  
              "Услуги доставки:", "Обработка отменённых и невостребованных товаров", obr_otmen, "\n",
              "Услуги доставки:", "Обратная логистика", obr_ligistika, "\n",
              "Услуги доставки:", "Обработка отправления Drop-off (ПВЗ)", drop_off)
    
  

