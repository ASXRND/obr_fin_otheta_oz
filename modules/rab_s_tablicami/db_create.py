import sqlite3

def create_db(db_name_create):
    """
    Создаёт файл базы данных SQLite, если его ещё нет.
    Таблицы в этом модуле не создаются.
    """
    try:
        conn = sqlite3.connect(db_name_create)
        print(f"База данных '{db_name_create}' успешно создана (или уже существует).")
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        if conn:
            conn.close()
