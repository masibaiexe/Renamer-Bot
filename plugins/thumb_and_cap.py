# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz & @Rkn_Bots_Updates
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

# imports
from telethon import events, utils
from helper.database import digital_botz
from config import Config

@Config.BOT.on(events.NewMessage(pattern=r'^/set_caption', func=lambda e: e.is_private))
async def add_caption(event):
    rkn = await event.reply("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    
    # Split arguments
    args = event.text.split(" ", 1)
    
    if len(args) == 1:
       return await rkn.edit("**__Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ__\n\nExᴀᴍᴩʟᴇ:- `/set_caption {filename}\n\n💾 Sɪᴢᴇ: {filesize}\n\n⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}\n\bBy: @OtherBs`**")
    
    caption = args[1]
    await digital_botz.set_caption(event.sender_id, caption=caption)
    await rkn.edit("__**✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ**__")
   
@Config.BOT.on(events.NewMessage(pattern=r'^/(del_caption|delete_caption|delcaption)', func=lambda e: e.is_private))
async def delete_caption(event):
    rkn = await event.reply("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    caption = await digital_botz.get_caption(event.sender_id)  
    if not caption:
       return await rkn.edit("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")
    await digital_botz.set_caption(event.sender_id, caption=None)
    await rkn.edit("__**❌️ Cᴀᴩᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ**__")
                                       
@Config.BOT.on(events.NewMessage(pattern=r'^/(see_caption|view_caption)', func=lambda e: e.is_private))
async def see_caption(event):
    rkn = await event.reply("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    caption = await digital_botz.get_caption(event.sender_id)  
    if caption:
       await rkn.edit(f"**Yᴏᴜ'ʀᴇ Cᴀᴩᴛɪᴏɴ:-**\n\n`{caption}`")
    else:
       await rkn.edit("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")

@Config.BOT.on(events.NewMessage(pattern=r'^/(view_thumb|viewthumb)', func=lambda e: e.is_private))
async def viewthumb(event):
    rkn = await event.reply("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    thumb = await digital_botz.get_thumbnail(event.sender_id)
    if thumb:
        # Telethon send_file can handle various input types (path, bytes, input location)
        # Note: If 'thumb' in DB is a Pyrogram file_id string, Telethon might fail to send it.
        # This works best if the thumb was saved using the 'addthumbs' handler below (Telethon format).
        try:
            await event.client.send_file(event.chat_id, file=thumb)
            await rkn.delete()
        except Exception as e:
            await rkn.edit(f"❌ Error sending thumb (Use /del_thumb and set again): {e}")
    else:
        await rkn.edit("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__") 
		
@Config.BOT.on(events.NewMessage(pattern=r'^/(del_thumb|delete_thumb|delthumb)', func=lambda e: e.is_private))
async def removethumb(event):
    rkn = await event.reply("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    thumb = await digital_botz.get_thumbnail(event.sender_id)
    if thumb:
        await digital_botz.set_thumbnail(event.sender_id, file_id=None)
        await rkn.edit("❌️ __**Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ**__")
        return
    await rkn.edit("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__")

# Filter for photos to set thumbnail
@Config.BOT.on(events.NewMessage(func=lambda e: e.is_private and e.photo))
async def addthumbs(event):
    rkn = await event.reply("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    
    # Generate a persistent file reference string for Telethon
    # This replaces Pyrogram's file_id logic
    try:
        file_id_str = utils.pack_bot_file_id(event.media)
        await digital_botz.set_thumbnail(event.sender_id, file_id=file_id_str)                
        await rkn.edit("✅️ __**Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ**__")
    except Exception as e:
        await rkn.edit(f"❌ Error saving thumbnail: {e}")

# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Update Channel @Digital_Botz & @DigitalBotz_Support
