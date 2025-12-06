import asyncio  # noqa
import uvloop  # noqa

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, __version__, idle  # noqa: E402
from pyrogram.raw.all import layer  # noqa: E402
from pyropatch import flood_handler, pyropatch  # noqa: E402, F401

from clonebot import API_HASH, APP_ID, BOT_TOKEN, SESSION  # noqa: E402

bot = None
user = None


async def main():
    global bot, user
    plugins = dict(root="clonebot/plugins")
    bot = Client(
        name="clonebot",
        api_id=APP_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=plugins,
    )
    if SESSION:
        user = Client(
            name="user_clonebot",
            api_id=APP_ID,
            api_hash=API_HASH,
            session_string=SESSION,
            plugins=plugins,
        )
    async with bot:
        print(
            f"{bot.me.first_name} - @{bot.me.username} - Pyrogram v{__version__} (Layer {layer}) - Bot Started..."
        )
        if user:
            await user.start()
            print(
                f"{user.me.first_name} - @{user.me.username} - Pyrogram v{__version__} (Layer {layer}) - User Started..."
            )

        await idle()

        await bot.stop()
        print(f"{bot.me.first_name} - @{bot.me.username} - Bot Stopped !!!")
        if user:
            await user.stop()
            print(f"{user.me.first_name} - @{user.me.username}- User Stopped !!!")


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
