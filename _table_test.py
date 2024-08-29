from table.tabler import Tabler
from config_base import mysqldata

tabler = Tabler(mysqldata)

# tabler.renew_base()
# tabler.create_base()

tabler.init_table_post()
# # tabler.add_post_simple('❌', '', 'Добро пожаловать! Это первый бот в для всего, что касается щебня!')
# # tabler.add_post_simple('Щебень', '❌', 'Щебень это типа очень крутая вещь. Вашему вниманию предлагаются следующие виды щебня:')
# # tabler.add_post_simple('Песок', '❌', 'Песка крутого тоже очень много')

# # tabler.add_post_simple('Еврофракции', 'Щебень', 'Фракция 4-8\nФракция 8-16\nФракция 5-10\nФракция 10-20\nФракция 16-23,5')
# tabler.add_post_simple('Щебень известняковый', 'Щебень', 'Фракция 5-20\nФракция 20-40\nФракция 40-70')
# tabler.add_post_simple('ЩПС', 'Щебень', 'ЩПС С5\nЩПС С4')
# tabler.add_post_simple('Отсев дробления', 'Щебень', '0-4\n0-2')
# # tabler.add_post_simple('О нас', '❌', 'О нас это замечательный пункт')
# # tabler.add_post_hard('Где мы', 'О нас','Наш карьер находится...')
# tabler.add_post_hard('Сертификат', 'О нас','Наш сертификат представлен здесь')
# # tabler.add_post_hard('Где мы', 'О нас','Наш карьер находится...')

# print(tabler.try_parse_coords('46 54'))