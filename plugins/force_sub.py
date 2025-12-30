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
from telethon import events, Button, errors
from telethon.tl.types import ChannelParticipantBanned, ChannelParticipantLeft

# extra imports
from config import Config
from helper.database import digital_botz
import datetime 

async def not_subscribed(client, event):
    # Ensure user is in DB
    # Note: Ensure digital_botz.add_user can handle Telethon events or (client, user_id)
    await digital_botz.add_user(client, event)
    
    if not Config.FORCE_SUB:
        return False

    try:
        # Telethon: get_participant raises UserNotParticipantError if not found
        user_id = event.sender_id
        participant = await client.get_participant(Config.FORCE_SUB, user_id)
        
        # specific check for Banned or Left explicitly returned
        if isinstance(participant, (ChannelParticipantBanned, ChannelParticipantLeft)):
            return True
            
        return False
        
    except errors.UserNotParticipantError:
        return True
    except Exception as e:
        print(f"Error checking subscription: {e}")
        # If error (e.g. Bot not admin in Force Sub channel), we usually allow to proceed to avoid blocking users
        return False

async def handle_banned_user_status(client, event):
    await digital_botz.add_user(client, event) 
    user_id = event.sender_id
    ban_status = await digital_botz.get_ban_status(user_id)
    
    if ban_status.get("is_banned", False):
        if ( datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await digital_botz.remove_ban(user_id)
        else:
            await event.reply("Sorry Sir, 😔 You are Banned!.. Please Contact - @xspes")
            # Telethon way to stop other handlers from processing this event
            raise events.StopPropagation
    
    # In Telethon, we don't need continue_propagation() explicitly 
    # unless we stopped it elsewhere. If we don't raise StopPropagation, it continues.
    
async def forces_sub(client, event):
    # Telethon Button format
    buttons = [[Button.url("📢 Join Update Channel 📢", url=f"https://t.me/{Config.FORCE_SUB}")]] 
    text = "**🌟 Welcome! To continue, please join our updates channel for the latest news and features. Thank you for your support! 💙**"

    try:
        user_id = event.sender_id
        participant = await client.get_participant(Config.FORCE_SUB, user_id)
        
        if isinstance(participant, ChannelParticipantBanned):
            return await event.reply("Sᴏʀʀy Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ Tᴏ Uꜱᴇ Mᴇ")
        
        # If we got participant object and they aren't banned, they are likely a member.
        # But if this function was called, it usually means not_subscribed returned True.
        # Double check logic: if we are here, we ask them to join.
        
    except errors.UserNotParticipantError:
        pass # Expected, proceed to send join message
    except Exception as e:
        pass

    return await event.reply(text=text, buttons=buttons)
    
# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Update Channel @Digital_Botz & @DigitalBotz_Support
