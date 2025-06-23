import psycopg2
from config import DB_CONFIG
from datetime import datetime

def create_connection():
    """Создаёт подключение к PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)

def setup_database():
    """Создаёт структуру БД"""
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    file_path TEXT UNIQUE,
                    file_type TEXT,
                    content TEXT,
                    file_size_kb FLOAT,
                    last_modified TIMESTAMP,
                    content_length INTEGER,
                    tsv TSVECTOR
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS tsv_idx 
                ON documents USING GIN(tsv)
            """)
        conn.commit()
    finally:
        conn.close()
    print("Таблица 'documents' готова")

def save_to_database(data):
    """Сохраняет данные в PostgreSQL"""
    if not data:
        print("Нет данных для сохранения!")
        return
    
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            for item in data:
                try:
                    cur.execute("""
                        INSERT INTO documents 
                        (file_path, file_type, content, file_size_kb, 
                         last_modified, content_length, tsv)
                        VALUES (%s, %s, %s, %s, %s, %s, 
                                to_tsvector('russian', %s))
                        ON CONFLICT (file_path) DO UPDATE SET
                            file_type = EXCLUDED.file_type,
                            content = EXCLUDED.content,
                            file_size_kb = EXCLUDED.file_size_kb,
                            last_modified = EXCLUDED.last_modified,
                            content_length = EXCLUDED.content_length,
                            tsv = EXCLUDED.tsv
                    """, (
                        item['path'],
                        item['type'],
                        item['content'],
                        item['size_kb'],
                        item['modified'],
                        item['content_length'],
                        item['content']
                    ))
                except Exception as e:
                    print(f"Ошибка сохранения {item['path']}: {str(e)}")
                    conn.rollback()
        conn.commit()
        print(f"Успешно сохранено {len(data)} записей")
    finally:
        conn.close()