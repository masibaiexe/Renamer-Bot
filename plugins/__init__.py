#  Telegram MTProto API Client Library for Telethon
#  Copyright (C) 2017-present DigitalBotz <https://github.com/DigitalBotz>
#  I am a telegram bot, I created it using Telethon library.
"""
Apache License 2.0
Copyright (c) 2022 @Digital_Botz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Telegram Link : https://t.me/Digital_Botz 
Repo Link : https://github.com/DigitalBotz/Digital-Rename-Bot
License Link : https://github.com/DigitalBotz/Digital-Rename-Bot/blob/main/LICENSE
"""

__name__ = "Digital-Rename-Bot"
__version__ = "3.1.0"
__license__ = " Apache License, Version 2.0"
__copyright__ = "Copyright (C) 2022-present Digital Botz <https://github.com/DigitalBotz>"
__programer__ = "<a href=https://github.com/DigitalBotz/Digital-Rename-Bot>Digital Botz</a>"
__library__ = "<a href=https://docs.telethon.dev/en/stable/>Tᴇʟᴇᴛʜᴏɴ</a>"
__language__ = "<a href=https://www.python.org/>Pyᴛʜᴏɴ 3</a>"
__database__ = "<a href=https://cloud.mongodb.com/>Mᴏɴɢᴏ DB</a>"
__developer__ = "<a href=https://t.me/Digital_Botz>Digital Botz</a>"
__maindeveloper__ = "<a href=https://t.me/RknDeveloper>RknDeveloper</a>"

# main copyright herders (©️)
# I have been working on this repo since 2022

from plugins.force_sub import not_subscribed, forces_sub, handle_banned_user_status
from telethon import events
from config import Config

# Only register handlers if the BOT instance is initialized (avoids errors during initial import)
if hasattr(Config, 'BOT') and Config.BOT:
    
    # Handler 1: Banned User Status
    # Checks every incoming private message
    @Config.BOT.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def banned_check_handler(event):
        # We pass the bot instance and the event (message)
        await handle_banned_user_status(Config.BOT, event)
    
    # Handler 2: Force Subscription
    # Custom filter function to check if user is NOT subscribed
    async def _force_sub_filter(event):
        if not event.is_private:
            return False
        # Returns True if user is NOT subscribed (triggering the handler)
        # Assumes not_subscribed is updated to accept (client, event)
        return await not_subscribed(Config.BOT, event)

    @Config.BOT.on(events.NewMessage(incoming=True, func=_force_sub_filter))
    async def forces_sub_handler(event):
        await forces_sub(Config.BOT, event)
