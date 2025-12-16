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
# Сумируем все услуги FBO
def uslugi_fbo_itog_main():
    return (
        get_bron_mesta()
        + get_kros_doking()
    )

# ЗАПУСК ФУНКЦИИ
def uslugi_fbo_main():
    bron_mesta = get_bron_mesta()
    kros_doking = get_kros_doking()

    itog = (
        bron_mesta
        + kros_doking
    )
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    print("\n================= УСЛУГИ FBO =================")
    print("Сумма:", itog, "\n")
    print("Услуги FBO:", "Бронирование места и персонала для поставки с неполным составом в составе грузоместа", bron_mesta)
    print("Услуги FBO:", "Кросс-докинг", kros_doking)
    
# if __name__ == "__main__":
#     uslugi_fbo_main()
#     uslugi_fbo_itog_main()    