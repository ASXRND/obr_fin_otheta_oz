import sqlite3
from pathlib import Path
import sys

def clear_table(db_path: str, table_name: str):
    db_file = Path(db_path)
    if not db_file.exists():
        print(f"Ошибка: файл базы данных '{db_path}' не найден!")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(f'DELETE FROM "{table_name}"')
        conn.commit()
        print(f"Таблица '{table_name}' очищена.")
    except sqlite3.OperationalError as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python clear_table.py <путь_к_базе> <название_таблицы>")
    else:
        clear_table(sys.argv[1], sys.argv[2])
