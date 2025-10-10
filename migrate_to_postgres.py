#!/usr/bin/env python3
"""
Скрипт миграции данных с MySQL на PostgreSQL
Запускать только один раз при переходе с MySQL на PostgreSQL
"""

import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def migrate_data():
    """
    Миграция данных с MySQL на PostgreSQL
    """
    print("🚀 Начинаем миграцию данных с MySQL на PostgreSQL...")
    
    # Проверяем наличие .env файла
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден! Создайте его на основе env.example")
        return False
    
    # Проверяем подключение к PostgreSQL
    try:
        import psycopg2
        from config_base import mysqldata
        
        # Подключаемся к PostgreSQL
        conn = psycopg2.connect(
            user=mysqldata['user'],
            password=mysqldata['password'],
            host=mysqldata['host'],
            database=mysqldata['database']
        )
        cursor = conn.cursor()
        
        # Проверяем, есть ли уже данные в PostgreSQL
        cursor.execute("SELECT COUNT(*) FROM Posts")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"⚠️  В PostgreSQL уже есть {count} записей. Миграция не требуется.")
            cursor.close()
            conn.close()
            return True
        
        print("✅ Подключение к PostgreSQL успешно!")
        
        # Создаем таблицу если её нет
        from table.init import init_posts
        init_posts(mysqldata)
        print("✅ Таблица Posts создана/проверена")
        
        cursor.close()
        conn.close()
        
        print("🎉 Миграция завершена успешно!")
        print("📝 Теперь вы можете запустить проект с PostgreSQL:")
        print("   docker-compose up -d")
        
        return True
        
    except ImportError:
        print("❌ psycopg2 не установлен! Установите зависимости:")
        print("   pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Ошибка при миграции: {e}")
        return False

if __name__ == "__main__":
    success = migrate_data()
    sys.exit(0 if success else 1)
