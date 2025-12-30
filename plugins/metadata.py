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

# Telethon imports
from telethon import events, Button
import asyncio

# extra imports
from helper.database import digital_botz
from config import rkn, Config

# Telethon Button Layouts
TRUE = [
    [Button.inline('ᴍᴇᴛᴀᴅᴀᴛᴀ ᴏɴ', data='metadata_1'),
     Button.inline('✅', data='metadata_1')],
    [Button.inline('Sᴇᴛ Cᴜsᴛᴏᴍ Mᴇᴛᴀᴅᴀᴛᴀ', data='cutom_metadata')]
]

FALSE = [
    [Button.inline('ᴍᴇᴛᴀᴅᴀᴛᴀ ᴏғғ', data='metadata_0'),
     Button.inline('❌', data='metadata_0')],
    [Button.inline('Sᴇᴛ Cᴜsᴛᴏᴍ Mᴇᴛᴀᴅᴀᴛᴀ', data='cutom_metadata')]
]


@Config.BOT.on(events.NewMessage(pattern=r'^/metadata$', func=lambda e: e.is_private))
async def handle_metadata(event):
    # Send initial "Please wait" message
    rkn_dev = await event.reply("**Please Wait...**")
    
    user_id = event.sender_id
    bool_metadata = await digital_botz.get_metadata_mode(user_id)
    user_metadata = await digital_botz.get_metadata_code(user_id)

    await rkn_dev.edit(
        f"Your Current Metadata:-\n\n➜ `{user_metadata}`",
        buttons=(TRUE if bool_metadata else FALSE)
    )


@Config.BOT.on(events.CallbackQuery(pattern=r'.*?(cutom_metadata|metadata).*?'))
async def query_metadata(event):
    bot = event.client
    data = event.data.decode('utf-8')
    user_id = event.sender_id

    if data.startswith('metadata_'):
        _bool = data.split('_')[1]
        user_metadata = await digital_botz.get_metadata_code(user_id)
        
        # Determine boolean state (0 or 1)
        # Note: eval is risky, strict comparison is safer, but keeping original logic flow
        bool_meta = bool(int(_bool)) 
        
        await digital_botz.set_metadata_mode(user_id, bool_meta=not bool_meta)
        
        # Update the message
        await event.edit(
            f"Your Current Metadata:-\n\n➜ `{user_metadata}`", 
            buttons=(FALSE if bool_meta else TRUE)
        )
           
    elif data == 'cutom_metadata':
        await event.delete()
        
        # Telethon Conversation to simulate bot.ask
        try:
            async with bot.conversation(user_id, timeout=30) as conv:
                prompt_msg = await conv.send_message(
                    text=rkn.SEND_METADATA,
                    link_preview=False
                )
                
                # Wait for response
                metadata_response = await conv.get_response()
                
                rkn_dev = await metadata_response.reply("**Please Wait...**")
                await digital_botz.set_metadata_code(user_id, metadata_code=metadata_response.text)
                await rkn_dev.edit("**Your Metadata Code Set Successfully ✅**")
                
        except asyncio.TimeoutError:
            # Telethon/Asyncio timeout
            await bot.send_message(
                user_id,
                "⚠️ Error!!\n\n**Request timed out.**\nRestart by using /metadata"
            )
        except Exception as e:
            print(f"Metadata Error: {e}")
            await bot.send_message(user_id, f"Error: {e}")

# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
