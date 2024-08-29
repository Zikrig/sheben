from mysql.connector import connect, Error

def select_one(my, zap):
    try:
        conn = connect(
            user=my['user'], 
            password=my['password'],
            host=my['host'],
            database=my['database']
        )
        cursor = conn.cursor(buffered=True)
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
        conn = connect(
            user=my['user'], 
            password=my['password'],
            host=my['host'],
            database=my['database']
        )
        cursor = conn.cursor(buffered=True)
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
        conn = connect(
            user=my['user'], 
            password=my['password'],
            host=my['host'],
            database=my['database']
            )
        cursor = conn.cursor(buffered=True)
        cursor.execute(zap)
        conn.commit()
        if ret:
            res = cursor.lastrowid
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