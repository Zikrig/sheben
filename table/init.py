from table.conf import *

def init_posts(mysqldata): 
    return send_some(mysqldata, "CREATE TABLE Posts (Id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(30), Father Varchar(30), TextOf VARCHAR(500), TypeOf VARCHAR(10), Image VARCHAR(100) DEFAULT '', Geo VARCHAR(50) DEFAULT '')")

def create_post(mysqldata, name, father, text, typeof):
    num = send_some(mysqldata, f"INSERT INTO Posts (Name, Father, TextOf, TypeOf) VALUES ('{name}', '{father}', '{text}', '{typeof}')", True)
    return num

def alt_image_by_post(mysqldata, id, image):
    return send_some(mysqldata, f"UPDATE Posts set Image = '{image}' WHERE (Id) = ({id})")

def alt_geo_by_post(mysqldata, id, geo):
    return send_some(mysqldata, f"UPDATE Posts set Geo = '{geo}' WHERE (Id) = ({id})")

def alt_descr_by_post(mysqldata, id, descr):
    return send_some(mysqldata, f"UPDATE Posts set TextOf = '{descr}' WHERE (Id) = ({id})")

def alt_name_by_post(mysqldata, name, newname):
    send_some(mysqldata, f"UPDATE Posts set Name = '{newname}' WHERE Name = '{name}'")
    send_some(mysqldata, f"UPDATE Posts set Father = '{newname}' WHERE Name = '{name}'")

def get_all_posts(mysqldata):
    return select_all(mysqldata, "SELECT * FROM Posts")

def del_posts(mysqldata):
    return send_some(mysqldata, "DROP TABLE Posts;")

def del_post_by(mysqldata, bywhat, ar):
    # print(f"Удаляем {str(ar)}")
    if bywhat == 'id':
        return send_some(mysqldata, f"DELETE FROM Posts WHERE Id={str(ar)}")
    else:
        return send_some(mysqldata, f"DELETE FROM Posts WHERE Name='{ar}'")