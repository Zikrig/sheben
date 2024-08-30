from table.tabler import Tabler
from config_base import mysqldata

tabler = Tabler(mysqldata)

tabler.renew_base()
# tabler.create_base()

tabler.init_table_post()
tabler.add_post_hard('❌', '', 'Добро пожаловать! Это первый бот в для всего, что касается щебня!')
tabler.add_post_simple('Щебень', '❌', 'Вашему вниманию предлагаются следующие виды щебня:')

tabler.add_post_simple('Еврофракции', 'Щебень', 'Фракция 4-8\nФракция 8-16\nФракция 5-10\nФракция 10-20\nФракция 16-23,5')
tabler.add_post_simple('Щебень известняковый', 'Щебень', 'Фракция 5-20\nФракция 20-40\nФракция 40-70')
tabler.add_post_simple('ЩПС', 'Щебень', 'ЩПС С5\nЩПС С4')
tabler.add_post_simple('Отсев дробления', 'Щебень', '0-4\n0-2')
tabler.add_post_simple('Документы', '❌', 'Здесь расположена информация о документах')
tabler.add_post_hard('Где мы', '❌','Наш карьер находится...')
tabler.add_post_hard('Сертификат', 'Документы','Наш сертификат представлен здесь')
