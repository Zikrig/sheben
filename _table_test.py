from table.tabler import Tabler
from config_base import mysqldata

tabler = Tabler(mysqldata)

tabler.renew_base()
# tabler.create_bases()

tabler.init_table_post()
print(tabler.posts)
tabler.add_post_simple('❌', '', 'Добро пожаловать! Это первый бот в для всего, что касается щебня!')
tabler.add_post_simple('Щебень', '❌', 'Блок Щебень')
tabler.add_post_simple('Щебень известняковый', 'Щебень', 'Фракция 5-20\nФракция 20-40\nФракция 40-70')
