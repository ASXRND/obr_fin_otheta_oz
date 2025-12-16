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

# --- ВОЗВРАТЫ ---
def get_vozvrat_viruchki():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Возвраты' AND TRIM(accrual_type)='Возврат выручки'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_programmi_partnerov():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Возвраты' AND TRIM(accrual_type)='Программы партнёров'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_balli_za_skidki():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Возвраты' AND TRIM(accrual_type)='Баллы за скидки'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

# ЗАПУСК ФУНКЦИИ
def vozvrati_main():
    vozvrat_viruchki = get_vozvrat_viruchki()
    programmi_partnerov = get_programmi_partnerov()
    balli_za_skidki = get_balli_za_skidki()

    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = vozvrat_viruchki + programmi_partnerov + balli_za_skidki
    print("\n================= ВОЗВРАТЫ =================")
    print("Сумма:", itog, "\n")
    print("Возвраты:", "Возврат выручки", vozvrat_viruchki)
    print("Возвраты:", "Программы партнёров", programmi_partnerov)
    print("Возвраты:", "Баллы за скидки", balli_za_skidki)
    