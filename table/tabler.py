from table.init import *
from config_base import picdir
from os import remove


    
class Tabler:
    def __init__(self, mysqldata):
        self.mysqldata = mysqldata

    def try_parse_coords(self, coords):
        coords.replace('\n', ' ').replace(',', '.')
        geo = coords.split(' ')
        try:
            g1 = float(geo[0])
            g2 = float(geo[1])
        except:
            return False
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
                if geonew:
                    p_to_add['geo'] = geonew
            
            # if name in keyb:
            #     p_to_add['keyboard'] = keyb[name]

            self.posts[name] = p_to_add

            self.posts_by_ids[str(id)] = p_to_add

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
            # print(post)
            # print(post['father'])
            elif self.posts[post]['father'] in self.keyb:
                father = self.posts[post]['father']
                self.set_keyboard_of_post(post, self.keyb[father])
    
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
            # print(f'К удалению: '+ self.posts_by_ids[id]['image'])
            remove(picdir + self.posts_by_ids[id]['image'])
        except Exception as e:
            print('Ошибка ' + e)
        finally:
            alt_image_by_post(self.mysqldata, id, '')
            self.init_table_post()

    def set_geo(self, id, geo):
        alt_geo_by_post(self.mysqldata, id, geo)
        self.init_table_post()
    
    def del_geo(self, id):
        alt_geo_by_post(self.mysqldata, id, '')
        self.init_table_post()

    def set_descr(self, name, descr):
        alt_descr_by_post(self.mysqldata, name, descr)
        self.init_table_post()

    def del_post_by_id(self, id):
        del_post_by(self.mysqldata, 'id', id)
        self.init_table_post()

    def del_post_by_name(self, name):
        del_post_by(self.mysqldata, 'name', name)
        self.init_table_post()