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

# Сумируем все другие услуги
def voznagr_ozon_itog_main():
    return (
        get_vozn_za_proda()
        + get_vozvrat_voznag()
    )

# ЗАПУСК ФУНКЦИИ
def voznagr_ozon_main(silent=False):
    vozn_za_proda = get_vozn_za_proda()
    vozvrat_voznag = get_vozvrat_voznag()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    itog = (vozn_za_proda + vozvrat_voznag)
    if not silent:
        print("\n================= ВОЗНАГРАЖДЕНИЕ ОЗОН =================")
        print("Сумма:", itog, "\n")
        print("Вознаграждение:" , vozn_za_proda)
        print("Возврат вознаграждения:" , vozvrat_voznag)
    