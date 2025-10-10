from table.conf import *
from table.initial_data import get_initial_posts

def init_posts(sql_config): 
    return send_some(sql_config, "CREATE TABLE IF NOT EXISTS posts (Id SERIAL PRIMARY KEY, Name VARCHAR(30), Father VARCHAR(30), TextOf VARCHAR(500), TypeOf VARCHAR(10), Image VARCHAR(100) DEFAULT '', Geo VARCHAR(50) DEFAULT '')")

def create_post(sql_config, name, father, text, typeof):
    num = send_some(sql_config, f"INSERT INTO posts (Name, Father, TextOf, TypeOf) VALUES ('{name}', '{father}', '{text}', '{typeof}') RETURNING Id", True)
    return num

def alt_image_by_post(sql_config, id, image):
    return send_some(sql_config, f"UPDATE posts set Image = '{image}' WHERE (Id) = ({id})")

def alt_geo_by_post(sql_config, id, geo):
    return send_some(sql_config, f"UPDATE posts set Geo = '{geo}' WHERE Id = {id}")

def alt_descr_by_post(sql_config, id, descr):
    return send_some(sql_config, f"UPDATE posts set TextOf = '{descr}' WHERE (Id) = ({id})")

def alt_name_by_post(sql_config, name, newname):
    send_some(sql_config, f"UPDATE posts set Name = '{newname}' WHERE Name = '{name}'")
    send_some(sql_config, f"UPDATE posts set Father = '{newname}' WHERE Father = '{name}'")

def get_all_posts(sql_config):
    return select_all(sql_config, "SELECT * FROM posts")

def del_posts(sql_config):
    return send_some(sql_config, "DROP TABLE IF EXISTS posts;")

def del_post_by(sql_config, bywhat, ar):
    # print(f"Удаляем {str(ar)}")
    if bywhat == 'id':
        return send_some(sql_config, f"DELETE FROM posts WHERE Id={str(ar)}")
    else:
        return send_some(sql_config, f"DELETE FROM posts WHERE Name='{ar}'")

def init_default_posts(sql_config):
    """Инициализация базовых постов при первом запуске"""
    # Проверяем, есть ли уже посты в базе
    existing_posts = select_all(sql_config, "SELECT COUNT(*) FROM posts")
    if existing_posts and existing_posts[0][0] > 0:
        print("Посты уже существуют, пропускаем инициализацию")
        return True
    
    print("Инициализируем базовые посты...")
    initial_posts = get_initial_posts()
    
    for post_data in initial_posts:
        try:
            # Экранируем кавычки в тексте
            text_escaped = post_data['textof'].replace("'", "''")
            name_escaped = post_data['name'].replace("'", "''")
            father_escaped = post_data['father'].replace("'", "''")
            
            query = f"INSERT INTO posts (Name, Father, TextOf, TypeOf) VALUES ('{name_escaped}', '{father_escaped}', '{text_escaped}', '{post_data['typeof']}')"
            result = send_some(sql_config, query)
            
            if result == -2:  # Успешное выполнение
                print(f"✓ Создан пост: {post_data['name']}")
            else:
                print(f"✗ Ошибка создания поста {post_data['name']}: {result}")
                
        except Exception as e:
            print(f"✗ Ошибка при создании поста {post_data['name']}: {e}")
    
    print("Инициализация постов завершена!")
    return True