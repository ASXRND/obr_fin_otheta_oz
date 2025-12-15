# ===================== ИМПОРТЫ =====================
import os
import sqlite3
from dotenv import load_dotenv

# ===================== НАСТРОЙКИ =====================
load_dotenv()

period = os.getenv("PERIOD")            # например: 01.11.2025-30.11.2025
db_name = os.getenv("DB_NAME")
table_name = os.getenv("TABLE_NAME")

sebestoimost_grey_big_holder = os.getenv("grey_big_holder")
sebestoimost_black_big_holder = os.getenv("black_big_holder")
sebestoimost_brown_big_holder = os.getenv("brown_big_holder")
sebestoimost_white_big_holder = os.getenv("white_big_holder")
sebestoimost_yellow_merc_cap = os.getenv("yellow_merc_cap")
sebestoimost_white_merc_cap = os.getenv("white_merc_cap")
sebestoimost_red_merc_cap = os.getenv("red_merc_cap")
sebestoimost_white_black_merc_cap = os.getenv("white_black_merc_cap")
sebestoimost_black_oval_hooks_2 = os.getenv("black_oval_hooks_2")

start, end = period.split("-")
start_date = f"{start[6:]}-{start[3:5]}-{start[:2]}"
end_date   = f"{end[6:]}-{end[3:5]}-{end[:2]}"

# ===================== ИНИЦИАЛИЗАЦИЯ ПЕРЕМЕННЫХ =====================
# pylint: disable=undefined-variable
grey_big_holder = 0
black_big_holder = 0
brown_big_holder = 0
white_big_holder = 0
yellow_merc_cap = 0
white_merc_cap = 0
red_merc_cap = 0
white_black_merc_cap = 0
black_oval_hooks_2 = 0

# ===================== СООТВЕТСТВИЕ ИМЁН =====================
# ключ — как в БД
# значение — имя переменной в Python (валидное)
ARTICLES_MAP = {
    "grey_big_holder": "grey_big_holder",
    "black_big_holder": "black_big_holder",
    "brown_big_holder": "brown_big_holder",
    "white_big_holder": "white_big_holder",
    "yellow_merc_cap": "yellow_merc_cap",
    "white_merc_cap": "white_merc_cap",
    "red_merc_cap": "red_merc_cap",
    "white_black_merc_cap": "white_black_merc_cap",
    "2_black_oval_hooks": "black_oval_hooks_2",
}
# ===================== ФУНКЦИЯ ЗАПРОСА В БД =====================
def get_kol_vo_by_articles_split(articles: list[str]) -> dict[str, int]:
    if not articles:
        return {}
    placeholders = ",".join("?" for _ in articles)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = f"""
        SELECT
            TRIM(article) AS article,
            COALESCE(SUM(quantity), 0)
        FROM "{table_name}"
        WHERE TRIM(group_service) = 'Продажи'
          AND TRIM(article) IN ({placeholders})
          AND DATE(accrual_date) BETWEEN ? AND ?
        GROUP BY TRIM(article)
    """
    cursor.execute(query, (*articles, start_date, end_date))
    rows = cursor.fetchall()
    conn.close()
    result = {article: 0 for article in articles}
    for article, qty in rows:
        result[article] = qty
    return result

# ===================== ФУНКЦИЯ ЗАГРУЗКИ В ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =====================
def load_kol_vo_as_globals() -> None:
    articles = list(ARTICLES_MAP.keys())
    data = get_kol_vo_by_articles_split(articles)

    for db_article, qty in data.items():
        var_name = ARTICLES_MAP[db_article]
        globals()[var_name] = qty

# ===================== ОСНОВНОЙ ЗАПУСК =====================
def kol_vo_prod_ed_main():
    load_kol_vo_as_globals()

    	 # РАСЧЁТЫ 
    # Итого по продажам
    itog = grey_big_holder + black_big_holder + brown_big_holder + white_big_holder + \
					 yellow_merc_cap + white_merc_cap + red_merc_cap + white_black_merc_cap + black_oval_hooks_2
    # Себестоимость итог
    sebestoimost_itog = grey_big_holder * float(sebestoimost_grey_big_holder) + \
												black_big_holder * float(sebestoimost_black_big_holder) + \
												brown_big_holder * float(sebestoimost_brown_big_holder) + \
												white_big_holder * float(sebestoimost_white_big_holder) + \
												yellow_merc_cap * float(sebestoimost_yellow_merc_cap) + \
												white_merc_cap * float(sebestoimost_white_merc_cap) + \
												red_merc_cap * float(sebestoimost_red_merc_cap) + \
												white_black_merc_cap * float(sebestoimost_white_black_merc_cap) + \
												black_oval_hooks_2 * float(sebestoimost_black_oval_hooks_2)
    
    print("\n================= ПРОДАНО ШТ =================", "\n")
    print("Продано шт = ", itog, "Себестоимость P = ", sebestoimost_itog, "\n")

    print("Продано: grey_big_holder", int(grey_big_holder), "На сумму", float(sebestoimost_grey_big_holder) * int(grey_big_holder), "\n" )
    print("Продано: black_big_holder", int(black_big_holder), "На сумму", float(sebestoimost_black_big_holder) * int(black_big_holder), "\n")
    print("Продано: brown_big_holder", int(brown_big_holder), "На сумму", float(sebestoimost_brown_big_holder) * int(brown_big_holder), "\n")
    print("Продано: white_big_holder", int(white_big_holder), "На сумму", float(sebestoimost_white_big_holder) * int(white_big_holder), "\n")
    print("Продано: yellow_merc_cap", int(yellow_merc_cap), "На сумму", float(sebestoimost_yellow_merc_cap) * int(yellow_merc_cap), "\n")
    print("Продано: white_merc_cap", int(white_merc_cap), "На сумму", float(sebestoimost_white_merc_cap) * int(white_merc_cap), "\n")
    print("Продано: red_merc_cap", int(red_merc_cap), "На сумму", float(sebestoimost_red_merc_cap) * int(red_merc_cap), "\n")
    print("Продано: white_black_merc_cap", int(white_black_merc_cap), "На сумму", float(sebestoimost_white_black_merc_cap) * int(white_black_merc_cap), "\n")
    print("Продано: black_oval_hooks_2", int(black_oval_hooks_2), "На сумму", float(sebestoimost_black_oval_hooks_2) * int(black_oval_hooks_2), "\n")

if __name__ == "__main__":
    kol_vo_prod_ed_main()


    









# # Кол-во проданных white_big_holder
# def get_white_big_holder_kol_vo():
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute(f"""
#         SELECT COALESCE(SUM(quantity), 0)
#         FROM "{table_name}"
#         WHERE TRIM(group_service) = 'Продажи'
#           AND TRIM(article) = 'white_big_holder'
#           AND DATE(accrual_date) BETWEEN ? AND ?
#     """, (start_date, end_date))
#     result = cursor.fetchone()[0]
#     conn.close()
#     return result
