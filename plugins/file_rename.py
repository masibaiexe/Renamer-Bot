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

# Telethon imports
from telethon import TelegramClient, events, Button, errors
from telethon.tl.types import DocumentAttributeVideo, DocumentAttributeAudio, ReplyKeyboardForceReply
from telethon.sessions import StringSession
import asyncio
import os
import time
from PIL import Image
from html import escape 

# hachoir imports
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

# bots imports
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path
from helper.database import digital_botz
from helper.ffmpeg import change_metadata
from helper.fast import fast_download, fast_upload
from config import Config

UPLOAD_TEXT = "📤 Uploading file..."
DOWNLOAD_TEXT = "📥 Downloading file..."

# Initialize Premium Client (if String Session exists)
if Config.STRING_SESSION:
    app = TelegramClient(
        StringSession(Config.STRING_SESSION),
        Config.API_ID,
        Config.API_HASH
    )
else:
    app = None

# ---------------------------------------------------------------------------------
#                                HANDLERS
# ---------------------------------------------------------------------------------

@Config.BOT.on(events.NewMessage(func=lambda e: e.is_private and (e.document or e.video or e.audio)))
async def rename_start(event):
    client = event.client
    message = event.message
    user_id = event.sender_id
    
    if not event.file:
        return

    rkn_file = event.file
    filename = rkn_file.name or (message.file.name if message.file else "unknown_file")
    if not filename:
        ext = rkn_file.ext
        filename = f"file{ext}"
        
    filesize = humanbytes(rkn_file.size)
    mime_type = rkn_file.mime_type
    
    dcid = "Unknown"
    if hasattr(message.media, 'document'):
        dcid = message.media.document.dc_id
    elif hasattr(message.media, 'photo'):
        dcid = message.media.photo.dc_id

    extension_type = mime_type.split('/')[0]
    file_ext = filename.split('.')[-1].lower() if '.' in filename else ""

    FILE_TYPE_EMOJIS = {
        "audio": "🎵", "video": "🎬", "image": "🖼️",
        "application": "📦", "text": "📄", "font": "🔤", "default": "📁"
    }
    EXTENSION_EMOJIS = {
        "zip": "🗜️", "rar": "📚", "7z": "🧳", "apk": "🤖", "exe": "💻", "mkv": "📽️", "mp4": "🎥"
    }

    async def send_media_info():
        emoji = EXTENSION_EMOJIS.get(file_ext) or FILE_TYPE_EMOJIS.get(extension_type, FILE_TYPE_EMOJIS["default"])
        text = (
            f"**__{emoji} ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n"
            f"🗃️ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n"
            f"🏷️ ᴇxᴛᴇɴꜱɪᴏɴ: `{file_ext.upper()}`\n"
            f"📏 ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n"
            f"🧬 ᴍɪᴍᴇ ᴛʏᴘᴇ: `{mime_type}`\n"
            f"🆔 ᴅᴄ ɪᴅ: `{dcid}`\n\n"
            f"✏️ ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛᴏ ᴛʜɪs ᴍᴇssᴀɢᴇ...__**"
        )
        await event.reply(text, reply_to=event.id, buttons=ReplyKeyboardForceReply(single_use=True, selective=True))

    # Check Limits
    is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
    is_upload_limit = getattr(Config, 'UPLOAD_LIMIT_MODE', False)

    if is_premium_mode and is_upload_limit:
        await digital_botz.reset_uploadlimit_access(user_id)
        user_data = await digital_botz.get_user_data(user_id)
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)
        remain = int(limit) - int(used)
        if remain < int(rkn_file.size):
            buttons = [[Button.inline("🪪 Uᴘɢʀᴀᴅᴇ", data="plans")]]
            return await event.reply("Limit Exceeded. Buy Premium.", buttons=buttons)

    has_premium = await digital_botz.has_premium_access(user_id)
    
    if has_premium and is_premium_mode:
        if not Config.STRING_SESSION:
            if rkn_file.size > 2000 * 1024 * 1024:
                return await event.reply("⚠️ Bot can't handle 2GB+ without string session.")
        await send_media_info()
    else:
        if rkn_file.size > 2000 * 1024 * 1024 and is_premium_mode:
            return await event.reply("‼️ File > 2GB. Buy Premium.")
        await send_media_info()


