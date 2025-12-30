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
"""

# extra imports
import datetime, time, psutil, shutil
from html import escape

# Telethon imports
from telethon import events, Button

# bots imports
from helper.database import digital_botz
from config import Config, rkn
from helper.utils import humanbytes
# Note: Ensure plugins/__init__.py exposes these variables correctly
from plugins import __version__ as _bot_version_, __developer__, __database__, __library__, __language__, __programer__

def format_uptime(seconds: int) -> str:
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

# Helper to generate mentions based on mode
def get_mention(user, mode="html"):
    name = user.first_name if user.first_name else "User"
    if mode == "markdown":
        # Escape brackets for markdown
        safe_name = name.replace("[", "").replace("]", "")
        return f"[{safe_name}](tg://user?id={user.id})"
    else:
        # Default HTML
        return f"<a href='tg://user?id={user.id}'>{escape(name)}</a>"

# Buttons - Defined exactly as requested
upgrade_button = [
    [Button.user_profile(6318135266, text='buy premium ✓')],
    [Button.inline("Bᴀᴄᴋ", data="start")]
]

upgrade_trial_button = [
    [Button.user_profile(6318135266, text='buy premium ✓')],
    [
        Button.inline("ᴛʀɪᴀʟ - 𝟷𝟸 ʜᴏᴜʀs ✓", data="give_trial"),
        Button.inline("Bᴀᴄᴋ", data="start")
    ]
]

# ---------------------------------------------------------------------------------
#                                COMMANDS
# ---------------------------------------------------------------------------------

@Config.BOT.on(events.NewMessage(pattern=r'^/start', func=lambda e: e.is_private))
async def start(event):
    client = event.client
    user = await event.get_sender()
    
    start_button = [
        [
            Button.url('Uᴩᴅᴀ𝚃ᴇꜱ', url='https://t.me/OtherBs'),
            Button.url('Sᴜᴩᴩᴏʀ𝚃', url='https://t.me/DigitalBotz_Support')
        ],
        [
            Button.inline('Aʙᴏυᴛ', data='about'),
            Button.inline('Hᴇʟᴩ', data='help')
        ]
    ]

    is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
    if is_premium_mode:
        start_button.append([
            # Using standard upgrade button here, or change to user_profile if needed
            Button.inline('💸 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ 💸', data='upgrade')
        ])

    await digital_botz.add_user(client, event)

    # Use HTML mention for start message (Config text likely has HTML)
    mention = get_mention(user, mode="html")

    if Config.RKN_PIC:
        await client.send_file(
            event.chat_id,
            Config.RKN_PIC,
            caption=rkn.START_TXT.format(mention),
            buttons=start_button,
            parse_mode='html'
        )
    else:
        await event.reply(
            rkn.START_TXT.format(mention),
            buttons=start_button,
            link_preview=False,
            parse_mode='html'
        )


@Config.BOT.on(events.NewMessage(pattern=r'^/myplan', func=lambda e: e.is_private))
async def myplan(event):
    client = event.client
    is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
    
    if not is_premium_mode:
        return # premium mode disabled ✓

    user_id = event.sender_id
    user = await event.get_sender()
    
    # Use Markdown mention here so we can use backticks for mono font elsewhere
    mention = get_mention(user, mode="markdown")
    
    if await digital_botz.has_premium_access(user_id):
        data = await digital_botz.get_user(user_id)
        expiry_str_in_ist = data.get("expiry_time")
        if expiry_str_in_ist.tzinfo is None:
             expiry_str_in_ist = expiry_str_in_ist.replace(tzinfo=datetime.timezone.utc)
        
        now = datetime.datetime.now(datetime.timezone.utc)
        if expiry_str_in_ist > now:
             time_left = expiry_str_in_ist - now
        else:
             time_left = "Expired"

        # Using Markdown backticks `...` for mono font
        text = f"👤 ᴜꜱᴇʀ :- {mention}\n🆔 ᴜꜱᴇʀ ɪᴅ :- `{user_id}`\n"

        is_upload_limit = getattr(Config, 'UPLOAD_LIMIT_MODE', False)
        if is_upload_limit:
            await digital_botz.reset_uploadlimit_access(user_id)                
            user_data = await digital_botz.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type_plan = user_data.get('usertype', "Free")

            text += f"📦 ᴘʟᴀɴ :- `{type_plan}`\n📈 ᴅᴀɪʟʏ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ :- `{humanbytes(limit)}`\n📊 ᴛᴏᴅᴀʏ ᴜsᴇᴅ :- `{humanbytes(used)}`\n🧮 ʀᴇᴍᴀɪɴ :- `{humanbytes(remain)}`\n\n"

        text += f"⏳ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left}\n\n📅 ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}"

        # No parse_mode specified = Default Markdown
        await event.reply(text)

    else:
        is_upload_limit = getattr(Config, 'UPLOAD_LIMIT_MODE', False)
        if is_upload_limit:
            user_data = await digital_botz.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type_plan = user_data.get('usertype', "Free")

            text = f"👤 ᴜꜱᴇʀ :- {mention}\n🆔 ᴜꜱᴇʀ ɪᴅ :- `{user_id}`\n📦 ᴘʟᴀɴ :- `{type_plan}`\n📈 ᴅᴀɪʟʏ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ :- `{humanbytes(limit)}`\n📊 ᴛᴏᴅᴀʏ ᴜsᴇᴅ :- `{humanbytes(used)}`\n🧮 ʀᴇᴍᴀɪɴ :- `{humanbytes(remain)}`\n📅 ᴇxᴘɪʀᴇᴅ ᴅᴀᴛᴇ :- ʟɪғᴇᴛɪᴍᴇ\n\n💎 ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ, ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ 👇"

            # Button to upgrade
            await event.reply(text, buttons=[[Button.inline("💸 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ 💸", data='upgrade')]])

        else:
            await event.reply(
                f"ʜᴇʏ {mention},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ. ᴛᴏ ᴘᴜʀᴄʜᴀꜱᴇ ᴘʀᴇᴍɪᴜᴍ, ᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ. 👇",
                buttons=[[Button.inline("💸 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ 💸", data='upgrade')]]
            )

@Config.BOT.on(events.NewMessage(pattern=r'^/plans', func=lambda e: e.is_private))
async def plans(event):
    is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
    if not is_premium_mode:
        return # premium mode disabled ✓

    client = event.client
    user = await event.get_sender()
    mention = get_mention(user, mode="html") # Back to HTML for plans
    
    is_upload_limit = getattr(Config, 'UPLOAD_LIMIT_MODE', False)
    upgrade_msg = rkn.UPGRADE_PLAN.format(mention) if is_upload_limit else rkn.UPGRADE_PREMIUM.format(mention)
    
    free_trial_status = await digital_botz.get_free_trial_status(user.id)
    if not await digital_botz.has_premium_access(user.id):
        if not free_trial_status:
            await event.reply(upgrade_msg, buttons=upgrade_trial_button, link_preview=False, parse_mode='html')
        else:
            await event.reply(upgrade_msg, buttons=upgrade_button, link_preview=False, parse_mode='html')
    else:
        await event.reply(upgrade_msg, buttons=upgrade_button, link_preview=False, parse_mode='html')


# ---------------------------------------------------------------------------------
#                                CALLBACK HANDLERS
# ---------------------------------------------------------------------------------

@Config.BOT.on(events.CallbackQuery())
async def cb_handler(event):
    client = event.client
    data = event.data.decode("utf-8")
    user = await event.get_sender()
    mention = get_mention(user, mode="html")

    if data == "start":
        start_button = [
            [
                Button.url('Uᴩᴅᴀ𝚃ᴇꜱ', url='https://t.me/OtherBs'),
                Button.url('Sᴜᴩᴩᴏʀ𝚃', url='https://t.me/DigitalBotz_Support')
            ],
            [
                Button.inline('Aʙᴏυᴛ', data='about'),
                Button.inline('Hᴇʟᴩ', data='help')       
            ]
        ]
        is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
        if is_premium_mode:
            start_button.append([Button.inline('💸 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ 💸', data='upgrade')])
        
        await event.edit(
            rkn.START_TXT.format(mention),
            link_preview=False,
            buttons=start_button,
            parse_mode='html'
        )

    elif data == "help":
        await event.edit(
            rkn.HELP_TXT,
            link_preview=False,
            buttons=[
                [
                    Button.inline("ᴛʜᴜᴍʙɴᴀɪʟ", data="thumbnail"),
                    Button.inline("ᴄᴀᴘᴛɪᴏɴ", data="caption")
                ],
                [
                    Button.inline("ᴄᴜsᴛᴏᴍ ғɪʟᴇ ɴᴀᴍᴇ", data="custom_file_name")
                ],
                [
                    Button.inline("ᴀʙᴏᴜᴛ", data="about"),
                    Button.inline("ᴍᴇᴛᴀᴅᴀᴛᴀ", data="digital_meta_data")
                ],
                [
                    Button.inline("Bᴀᴄᴋ", data="start")
                ]
            ],
            parse_mode='html'
        ) 

    elif data == "about":
        about_button = [
            [
                Button.inline("𝚂ᴏᴜʀᴄᴇ", data="source_code"),
                Button.inline("ʙᴏᴛ sᴛᴀᴛᴜs", data="bot_status")
            ],
            [
                Button.inline("ʟɪᴠᴇ sᴛᴀᴛᴜs", data="live_status")
            ]
        ]
        
        is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
        if is_premium_mode:
            about_button[-1].append(Button.inline("ᴜᴘɢʀᴀᴅᴇ", data="upgrade"))
            about_button.append([Button.inline("Bᴀᴄᴋ", data="start")])
        else:
            about_button[-1].append(Button.inline("Bᴀᴄᴋ", data="start"))
            
        bot_user = await client.get_me()
        bot_mention = get_mention(bot_user, mode="html")
        
        await event.edit(
            rkn.ABOUT_TXT.format(
                bot_mention, 
                __developer__, __programer__, __library__, __language__, __database__, _bot_version_
            ),
            link_preview=False,
            buttons=about_button,
            parse_mode='html'
        )

    elif data == "upgrade":
        is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
        if not is_premium_mode:
            return await event.delete()
            
        is_upload_limit = getattr(Config, 'UPLOAD_LIMIT_MODE', False)
        upgrade_msg = rkn.UPGRADE_PLAN.format(mention) if is_upload_limit else rkn.UPGRADE_PREMIUM.format(mention)
        
        free_trial_status = await digital_botz.get_free_trial_status(event.sender_id)
        if not await digital_botz.has_premium_access(event.sender_id):
            if not free_trial_status:
                await event.edit(upgrade_msg, link_preview=False, buttons=upgrade_trial_button, parse_mode='html')
            else:
                await event.edit(upgrade_msg, link_preview=False, buttons=upgrade_button, parse_mode='html')
        else:
            await event.edit(upgrade_msg, link_preview=False, buttons=upgrade_button, parse_mode='html')

    elif data == "give_trial":
        is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
        if not is_premium_mode:
            return await event.delete()
            
        await event.delete()
        free_trial_status = await digital_botz.get_free_trial_status(event.sender_id)
        if not free_trial_status:
            await digital_botz.give_free_trail(event.sender_id)
            new_text = "**ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴛʀɪᴀʟ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ғᴏʀ 𝟷𝟸 ʜᴏᴜʀs...**"
        else:
            new_text = "**🤣 ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴜsᴇᴅ ғʀᴇᴇ...**"
        await client.send_message(event.sender_id, message=new_text, parse_mode='html')

    elif data == "thumbnail":
        await event.edit(
            rkn.THUMBNAIL, 
            link_preview=False,
            buttons=[[Button.inline(" Bᴀᴄᴋ", data="help")]],
            parse_mode='html'
        )

    elif data == "caption":
        await event.edit(
            rkn.CAPTION, 
            link_preview=False,
            buttons=[[Button.inline(" Bᴀᴄᴋ", data="help")]],
            parse_mode='html'
        )

    elif data == "custom_file_name":
        await event.edit(
            rkn.CUSTOM_FILE_NAME, 
            link_preview=False,
            buttons=[[Button.inline(" Bᴀᴄᴋ", data="help")]],
            parse_mode='html'
        )

    elif data == "digital_meta_data":
        await event.edit(
            rkn.DIGITAL_METADATA, 
            link_preview=False,
            buttons=[[Button.inline(" Bᴀᴄᴋ", data="help")]],
            parse_mode='html'
        )

    elif data == "bot_status":
        real_total_users = await digital_botz.total_users_count()
        real_total_premium_users = await digital_botz.total_premium_users_count()
        total_users = real_total_users + 1009
        
        is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
        total_premium_users = real_total_premium_users + 50 if is_premium_mode else "Disabled ✅"
        
        uptime_seconds = int(time.time() - Config.BOT_UPTIME)
        uptime = format_uptime(uptime_seconds)
        
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        
        # Fixed: Removed parse_mode here as requested
        await event.edit(
            rkn.BOT_STATUS.format(uptime, total_users, total_premium_users, sent, recv),
            link_preview=False,
            buttons=[[Button.inline(" Bᴀᴄᴋ", data="about")]]
        )

    elif data == "live_status":
        uptime_seconds = int(time.time() - Config.BOT_UPTIME)
        uptime = format_uptime(uptime_seconds)
        
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Fixed: Removed parse_mode here as requested
        await event.edit(
            rkn.LIVE_STATUS.format(uptime, cpu_usage, ram_usage, total, used, disk_usage, free, sent, recv),
            link_preview=False,
            buttons=[[Button.inline(" Bᴀᴄᴋ", data="about")]]
        )

    elif data == "source_code":
        await event.edit(
            rkn.DEV_TXT,
            link_preview=False,
            buttons=[
                [
                    Button.url(
                        "💞 Mᴀɪɴ Sᴏᴜʀᴄᴇ 💞",
                        url="https://github.com/DigitalBotz/Digital-Rename-Bot"
                    )
                ],
                [
                    Button.url(
                        "🍴 Fᴏʀᴋᴇᴅ Sᴏᴜʀᴄᴇ 🍴",
                        url="https://github.com/yudurov/Digital-Renamer-Bot"
                    )
                ],
                [
                    Button.inline("🔒 Cʟᴏꜱᴇ", data="close"),
                    Button.inline("◀️ Bᴀᴄᴋ", data="start")
                ]
            ],
            parse_mode='html'
        )

    elif data == "close":
        try:
            await event.delete()
            reply_msg = await event.get_reply_message()
            if reply_msg:
                await reply_msg.delete()
        except:
            pass
