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

# --- ПРОДВИЖЕНИЕ И РЕКЛАМА ---
def get_oplata_za_clik():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Продвижение и реклама' AND TRIM(accrual_type)='Оплата за клик'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_balli_za_otzivi():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Продвижение и реклама' AND TRIM(accrual_type)='Баллы за отзывы'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

# ЗАПУСК ФУНКЦИИ
def prod_i_reklama_main():
    oplata_za_clik = get_oplata_za_clik()
    balli_za_otzivi = get_balli_za_otzivi()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = oplata_za_clik + balli_za_otzivi
    print("\n================= ПРОДВИЖЕНИЕ И РЕКЛАМА =================", "\n")
    print("Сумма:", itog, "\n")
    print("Продвижение и реклама:","\n", " \n Оплата за клик", oplata_za_clik, "\n")
    print("Продвижение и реклама:", "\n",  " \n Баллы за отзывы", balli_za_otzivi, "\n")
    return itog  # возвращаем переменную itog