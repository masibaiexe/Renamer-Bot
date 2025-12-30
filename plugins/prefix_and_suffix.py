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

# imports
from telethon import events
from helper.database import digital_botz
from config import Config

# prefix commond ✨
@Config.BOT.on(events.NewMessage(pattern=r'^/set_prefix', func=lambda e: e.is_private))
async def add_prefix(event):
    # Split text to check for arguments
    args = event.text.split(" ", 1)
    if len(args) == 1:
        return await event.reply("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @OtherBs`**")
    
    prefix = args[1]
    rkn_dev = await event.reply("Please Wait ...")
    await digital_botz.set_prefix(event.sender_id, prefix)
    await rkn_dev.edit("__**✅ ᴘʀᴇꜰɪx ꜱᴀᴠᴇᴅ**__")

@Config.BOT.on(events.NewMessage(pattern=r'^/del_prefix', func=lambda e: e.is_private))
async def delete_prefix(event):
    rkn_dev = await event.reply("Please Wait ...")
    prefix = await digital_botz.get_prefix(event.sender_id)
    if not prefix:
        return await rkn_dev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await digital_botz.set_prefix(event.sender_id, None)
    await rkn_dev.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Config.BOT.on(events.NewMessage(pattern=r'^/see_prefix', func=lambda e: e.is_private))
async def see_prefix(event):
    rkn_dev = await event.reply("Please Wait ...")
    prefix = await digital_botz.get_prefix(event.sender_id)
    if prefix:
        await rkn_dev.edit(f"**ʏᴏᴜʀ ᴘʀᴇꜰɪx:-**\n\n`{prefix}`")
    else:
        await rkn_dev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")

# SUFFIX COMMOND ✨
@Config.BOT.on(events.NewMessage(pattern=r'^/set_suffix', func=lambda e: e.is_private))
async def add_suffix(event):
    args = event.text.split(" ", 1)
    if len(args) == 1:
        return await event.reply("**__Give The Suffix__\n\nExᴀᴍᴩʟᴇ:- `/set_suffix @OtherBs`**")
    
    suffix = args[1]
    rkn_dev = await event.reply("Please Wait ...")
    await digital_botz.set_suffix(event.sender_id, suffix)
    await rkn_dev.edit("__**✅ ꜱᴜꜰꜰɪx ꜱᴀᴠᴇᴅ**__")

@Config.BOT.on(events.NewMessage(pattern=r'^/del_suffix', func=lambda e: e.is_private))
async def delete_suffix(event):
    rkn_dev = await event.reply("Please Wait ...")
    suffix = await digital_botz.get_suffix(event.sender_id)
    if not suffix:
        return await rkn_dev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")
    await digital_botz.set_suffix(event.sender_id, None)
    await rkn_dev.edit("__**❌️ ꜱᴜꜰꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Config.BOT.on(events.NewMessage(pattern=r'^/see_suffix', func=lambda e: e.is_private))
async def see_suffix(event):
    rkn_dev = await event.reply("Please Wait ...")
    suffix = await digital_botz.get_suffix(event.sender_id)
    if suffix:
        await rkn_dev.edit(f"**ʏᴏᴜʀ ꜱᴜꜰꜰɪx:-**\n\n`{suffix}`")
    else:
        await rkn_dev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")

# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
