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


# --- УСЛУГИ АГЕНТОВ ---
def get_okvairing():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги агентов' AND TRIM(accrual_type)='Эквайринг'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_obrab_otpr_dropoff():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги агентов' AND TRIM(accrual_type)='Обработка отправления Drop-off партнёрами (АПВЗ)'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_dost_do_mest_vidachi():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги агентов' AND TRIM(accrual_type)='Доставка до места выдачи'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_obrat_vozv_i_omen():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Услуги агентов' AND TRIM(accrual_type)='Обработка возвратов, отмен и невыкупов партнёрами'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

def uslugi_agentov_main():
    okvairing = get_okvairing()
    obrab_otpr_dropoff = get_obrab_otpr_dropoff()
    dost_do_mest_vidachi = get_dost_do_mest_vidachi()
    obrat_vozv_i_omen = get_obrat_vozv_i_omen()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    total_sales = okvairing + obrab_otpr_dropoff + dost_do_mest_vidachi + obrat_vozv_i_omen
    # Итого по возвратам
    itog = total_sales
    print("\n================= УСЛУГИ АГЕНТОВ =================", "\n")
    print("Сумма:", itog, "\n")
    print("Услуги агентов:","\n", "\n Эквайринг", okvairing, "\n Обработка отправления Drop-off партнёрами (АПВЗ)", obrab_otpr_dropoff, "\n Доставка до места выдачи", dost_do_mest_vidachi, "\n Обработка возвратов, отмен и невыкупов партнёрами", obrat_vozv_i_omen, "\n")
    return itog  # возвращаем переменную itog

# if __name__ == "__main__":
#     uslugi_agentov_main()
  

