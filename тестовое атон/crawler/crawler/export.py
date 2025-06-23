import psycopg2
import csv

def export_to_csv(db_config, query, output_file):
    """Экспортирует данные из PostgreSQL в CSV-файл."""
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        
        # Выполнение запроса
        cursor.execute(query)
        
        # Получение данных
        rows = cursor.fetchall()
        
        # Получение имен столбцов
        column_names = [desc[0] for desc in cursor.description]
        
        # Запись данных в CSV-файл
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)  # Запись заголовков
            writer.writerows(rows)          # Запись данных

        print(f"Данные успешно экспортированы в {output_file}")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрытие соединения
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Пример использования
if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'user': 'postgres',
        'password': '1234',
        'database': 'documents',
  # или IP-адрес вашего сервера
        'port': '5432'        # стандартный порт PostgreSQL
    }
    
    query = "SELECT * FROM documents;"  # Замените на ваш SQL-запрос
    output_file = 'output_table.csv'  # Укажите имя выходного CSV-файла

    export_to_csv(db_config, query, output_file)
