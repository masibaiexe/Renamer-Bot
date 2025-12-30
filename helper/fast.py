import asyncio
import os
import time
from telethon import utils

async def fast_download(client, msg, file, progress_callback=None):
    """
    Standard Telethon download. 
    This handles DC switching and file creation automatically, preventing 'TLObject' errors.
    """
    try:
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
    Standard Telethon upload with optimized part size.
    """
    try:
        # 512kb part size is the sweet spot for speed and stability in Telethon
        return await client.upload_file(
            file_path,
            progress_callback=progress_callback,
            file_name=name,
            part_size_kb=512
        )
    except Exception as e:
        print(f"Fast Upload Error: {e}")
        return None