@Config.BOT.on(events.NewMessage(func=lambda e: e.is_private and e.is_reply))
async def refunc(event):
    client = event.client
    message = event.message
    reply_message = await event.get_reply_message()
    
    if reply_message and reply_message.reply_markup and isinstance(reply_message.reply_markup, ReplyKeyboardForceReply):
        new_name = message.text 
        await message.delete() 
        
        try:
            file_msg = await client.get_messages(event.chat_id, ids=reply_message.reply_to_msg_id)
        except:
            return await event.reply("Could not find original file.")

        if not file_msg or not file_msg.media:
            return

        media = file_msg.file
        original_name = media.name or "unknown"
        if "." not in new_name:
            if "." in original_name:
                extn = original_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        
        await reply_message.delete()

        buttons = [[Button.inline("📁 Dᴏᴄᴜᴍᴇɴᴛ", data="upload_document")]]
        
        is_video = media.mime_type.startswith('video/')
        is_audio = media.mime_type.startswith('audio/')
            
        if is_video or media.mime_type.startswith('application/') or not (is_video or is_audio):
             buttons.append([Button.inline("🎥 Vɪᴅᴇᴏ", data="upload_video")])
        elif is_audio:
            buttons.append([Button.inline("🎵 Aᴜᴅɪᴏ", data="upload_audio")])

        # Safer send_message logic with fallback
        try:
            await client.send_message(
                event.chat_id,
                f"Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ\n• Fɪʟᴇ Nᴀᴍᴇ :- `{new_name}`",
                reply_to=file_msg.id,
                buttons=buttons
            )
        except Exception as e:
            # Fallback if reply_to fails (e.g. original message deleted)
            await client.send_message(
                event.chat_id,
                f"Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ\n• Fɪʟᴇ Nᴀᴍᴇ :- `{new_name}`",
                buttons=buttons
            )


