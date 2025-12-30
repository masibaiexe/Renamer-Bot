import asyncio
import os
import time
from telethon import utils

async def fast_download(client, msg, file, progress_callback=None):
    """
    Native Telethon download. 
    Parallel downloading on a single client session often causes 'TLObject' errors.
    This method is stable and fast if 'cryptg' is installed.
    """
    try:
        # download_media handles DC switching and file creation automatically
        return await client.download_media(
            msg, 
            file=file, 
            progress_callback=progress_callback
        )
    except Exception as e:
        print(f"Fast Download Error: {e}")
        return None

async def fast_upload(client, file_path, progress_callback=None, name=None):
    """
    Native Telethon upload with optimized part size.
    """
    try:
        # Telethon's upload_file is highly optimized in recent versions.
        # part_size_kb=512 is a sweet spot for speed/stability.
        return await client.upload_file(
            file_path,
            progress_callback=progress_callback,
            file_name=name,
            part_size_kb=512
        )
    except Exception as e:
        print(f"Fast Upload Error: {e}")
        return None
