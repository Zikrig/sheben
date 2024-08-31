from table.tabler import Tabler
from config_base import mysqldata

tabler = Tabler(mysqldata)

tabler.renew_base()
# tabler.create_bases()

tabler.init_table_post()
print(tabler.posts)
tabler.add_post_simple('❌', '', 'Добро пожаловать! Это первый бот в для всего, что касается щебня!')
tabler.add_post_simple('Щебень', '❌', 'Блок Щебень')

tabler.add_post_simple('Еврофракции', 'Щебень', 'Фракция 4-8\nФракция 8-16\nФракция 5-10\nФракция 10-20\nФракция 16-23,5')
tabler.add_post_simple('Щебень известняковый', 'Щебень', 'Фракция 5-20\nФракция 20-40\nФракция 40-70')
tabler.add_post_simple('ЩПС', 'Щебень', 'ЩПС С5\nЩПС С4')
tabler.add_post_simple('Отсев дробления', 'Щебень', '0-4\n0-2')

tabler.add_post_hard('Документы', '❌','Документы блок')
tabler.add_post_hard('Точка загрузки', '❌','Где мы блок')
tabler.add_post_hard('Контакты', '❌','Контакты блок')
tabler.add_post_hard('Декларация стандарт М800', 'Документы','Декларация 1 блок')
tabler.add_post_hard('Декларация Еврофракции', 'Документы','Декларация 2 блок')
tabler.add_post_hard('Декларации ЩПС', 'Документы','Декларация 3 блок')
tabler.add_post_hard('Декларации отсев', 'Документы','Декларация 4 блок')
tabler.add_post_hard('Сертификат М800', 'Документы','Щебень М800 блок')
tabler.add_post_hard('Паспорта качества', 'Документы','Паспорта качества')

# print(tabler.try_parse_coords('46 54'))