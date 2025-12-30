# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To (https://github.com/JayMahakal98) & @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support

"""
Apache License 2.0
Copyright (c) 2022 @Digital_Botz
"""

# extra imports
import math, time, re, datetime, pytz, os
from config import Config, rkn
import random

# Telethon imports
from telethon import Button, errors

def get_speed_icon(speed_bps):
    speed_mbps = speed_bps / (1024 * 1024)
    if speed_mbps < 7:
        return "🐢"
    elif speed_mbps < 11:
        return "🚀"
    else:
        return "🛸"

async def progress_for_pyrogram(current, total, ud_type, message, start):
    # Note: 'message' is a Telethon Message object
    now = time.time()
    diff = now - start
    
    # Update every 5 seconds or at the end
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        speed_icon = get_speed_icon(speed)
        elapsed_time = round(diff) * 1000
        if speed > 0:
            time_to_completion = round((total - current) / speed) * 1000
        else:
            time_to_completion = 0
            
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress_bar = "{0}{1}".format(
            ''.join(["▣" for _ in range(math.floor(percentage / 5))]),
            ''.join(["▢" for _ in range(20 - math.floor(percentage / 5))])
        )

        # Formatted Output
        tmp = (
            f"<b>{ud_type}</b>\n\n"
            f"{progress_bar}\n\n"
            f"<b>╭━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━━➣</b>\n"
            f"<b>┃    🗂️ ᴄᴏᴍᴘʟᴇᴛᴇᴅ: {humanbytes(current)}</b>\n"
            f"<b>┃    📦 ᴛᴏᴛᴀʟ ꜱɪᴢᴇ: {humanbytes(total)}</b>\n"
            f"<b>┃    🔋 ꜱᴛᴀᴛᴜꜱ: {round(percentage, 2)}%</b>\n"
            f"<b>┃    {speed_icon} ꜱᴘᴇᴇᴅ: {humanbytes(speed)}/s</b>\n"
            f"<b>┃    ⏰ ᴇᴛᴀ: {estimated_total_time}</b>\n"
            f"<b>╰━━━━━━━━━━━━━━━━➣</b>"
        )

        try:
            # Telethon edit
            await message.edit(
                text=tmp,
                parse_mode='html',
                buttons=[[Button.inline("✖️ 𝙲𝙰𝙽𝙲ᴇʟ ✖️", data="close")]]
            )
        except errors.MessageNotModifiedError:
            pass
        except Exception as e:
            print(f"Progress Error: {e}")


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2]


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


async def send_log(b, u):
    if Config.LOG_CHANNEL:
        curr = datetime.datetime.now(pytz.timezone("Africa/Nairobi"))
        
        # Telethon doesn't have .mention property, manual markdown
        name = u.first_name if u.first_name else "User"
        user_mention = f"[{name}](tg://user?id={u.id})"
        username = f"@{u.username}" if u.username else "None"
        
        # Bot mention
        try:
            bot_me = await b.get_me()
            bot_mention = f"[{bot_me.first_name}](tg://user?id={bot_me.id})"
        except:
            bot_mention = "Bot"

        log_message = (
            "**🚀--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\n"
            f"📜Uꜱᴇʀ: {user_mention}\n"
            f"🆔Iᴅ: `{u.id}`\n"
            f"👤Uɴ: {username}\n\n"
            f"🗓️Dᴀᴛᴇ: {curr.strftime('%d %B, %Y')}\n"
            f"⏰Tɪᴍᴇ: {curr.strftime('%I:%M:%S %p')}\n\n"
            f"🚀Started: {bot_mention}"
        )
        try:
            await b.send_message(Config.LOG_CHANNEL, log_message)
        except Exception as e:
            print(f"Error sending log: {e}")


async def get_seconds_first(time_string):
    conversion_factors = {
        's': 1,
        'min': 60,
        'hour': 3600,
        'day': 86400,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    parts = time_string.split()
    total_seconds = 0

    for i in range(0, len(parts), 2):
        value = int(parts[i])
        unit = parts[i+1].rstrip('s')
        total_seconds += value * conversion_factors.get(unit, 0)

    return total_seconds


async def get_seconds(time_string):
    conversion_factors = {
        's': 1,
        'min': 60,
        'hour': 3600,
        'day': 86400,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    total_seconds = 0
    pattern = r'(\d+)\s*(\w+)'
    matches = re.findall(pattern, time_string)

    for value, unit in matches:
        total_seconds += int(value) * conversion_factors.get(unit, 0)

    return total_seconds


def add_prefix_suffix(input_string, prefix='', suffix=''):
    pattern = r'(?P<filename>.*?)(\.\w+)?$'
    match = re.search(pattern, input_string)

    if match:
        filename = match.group('filename')
        extension = match.group(2) or ''

        prefix_str = f"{prefix} " if prefix else ""
        suffix_str = f" {suffix}" if suffix else ""

        return f"{prefix_str}{filename}{suffix_str}{extension}"
    else:
        return input_string


async def remove_path(*paths):
    for path in paths:
        if path and os.path.lexists(path):
            os.remove(path)


def metadata_text(metadata_text):
    author = None
    title = None
    video_title = None
    audio_title = None
    subtitle_title = None

    flags = [i.strip() for i in metadata_text.split('--')]
    for f in flags:
        if "change-author" in f:
            author = f[len("change-author"):].strip()
        if "change-title" in f:
            title = f[len("change-title"):].strip()
        if "change-video-title" in f:
            video_title = f[len("change-video-title"):].strip()
        if "change-audio-title" in f:
            audio_title = f[len("change-audio-title"):].strip()
        if "change-subtitle-title" in f:
            subtitle_title = f[len("change-subtitle-title"):].strip()

    return author, title, video_title, audio_title, subtitle_title


# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
