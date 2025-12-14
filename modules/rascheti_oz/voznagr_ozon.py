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
def get_vozn_za_proda():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Вознаграждение Ozon' AND TRIM(accrual_type)='Вознаграждение за продажу'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result
# ________________________________________________________________________________
# --- ВОЗВРАТЫ ---
def get_vozvrat_voznag():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Вознаграждение Ozon' AND TRIM(accrual_type)='Возврат вознаграждения'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

# ЗАПУСК ФУНКЦИИ
def voznagr_ozon_main():
    vozn_za_proda = get_vozn_za_proda()
    vozvrat_voznag = get_vozvrat_voznag()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    itog = vozn_za_proda + vozvrat_voznag
    print("\n================= ВОЗНАГРАЖДЕНИЕ ОЗОН =================", "\n")
    print("Сумма:", itog, "\n")
    print("ВОЗНАГРАЖДЕНИЕ:", "\n", "\n", vozn_za_proda, "\n")
    print("ВОЗВРАТ ВОЗНАГРАЖДЕНИЯ:", "\n" , vozvrat_voznag)
    return itog  # возвращаем переменную itog