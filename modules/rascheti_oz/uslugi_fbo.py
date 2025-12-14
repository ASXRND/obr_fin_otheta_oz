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

# --- УСЛУГИ FBO ---
def get_bron_mesta():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги FBO' AND TRIM(accrual_type)='Бронирование места и персонала для поставки с неполным составом в составе грузоместа'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_kros_doking():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги FBO' AND TRIM(accrual_type)='Кросс-докинг'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

# ЗАПУСК ФУНКЦИИ
def uslugi_fbo_main():
    bron_mesta = get_bron_mesta()
    kros_doking = get_kros_doking()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = bron_mesta + kros_doking
    print("\n================= УСЛУГИ FBO =================", "\n")
    print("Сумма:", itog, "\n")
    print("Услуги FBO:","\n", " \n Бронирование места и персонала для поставки с неполным составом в составе грузоместа", bron_mesta, "\n")
    print("Услуги FBO", "\n",  " \n Кросс-докинг", kros_doking)
    return itog  # возвращаем переменную itog