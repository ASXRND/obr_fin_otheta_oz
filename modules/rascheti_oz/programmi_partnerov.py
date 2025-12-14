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
def get_sales_partners():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Продажи' AND TRIM(accrual_type)='Программы партнёров'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]

    conn.close()
    return result
# ________________________________________________________________________________
# --- ВОЗВРАТЫ ---
def get_returns_partners():
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

# ЗАПУСК ФУНКЦИИ
def programmi_partnerov_main():
    sales_partners = get_sales_partners()
    returns_partners = get_returns_partners()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    itog = sales_partners + returns_partners
    print("\n================= ПРОГРАММЫ ПАРТНЁРОВ =================","\n")
    print("Сумма:", itog, "\n")
    print("ПРОДАЖИ:", "\n", "\n Программы партнеров", sales_partners, "\n")
    print("ВОЗВРАТЫ:", "\n", "\n Программы партнеров", returns_partners)
