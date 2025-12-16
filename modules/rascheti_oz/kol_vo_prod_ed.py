# ===================== ИМПОРТЫ =====================
import os
import sqlite3
from dotenv import load_dotenv

# ===================== НАСТРОЙКИ =====================
load_dotenv()

period = os.getenv("PERIOD")
db_name = os.getenv("DB_NAME")
table_name = os.getenv("TABLE_NAME")

if not period:
    raise ValueError("PERIOD не задан в .env (например 01.11.2025-30.11.2025)")

# ===================== СЕБЕСТОИМОСТЬ (float) =====================
sebestoimost_grey_big_holder = float(os.getenv("grey_big_holder"))
sebestoimost_black_big_holder = float(os.getenv("black_big_holder"))
sebestoimost_brown_big_holder = float(os.getenv("brown_big_holder"))
sebestoimost_white_big_holder = float(os.getenv("white_big_holder"))
sebestoimost_yellow_merc_cap = float(os.getenv("yellow_merc_cap"))
sebestoimost_white_merc_cap = float(os.getenv("white_merc_cap"))
sebestoimost_red_merc_cap = float(os.getenv("red_merc_cap"))
sebestoimost_white_black_merc_cap = float(os.getenv("white_black_merc_cap"))
sebestoimost_black_oval_hooks_2 = float(os.getenv("black_oval_hooks_2"))

# ===================== ДАТЫ =====================
start, end = period.split("-")
start_date = f"{start[6:]}-{start[3:5]}-{start[:2]}"
end_date   = f"{end[6:]}-{end[3:5]}-{end[:2]}"

# ===================== КОЛ-ВО (инициализация) =====================
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

# ===================== ЗАПРОС В БД =====================
def get_kol_vo_by_articles_split(articles: list[str]) -> dict[str, int]:
    placeholders = ",".join("?" for _ in articles)
    query = f"""
        SELECT TRIM(article), COALESCE(SUM(quantity), 0)
        FROM "{table_name}"
        WHERE TRIM(group_service) = 'Продажи'
          AND TRIM(article) IN ({placeholders})
          AND DATE(accrual_date) BETWEEN ? AND ?
        GROUP BY TRIM(article)
    """

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (*articles, start_date, end_date))
        rows = cursor.fetchall()

    result = {article: 0 for article in articles}
    for article, qty in rows:
        result[article] = qty

    return result

# ===================== ЗАГРУЗКА В ПЕРЕМЕННЫЕ =====================
def load_kol_vo_as_globals() -> None:
    data = get_kol_vo_by_articles_split(list(ARTICLES_MAP.keys()))

    for db_article, qty in data.items():
        globals()[ARTICLES_MAP[db_article]] = int(qty)

# ===================== СЕБЕСТОИМОСТЬ ИТОГ =====================
def kol_vo_prod_ed_itog_main() -> float:
    load_kol_vo_as_globals()   # ← ВАЖНО

    sebestoimost_itog = (
        grey_big_holder * sebestoimost_grey_big_holder
        + black_big_holder * sebestoimost_black_big_holder
        + brown_big_holder * sebestoimost_brown_big_holder
        + white_big_holder * sebestoimost_white_big_holder
        + yellow_merc_cap * sebestoimost_yellow_merc_cap
        + white_merc_cap * sebestoimost_white_merc_cap
        + red_merc_cap * sebestoimost_red_merc_cap
        + white_black_merc_cap * sebestoimost_white_black_merc_cap
        + black_oval_hooks_2 * sebestoimost_black_oval_hooks_2
    )

    # print("Себестоимость итог =", sebestoimost_itog)
    return sebestoimost_itog

# ===================== ОСНОВНОЙ ЗАПУСК =====================
def kol_vo_prod_ed_main():
    load_kol_vo_as_globals()

    sebestoimost_itog = kol_vo_prod_ed_itog_main()
    kol_vo_prod_ed = grey_big_holder + black_big_holder + brown_big_holder + white_big_holder + \
                     yellow_merc_cap + white_merc_cap + red_merc_cap + white_black_merc_cap + black_oval_hooks_2

    print("\n================= ПРОДАНО РУБ ЕД =================")

    print("Себестоимость итог =", round(sebestoimost_itog), "Количесво единиц =", kol_vo_prod_ed, "\n")
    print("grey_big_holder:", grey_big_holder, "на сумму", grey_big_holder * sebestoimost_grey_big_holder)
    print("black_big_holder:", black_big_holder, "на сумму", black_big_holder * sebestoimost_black_big_holder)
    print("brown_big_holder:", brown_big_holder, "на сумму", brown_big_holder * sebestoimost_brown_big_holder)
    print("white_big_holder:", white_big_holder, "на сумму", white_big_holder * sebestoimost_white_big_holder)
    print("yellow_merc_cap:", yellow_merc_cap, "на сумму", yellow_merc_cap * sebestoimost_yellow_merc_cap)
    print("white_merc_cap:", white_merc_cap, "на сумму", white_merc_cap * sebestoimost_white_merc_cap)
    print("red_merc_cap:", red_merc_cap, "на сумму", red_merc_cap * sebestoimost_red_merc_cap)
    print("white_black_merc_cap:", white_black_merc_cap, "на сумму", white_black_merc_cap * sebestoimost_white_black_merc_cap)
    print("black_oval_hooks_2:", black_oval_hooks_2, "на сумму", black_oval_hooks_2 * sebestoimost_black_oval_hooks_2)

# ===================== ENTRY POINT =====================
if __name__ == "__main__":
    kol_vo_prod_ed_main()
