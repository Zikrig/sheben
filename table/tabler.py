from table.init import *
from config_base import picdir
from os import remove, path


    
class Tabler:
    def __init__(self, mysqldata):
        self.mysqldata = mysqldata

    def try_parse_coords(self, coords):
        coords = coords.replace('\n', ' ').replace(',', '.')
        geo = coords.split(' ')
        try:
            g1 = float(geo[0])
            g2 = float(geo[1])
        except:
            return (-1, -1)
        finally:
            return (g1, g2)
        
    def renew_base(self):
        del_posts(self.mysqldata)
        init_posts(self.mysqldata)
        
    def create_base(self):
        init_posts(self.mysqldata)
        
    def init_table_post(self):
        posts_raw = get_all_posts(self.mysqldata)

        self.posts = {}
        self.posts_by_ids = {}
        # self.postlists = {}
        for post in posts_raw:
            (id,  name, father, textof, typeof, image, geo) = post
            p_to_add = {
                'id': id,
                'name': name,
                'textof': textof,
                'textalt': textof + '\n/alt_' + str(id),
                'father': father,
                'typeof': typeof,
                # 'image': image,
                # 'geo': geo
            }

            if image != '':
                p_to_add['image'] = image
                
            if geo != '':
                geonew = self.try_parse_coords(geo)
                if geonew[0] != -1:
                    p_to_add['geo'] = geonew
            
            # if name in keyb:
            #     p_to_add['keyboard'] = keyb[name]

            self.posts[name] = p_to_add

            self.posts_by_ids[str(id)] = p_to_add
        
        for post in self.posts:
            p = self.posts[post]
            self.posts_by_ids[str(p['id'])] = p

        self.get_keyb()    

    def get_keyb(self):
        self.keyb = {}
        for post in self.posts:
            father = self.posts[post]['father']
            if father in self.posts:
                # print(f'Обнаружили {father}')
                if not father in self.keyb:
                    self.keyb[father] = []
                self.keyb[father].append(post)
            # else:
                # print(f'НЕТУ{father}')

        for keyb_item in self.keyb:
            if keyb_item != '❌':
                self.keyb[keyb_item].append('❌')
                
        for post in self.posts:
            if post in self.keyb:
                # if self.posts[post]['name'] == '❌':
                #     self.set_keyboard_of_post(post, self.keyb[post])
                # else:
                self.set_keyboard_of_post(post, self.keyb[post])
                self.posts[post]['is_parent'] = True
            # print(post)
            # print(post['father'])
            elif self.posts[post]['father'] in self.keyb:
                father = self.posts[post]['father']
                self.set_keyboard_of_post(post, self.keyb[father])
                self.posts[post]['is_parent'] = False
            
            self.posts_by_ids[str(self.posts[post]['id'])] = self.posts[post]
    
    def set_keyboard_of_post(self, name, keyboard):
        self.posts[name]['keyboard'] = keyboard
        id = str(self.posts[name]['id'])
        self.posts_by_ids[id]['keyboard'] = keyboard 

    def get_post_by_name(self, name):
        if not name in self.posts:
            return False
        # self.posts[name]
        # if admin:
        #     post = self.posts[name]
        #     post['textof'] += '\n/alt_' + str(self.posts[name]['id'])
        #     return post
        return self.posts[name]
    
    def get_post_by_id(self, id):
        # print(self.posts_by_ids)
        if not id in self.posts_by_ids:
            return False
        return self.posts_by_ids[id]
    
    def add_post_simple(self, name, father, textof):
        create_post(self.mysqldata, name, father, textof, 'simple')
        self.init_table_post()

    def add_post_hard(self, name, father, textof):
        create_post(self.mysqldata, name, father, textof, 'hard')
        self.init_table_post()

    def add_post_menu(self, name, father, textof):
        create_post(self.mysqldata, name, father, textof, 'menu')
        self.init_table_post()

    def set_image(self, id, imagepath):
        alt_image_by_post(self.mysqldata, id, imagepath)
        self.init_table_post()
    
    def del_image(self, id):
        try:
            id = str(id)
            if not 'image' in self.posts_by_ids[id] or self.posts_by_ids[id]['image'] == '':
                return True
            # print(f'К удалению: '+ self.posts_by_ids[id]['image'])
            if path.exists(picdir + self.posts_by_ids[id]['image']):
                remove(picdir + self.posts_by_ids[id]['image'])
        except Exception as e:
            print('Ошибка ' + str(e))
        finally:
            alt_image_by_post(self.mysqldata, id, '')
            self.init_table_post()

    def set_geo(self, id, geo):
        # print('Устанавливаем гео ' + geo)
        # if not 'geo' in self.posts_by_ids[str(id)]:
        #     return True
        alt_geo_by_post(self.mysqldata, id, geo)
        self.init_table_post()
    
    def del_geo(self, id):
        alt_geo_by_post(self.mysqldata, id, '')
        self.init_table_post()

    def set_descr(self, id, descr):
        alt_descr_by_post(self.mysqldata, id, descr)
        self.init_table_post()

    def set_name(self, name, newname):
        alt_name_by_post(self.mysqldata, name, newname)
        self.init_table_post()
        # print(self.posts)
        # print(self.posts_by_ids)

    def del_post_by_id(self, id):
        id = str(id)
        if not id in self.posts_by_ids:
            return True
        if self.posts_by_ids[id]['name'] == '❌':
            return True
        
        if self.posts_by_ids[id]['is_parent']:
            for name in self.posts_by_ids[id]['keyboard']:
                # print('Пытаемся удалить дочерний ' + name)
                self.del_post_by_name(name)
        
        self.del_geo(id)
        self.del_image(id)
        del_post_by(self.mysqldata, 'id', id)
        self.init_table_post()

    def del_post_by_name(self, name):
        id = self.posts[name]['id']
        self.del_post_by_id(id)
