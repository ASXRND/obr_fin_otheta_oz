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

# --- ПРОЧИЕ НАЧИСЛЕНИЯ ---
def get_vzaim_raschet_mech_dogovorami():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Прочие начисления' AND TRIM(accrual_type)='Взаимозачет требований между Договорами'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result

# ЗАПУСК ФУНКЦИИ
def prochie_nachisleniya_main():
    vzaim_raschet_mech_dogovorami = get_vzaim_raschet_mech_dogovorami()

    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    itog = vzaim_raschet_mech_dogovorami
    print("\n================= ПРОЧИЕ НАЧИСЛЕНИЯ =================", "\n")
    print("Сумма:", itog, "\n")
    print("Другие услуги:","\n", " \n Обработка операционных ошибок продавца: отгрузка в нерекомендованный слот", vzaim_raschet_mech_dogovorami, "\n")
    