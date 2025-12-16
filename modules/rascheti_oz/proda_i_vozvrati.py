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
def get_sales_vyruchka():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COALESCE(SUM(total_amount_rub),0)
        FROM '{table_name}'
        WHERE TRIM(group_service)='Продажи' AND TRIM(accrual_type)='Выручка'
        AND DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result
def get_sales_skidki():
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
def get_returns_vyruchka():
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
def get_returns_skidki():
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
# Сумируем все вознаграждения Озон
def proda_i_vozvrati_itog_main():
    return (
        get_sales_vyruchka()
        + get_sales_skidki()
        + get_sales_partners()
        + get_returns_vyruchka()
        + get_returns_skidki()
        + get_returns_partners()
    )

def proda_i_vozvrati_main():
    sales_vyruchka = get_sales_vyruchka()
    sales_skidki = get_sales_skidki()
    sales_partners = get_sales_partners()
    returns_vyruchka = get_returns_vyruchka()
    returns_skidki = get_returns_skidki()
    returns_partners = get_returns_partners()
    # ________________________________________________________________________________
    # РАСЧЁТЫ 
    # Итого по продажам
    total_sales = sales_vyruchka + sales_skidki + sales_partners
    # Итого по возвратам
    total_returns = returns_vyruchka + returns_skidki + returns_partners
    itog = total_sales + total_returns
    print("\n================= ПРОДАЖИ И ВОЗВРАТЫ =================")
    print("Сумма:", itog, "\n")
    print("","Продажи:", "Выручка", sales_vyruchka, "\n",
              "Продажи:", "Баллы за скидки", sales_skidki, "\n", 
              "Продажи:", "Программы партнеров", sales_partners, "\n", 
              "Продажи:", "Итого продажи", total_sales)
    print("","Возвраты:", "Возврат выручки", returns_vyruchka, "\n"
              "","Возвраты:", "Баллы за скидки", returns_skidki, "\n" 
              "","Возвраты:", "Программы партнеров", returns_partners, "\n" 
              "","Возвраты:", "Итого возврат выручки", total_returns)
    

# if __name__ == "__main__":
# 	proda_i_vozvrati_main()
























# def calculate_articles(db_path=None, table=None):
#     if db_path is None:
#         db_path = db_name
#     if table is None:
#         table = table_name

#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # ======================================================
#     # ВСЕ ЗАПРОСЫ К БАЗЕ — ВВЕРХУ
#     # ======================================================

#     # --- ПРОДАЖИ ---
#     cursor.execute(f"""
#         SELECT COALESCE(SUM(total_amount_rub),0)
#         FROM '{table}'
#         WHERE TRIM(group_service)='Продажи' AND TRIM(accrual_type)='Выручка'
#     """)
#     sales_vyruchka = cursor.fetchone()[0]

#     cursor.execute(f"""
#         SELECT COALESCE(SUM(total_amount_rub),0)
#         FROM '{table}'
#         WHERE TRIM(group_service)='Продажи' AND TRIM(accrual_type)='Баллы за скидки'
#     """)
#     sales_skidki = cursor.fetchone()[0]

#     cursor.execute(f"""
#         SELECT COALESCE(SUM(total_amount_rub),0)
#         FROM '{table}'
#         WHERE TRIM(group_service)='Продажи' AND TRIM(accrual_type)='Программы партнёров'
#     """)
#     sales_partners = cursor.fetchone()[0]

#     # --- ВОЗВРАТЫ ---
#     cursor.execute(f"""
#         SELECT COALESCE(SUM(total_amount_rub),0)
#         FROM '{table}'
#         WHERE TRIM(group_service)='Возвраты' AND TRIM(accrual_type)='Возврат выручки'
#     """)
#     returns_vyruchka = cursor.fetchone()[0]

#     cursor.execute(f"""
#         SELECT COALESCE(SUM(total_amount_rub),0)
#         FROM '{table}'
#         WHERE TRIM(group_service)='Возвраты' AND TRIM(accrual_type)='Баллы за скидки'
#     """)
#     returns_skidki = cursor.fetchone()[0]

#     cursor.execute(f"""
#         SELECT COALESCE(SUM(total_amount_rub),0)
#         FROM '{table}'
#         WHERE TRIM(group_service)='Возвраты' AND TRIM(accrual_type)='Программы партнёров'
#     """)
#     returns_partners = cursor.fetchone()[0]

#     conn.close()

#     # ======================================================
#     # ПРОСТЫЕ РАСЧЁТЫ — МАКСИМАЛЬНО ПРОЗРАЧНО
#     # ======================================================

#     # Итого по продажам
#     total_sales = sales_vyruchka + sales_skidki + sales_partners
#     # Итого по возвратам
#     total_returns = returns_vyruchka + returns_skidki + returns_partners
#     # Чистые продажи
#     net_sales = total_sales - total_returns

#     # Расчёты по блокам для наглядности
#     sales_block = sales_vyruchka + sales_skidki + sales_partners
#     returns_block = returns_vyruchka + returns_skidki + returns_partners

#     # Примеры отдельных комбинаций
#     sales_vyruchka_plus_skidki = sales_vyruchka + sales_skidki
#     sales_vyruchka_plus_partners = sales_vyruchka + sales_partners
#     returns_skidki_plus_partners = returns_skidki + returns_partners

#     # ======================================================
#     # ПРИНТЫ — ВСЁ В ОДНОЙ ФУНКЦИИ
#     # ======================================================
#     print("\n================= ПРОДАЖИ =================")
#     print("Выручка:             ", sales_vyruchka)
#     print("Баллы за скидки:     ", sales_skidki)
#     print("Программы партнёров: ", sales_partners)
#     print("Итого продажи:       ", total_sales)
#     print("-------------------------------------------")
#     print("Продажи (Выручка + Баллы): ", sales_vyruchka_plus_skidki)
#     print("Продажи (Выручка + Партнёры): ", sales_vyruchka_plus_partners)

#     print("\n================= ВОЗВРАТЫ =================")
#     print("Возврат выручки:     ", returns_vyruchka)
#     print("Баллы за скидки:     ", returns_skidki)
#     print("Программы партнёров: ", returns_partners)
#     print("Итого возвраты:      ", total_returns)
#     print("-------------------------------------------")
#     print("Возвраты (Баллы + Партнёры): ", returns_skidki_plus_partners)

#     print("\n================= ИТОГО =================")
#     print("Чистые продажи:       ", net_sales)
#     print("Общее (sales_block - returns_block):", sales_block - returns_block)
#     print("===========================================\n")
