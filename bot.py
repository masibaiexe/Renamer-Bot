# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
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

# extra imports
import aiohttp, asyncio, warnings, pytz, datetime
import logging
import logging.config
import glob, sys
import importlib.util
from pathlib import Path

# Telethon imports
from telethon import TelegramClient, errors, events
from telethon.sessions import StringSession

# bots imports
from config import Config
from plugins.web_support import web_server
# NOTE: Ensure plugins/file_rename.py is also converted to Telethon to export 'app' correctly
from plugins.file_rename import app 

# Get logging configurations
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('BotLog.txt'),
             logging.StreamHandler()]
)
#logger = logging.getLogger(__name__)
logging.getLogger("telethon").setLevel(logging.WARNING)

class DigitalRenameBot(TelegramClient):
    def __init__(self):
        super().__init__(
            session="DigitalRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH
        )
                
    async def start(self):
        # Start the client with the bot token
        await super().start(bot_token=Config.BOT_TOKEN)
        
        me = await self.get_me()
        # Telethon doesn't have a native .mention property, so we create one manually for markdown
        self.mention = f"[{me.first_name}](tg://user?id={me.id})"
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME
        self.premium = Config.PREMIUM_MODE
        self.uploadlimit = Config.UPLOAD_LIMIT_MODE
        
        # Set global config bot instance so plugins can access it
        Config.BOT = self
        
        # Start Web Server
        app_runner = aiohttp.web.AppRunner(await web_server())
        await app_runner.setup()
        bind_address = "0.0.0.0"
        await aiohttp.web.TCPSite(app_runner, bind_address, Config.PORT).start()
        
        # Manual Plugin Loader
        # Telethon doesn't auto-load plugins like Pyrogram, so we keep this manual loading logic.
        # Ensure your plugins use the client instance from Config.BOT or similar logic.
        path = "plugins/*.py"
        files = glob.glob(path)
        for name in files:
            with open(name) as a:
                patt = Path(a.name)
                plugin_name = patt.stem.replace(".py", "")
                plugins_path = Path(f"plugins/{plugin_name}.py")
                import_path = "plugins.{}".format(plugin_name)
                spec = importlib.util.spec_from_file_location(import_path, plugins_path)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules["plugins" + plugin_name] = load
                print("Digital Botz Imported " + plugin_name)
                
        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")

        # Send Startup Messages to Admins
        for admin_id in Config.ADMIN:
            if Config.STRING_SESSION:
                try: 
                    await self.send_message(admin_id, f"𝟮𝗚𝗕+ ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\nNote: Enjoy😂👌.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")                                
                except: 
                    pass
            else:
                try: 
                    await self.send_message(admin_id, f"𝟮𝗚𝗕- ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")                                
                except: 
                    pass
                    
        # Send Startup Log to Channel
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone("Africa/Nairobi"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**🌋 __{self.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Africa/Nairobi`\n\n🉐 Vᴇʀsɪᴏɴ : `v1.0 (Telethon)`</b>")                                
            except Exception as e:
                print(f"Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ: {e}")

    async def stop(self, *args):
        for admin_id in Config.ADMIN:
            try: 
                await self.send_message(admin_id, f"**Bot Stopped....**")                                
            except: 
                pass
                
        print("Bot Stopped 🙄")
        await super().disconnect()


digital_instance = DigitalRenameBot()

def main():
    async def start_services():
        if Config.STRING_SESSION:
            # Start both the userbot (app) and the bot (digital_instance)
            # Assuming 'app' is also a Telethon client or compatible awaitable
            await asyncio.gather(app.start(), digital_instance.start())
        else:
            await asyncio.gather(digital_instance.start())
        
        # Idle / Run until disconnected
        # Telethon uses run_until_disconnected() to block
        print("Services Started. Idling...")
        if Config.STRING_SESSION:
            await asyncio.gather(app.run_until_disconnected(), digital_instance.run_until_disconnected())
        else:
            await digital_instance.run_until_disconnected()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user!")
    finally:
        loop.close()

if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="There is no current event loop")
    try:
        main()
    except errors.FloodWaitError as ft:
        # Telethon's flood wait error is FloodWaitError
        print(f"⏳ FloodWait: Sleeping for {ft.seconds} seconds")
        asyncio.run(asyncio.sleep(ft.seconds))
        print("Now Ready For Deploying!")
        main()
        

# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Update Channel @Digital_Botz & @DigitalBotz_Support
