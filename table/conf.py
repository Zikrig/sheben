import psycopg2
from psycopg2 import Error

def select_one(my, zap):
    try:
        conn = psycopg2.connect(
            user=my['user'], 
            password=my['password'],
            host=my['host'],
            database=my['database']
        )
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()  
        res = cursor.fetchone()
        if res == None:
            res = []
        cursor.close()
        conn.close()
    except Error as error:
        res = []
        # print(f'Ошибка {error}')
        res = []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        return res

def select_all(my, zap, rasp=False):
    try:
        conn = psycopg2.connect(
            user=my['user'], 
            password=my['password'],
            host=my['host'],
            database=my['database']
        )
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()  

        res = cursor.fetchall()

    except Error as error:
        res = []
        print(f'Ошибка {error}')
        # 
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        if rasp:
            res = list(set([r[0] for r in res]))
        return res

def send_some(my, zap, ret=False):
    try:
        conn = psycopg2.connect(
            user=my['user'], 
            password=my['password'],
            host=my['host'],
            database=my['database']
            )
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()
        if ret:
            res = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        else:
            res = -2
    except (Exception, Error) as error:
        print(f'Ошибка {error}')
        res = error
        # return res
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        return res