import sqlite3

def create_table(db_name, table_name_create):
    """
    Создаёт таблицу с именем table_name в указанной базе данных.
    Если таблица уже существует, она не пересоздаётся.
    
    Args:
        db_name (str): Имя файла базы данных.
        table_name_create (str): Имя таблицы для создания.
    """
    try:
        conn = sqlite3.connect(db_name)  # <-- здесь подключаемся к базе, а не к таблице
        cursor = conn.cursor()

        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name_create} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_accrual TEXT NOT NULL,                 -- ID начисления
                accrual_date TEXT NOT NULL,           -- Дата начисления (соответствует "Дата начисления")
                group_service TEXT,                   -- Группа услуг
                accrual_type TEXT NOT NULL,           -- Тип начисления
                article TEXT,                         -- Артикул
                sku TEXT,                             -- SKU
                product_name TEXT,                    -- Название товара
                quantity REAL,                        -- Количество
                seller_price REAL,                    -- Цена продавца
                order_processing_date TEXT,           -- Дата принятия заказа к обработке или оказания услуги
                sales_platform TEXT,                  -- Платформа продажи
                work_scheme TEXT,                     -- Схема работы
                ozon_fee_pct REAL,                    -- Вознаграждение Ozon, %
                localization_index_pct REAL,          -- Индекс локализации, %
                avg_delivery_hours REAL,              -- Среднее время доставки, часы
                total_amount_rub REAL NOT NULL,       -- Сумма итог, руб.
                report_loaded_at TEXT NOT NULL        -- Время, когда этот JSON-файл был загружен
            )
        ''')

        conn.commit()
        print(f"Таблица '{table_name_create}' успешно создана (или уже существует).")

    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        if conn:
            conn.close()