@Config.BOT.on(events.CallbackQuery(pattern="upload"))
async def doc(event):
    bot = event.client
    msg = await event.get_message()
    original_text = msg.text
    rkn_processing = await msg.edit("`☄️Processing...`", buttons=None)
	
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    user_id = event.chat_id
    try:
        new_name = original_text
        new_filename_ = new_name.split(":-")[1].strip().replace("`", "").replace("**", "")
    except:
        new_filename_ = "unknown_file"

    user_data = await digital_botz.get_user_data(user_id)

    try:
        prefix = await digital_botz.get_prefix(user_id)
        suffix = await digital_botz.get_suffix(user_id)
        new_filename = add_prefix_suffix(new_filename_, prefix, suffix)
    except Exception as e:
        return await rkn_processing.edit(f"Error setting prefix/suffix: {e}")

    file_msg = await msg.get_reply_message()
    if not file_msg and msg.reply_to_msg_id:
        try:
            file_msg = await bot.get_messages(event.chat_id, ids=msg.reply_to_msg_id)
        except:
            pass
            
    if not file_msg or not file_msg.media:
        return await rkn_processing.edit("Original file not found.")

    media = file_msg.file
    file_path = f"Renames/{new_filename}"
    metadata_path = f"Metadata/{new_filename}"    

    await rkn_processing.edit("`☄️Trying To Download....`")
    
    # Limits logic
    is_premium_mode = getattr(Config, 'PREMIUM_MODE', False)
    is_upload_limit = getattr(Config, 'UPLOAD_LIMIT_MODE', False)
    if is_premium_mode and is_upload_limit:
        used = user_data.get('used_limit', 0)
        await digital_botz.set_used_limit(user_id, media.size)
        total_used = int(used) + int(media.size)
        await digital_botz.set_used_limit(user_id, total_used)
	
    start_time = time.time()
    async def progress_wrapper(current, total):
        await progress_for_pyrogram(current, total, DOWNLOAD_TEXT, rkn_processing, start_time)

    try:
        # Stable Download
        dl_path = await fast_download(
            client=bot,
            msg=file_msg,
            file=file_path,
            progress_callback=progress_wrapper
        )
        if not dl_path:
            raise Exception("Download failed")
            
    except Exception as e:
        if is_premium_mode and is_upload_limit:
            used_remove = int(used) - int(media.size)
            await digital_botz.set_used_limit(user_id, used_remove)
        return await rkn_processing.edit(f"Download Error: {e}")

    metadata_mode = await digital_botz.get_metadata_mode(user_id)
    if (metadata_mode):        
        metadata = await digital_botz.get_metadata_code(user_id)
        if metadata:
            await rkn_processing.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")            
            if change_metadata(dl_path, metadata_path, metadata):            
                await rkn_processing.edit("Metadata Added.....")
        await rkn_processing.edit("**Metadata added... Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")
    else:
        await rkn_processing.edit("`☄️Trying To Upload....`")
	    
    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        parser.close()
    except:
        pass
	    
    ph_path = None
    c_caption = await digital_botz.get_caption(user_id)
    c_thumb = await digital_botz.get_thumbnail(user_id)

    if c_caption:
         try:
             caption = c_caption.format(
                 filename=new_filename,
                 filesize=humanbytes(media.size),
                 duration=convert(duration)
             )
         except Exception as e:
             if is_premium_mode and is_upload_limit:
                 used_remove = int(used) - int(media.size)
                 await digital_botz.set_used_limit(user_id, used_remove)
             return await rkn_processing.edit(f"Caption Error: {e}")             
    else:
         caption = f"{new_filename}"
 
    thumb_to_download = None
    if c_thumb:
        thumb_to_download = c_thumb
    elif (file_msg.document and file_msg.document.thumbs) or file_msg.photo:
        thumb_to_download = file_msg 
        
    if thumb_to_download:
         ph_path = "thumb.jpg" 
         try:
             path_ = await bot.download_media(thumb_to_download, file=ph_path, thumb=-1)
             if path_ and os.path.exists(path_):
                 Image.open(path_).convert("RGB").save(path_)
                 img = Image.open(path_)
                 img.resize((320, 320))
                 img.save(path_, "JPEG")
                 ph_path = path_
             else:
                 ph_path = None
         except:
             ph_path = None

    upload_type = event.data.decode("utf-8").split("_")[1] 
    
    upload_client = bot
    if media.size > 2000 * 1024 * 1024:
        if app:
            upload_client = app
        else:
            return await rkn_processing.edit("File > 2GB and no Premium Session configured.")

    final_path = metadata_path if metadata_mode and os.path.exists(metadata_path) else file_path
    
    attributes = []
    if upload_type == "video":
        attributes.append(DocumentAttributeVideo(
            duration=duration,
            w=0, h=0, 
            supports_streaming=True
        ))
    elif upload_type == "audio":
        attributes.append(DocumentAttributeAudio(
            duration=duration,
            title=new_filename.rsplit('.', 1)[0],
            performer="Unknown"
        ))
    
    start_time = time.time()
    async def upload_progress(current, total):
        await progress_for_pyrogram(current, total, UPLOAD_TEXT, rkn_processing, start_time)

    try:
        # FAST UPLOAD (Stable)
        input_file = await fast_upload(
            client=upload_client,
            file_path=final_path,
            progress_callback=upload_progress,
            name=new_filename
        )
        
        # 1. Upload to Log Channel first
        uploaded_msg = await upload_client.send_file(
            Config.LOG_CHANNEL,
            file=input_file,
            thumb=ph_path,
            caption=caption,
            attributes=attributes,
            force_document=(upload_type == "document"),
            parse_mode='html'
        )
        
        # 2. Get reference from Bot Client to ensure compatibility
        msg_ref = await bot.get_messages(Config.LOG_CHANNEL, ids=uploaded_msg.id)
        
        # 3. Send to User (Copying media)
        await bot.send_file(
            user_id,
            file=msg_ref.media,
            caption=caption,
            parse_mode='html'
        )
            
        await bot.delete_messages(Config.LOG_CHANNEL, uploaded_msg.id)
        
    except Exception as e:
        if is_premium_mode and is_upload_limit:
            used_remove = int(used) - int(media.size)
            await digital_botz.set_used_limit(user_id, used_remove)
        await remove_path(ph_path, file_path, dl_path, metadata_path)
        return await rkn_processing.edit(f"Upload Error: {e}")

    await remove_path(ph_path, file_path, dl_path, metadata_path)
    return await rkn_processing.edit("🎈 Uploaded Successfully....", buttons=None)
