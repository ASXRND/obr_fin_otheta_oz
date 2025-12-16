import os
import pandas as pd
import sqlite3
from datetime import datetime
import warnings

from dotenv import load_dotenv
import os

load_dotenv()

table_name = os.getenv("TABLE_NAME")

# Подавляем предупреждение openpyxl
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def load_excel_to_db(db_name, excel_file, table_name, skiprows=2):
    """
    Загружает данные из Excel-файла в существующую таблицу fin_transactions_ozon_detailed.
    report_loaded_at автоматически проставляется текущей датой и временем.
    Добавляется поле report_period для разграничения периодов.
    """

    # Извлекаем период из имени файла (формат: Отчет по начислениям_DD.MM.YYYY-DD.MM.YYYY.xlsx)
    import re
    match = re.search(r'(\d{2}\.\d{2}\.\d{4})-(\d{2}\.\d{2}\.\d{4})', excel_file)
    if match:
        start_str, end_str = match.groups()
        start_date = f"{start_str[6:]}-{start_str[3:5]}-{start_str[:2]}"
        end_date = f"{end_str[6:]}-{end_str[3:5]}-{end_str[:2]}"
        
        # Удаляем существующие данные за этот период
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"""
            DELETE FROM "{table_name}" 
            WHERE DATE(accrual_date) BETWEEN '{start_date}' AND '{end_date}'
        """)
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        print(f"Удалено {deleted_count} существующих записей за период {start_date} - {end_date}")
    else:
        print("Не удалось извлечь период из имени файла, данные будут добавлены без удаления существующих")

    # Проверка существования базы
    if not os.path.exists(db_name):
        raise FileNotFoundError(f"База '{db_name}' не найдена!")

    # Целевые имена столбцов
    columns = [
        "id_accrual", "accrual_date", "group_service", "accrual_type", "article",
        "sku", "product_name", "quantity", "seller_price", "order_processing_date",
        "sales_platform", "work_scheme", "ozon_fee_pct", "localization_index_pct",
        "avg_delivery_hours", "total_amount_rub"
    ]

    # Чтение Excel
    df = pd.read_excel(excel_file, header=None, skiprows=skiprows)

    # Проверка колонок
    if df.shape[1] < len(columns):
        raise ValueError(f"В Excel меньше колонок ({df.shape[1]}) чем ожидается ({len(columns)})")

    df.columns = columns
    df = df.where(pd.notnull(df), None)  # NaN → None

    # Заполняем пустые id_accrual
    df['id_accrual'] = df['id_accrual'].fillna('N/A')

    # Фильтруем строки с пустыми обязательными полями
    df = df.dropna(subset=['id_accrual', 'accrual_date'])

    # Проверка обязательных полей
    if df['accrual_date'].isnull().any() or df['id_accrual'].isnull().any():
        raise ValueError("В некоторых строках отсутствует id_accrual или accrual_date.")

    # Преобразуем datetime в строки
    datetime_cols = ['accrual_date', 'order_processing_date']
    for col in datetime_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else None)

    # Добавляем report_loaded_at
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['report_loaded_at'] = now_str

    # Подключение к базе
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    added_count = 0

    # Вставка всех строк (включая дубликаты)
    for index, row in df.iterrows():
        # Получаем все значения для вставки
        insert_values = [row[col] for col in columns] + [now_str]
        
        # INSERT: вставляем все поля (дубликаты будут добавлены как отдельные записи)
        placeholders = ", ".join(["?"] * len(insert_values))
        cursor.execute(
            f"""
            INSERT INTO "{table_name}"
            ({', '.join(columns + ['report_loaded_at'])})
            VALUES ({placeholders})
            """,
            insert_values
        )
        added_count += 1

    conn.commit()
    conn.close()

    print(f"Файл '{excel_file}' успешно загружен в базу '{db_name}'.")
    print(f"Добавлено записей: {added_count}")
