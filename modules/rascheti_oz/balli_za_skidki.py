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

# --- ПРОДАЖИ ---
def get_balli_za_skidki():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Продажи' AND TRIM(accrual_type)='Баллы за скидки'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result
# ________________________________________________________________________________
# --- ВОЗВРАТЫ ---
def get_balli_za_skidki_voz():
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
def balli_za_skidki_main():
    balli_za_skidki = get_balli_za_skidki()
    balli_za_skidki_voz = get_balli_za_skidki_voz()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    itog = balli_za_skidki + balli_za_skidki_voz
    print("\n================= БАЛЛЫ ЗА СКИДКИ =================", "\n")
    print("Сумма:", itog, "\n")
    print("ПРОДАЖИ:", "\n", " \n Баллы за скидки", balli_za_skidki, "\n")
    print("ВОЗВРАТЫ:","\n", " \n Баллы за скидки", balli_za_skidki_voz)
