import asyncio

from bot_create import dp, bot
from handlers import main, alt

dp.include_routers(main.router, alt.router)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))

